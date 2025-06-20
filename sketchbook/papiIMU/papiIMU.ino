
// Uncomment the below line to use this axis definition:
   // X axis pointing forward
   // Y axis pointing to the right
   // and Z axis pointing down.
// Positive pitch : nose up
// Positive roll : right wing down
// Positive yaw : clockwise

int SENSOR_SIGN[9] = {1,1,1,-1,-1,-1,1,1,1}; // Correct directions x,y,z - gyro, accelerometer, magnetometer

// Uncomment the below line to use this axis definition:
   // X axis pointing forward
   // Y axis pointing to the left
   // and Z axis pointing up.
// Positive pitch : nose down
// Positive roll : right wing down
// Positive yaw : counterclockwise
//int SENSOR_SIGN[9] = {1,-1,-1,-1,1,1,1,-1,-1}; // Correct directions x,y,z - gyro, accelerometer, magnetometer

// < includes >------------------------------------------------------------------------------------

#include <Wire.h>

// < defines >-------------------------------------------------------------------------------------

// accelerometer: 8 g sensitivity
// 3.9 mg/digit; 1 g = 256
#define GRAVITY 256  // this equivalent to 1G in the raw data coming from the accelerometer

#define ToRad(x) ((x)*0.01745329252)  // *pi/180
#define ToDeg(x) ((x)*57.2957795131)  // *180/pi

// gyro: 2000 dps full scale
// 70 mdps/digit; 1 dps = 0.07
#define Gyro_Gain_X 0.07  // X axis Gyro gain
#define Gyro_Gain_Y 0.07  // Y axis Gyro gain
#define Gyro_Gain_Z 0.07  // Z axis Gyro gain

#define Gyro_Scaled_X(x) ((x)*ToRad(Gyro_Gain_X))  // return the scaled ADC raw data of the gyro in radians for second
#define Gyro_Scaled_Y(x) ((x)*ToRad(Gyro_Gain_Y))  // return the scaled ADC raw data of the gyro in radians for second
#define Gyro_Scaled_Z(x) ((x)*ToRad(Gyro_Gain_Z))  // return the scaled ADC raw data of the gyro in radians for second

// LSM303/LIS3MDL magnetometer calibration constants; use the Calibrate example from
// the Pololu LSM303 or LIS3MDL library to find the right values for your board

#define M_X_MIN -1330
#define M_Y_MIN -1481
#define M_Z_MIN -1812
#define M_X_MAX +1535
#define M_Y_MAX +1229
#define M_Z_MAX +742

#define Kp_ROLLPITCH 0.02
#define Ki_ROLLPITCH 0.00002

#define Kp_YAW 1.2
#define Ki_YAW 0.00002

/* for debugging purposes */
// OUTPUTMODE=1 will print the corrected data,
// OUTPUTMODE=0 will print uncorrected data of the gyros (with drift)
#define OUTPUTMODE 1

#define PRINT_DCM 0      // will print the whole direction cosine matrix
#define PRINT_ANALOGS 1  // will print the analog raw data
#define PRINT_EULER 1    // will print the Euler angles Roll, Pitch and Yaw

#define STATUS_LED 13

// < data >----------------------------------------------------------------------------------------

float G_Dt = 0.02; // integration time (DCM algorithm)  We will run the integration loop at 50Hz if possible

long timer = 0;    // general purpuse timer
long timer_old;
long timer24 = 0;  // second timer used to print values

int AN[6];  // array that stores the gyro and accelerometer data
int AN_OFFSET[6] = {0, 0, 0, 0, 0, 0};  // array that stores the Offset of the sensors

int gyro_x;
int gyro_y;
int gyro_z;

int accel_x;
int accel_y;
int accel_z;

int magnetom_x;
int magnetom_y;
int magnetom_z;

float c_magnetom_x;
float c_magnetom_y;
float c_magnetom_z;

float MAG_Heading;

float Accel_Vector[3] = {0,0,0};  // store the acceleration in a vector
float Gyro_Vector[3] = {0,0,0};   // store the gyros turn rate in a vector

float Omega_Vector[3] = {0,0,0};  // corrected Gyro_Vector data
float Omega_P[3] = {0,0,0};       // omega Proportional correction
float Omega_I[3] = {0,0,0};       // omega Integrator
float Omega[3] = {0,0,0};

// Euler angles
float roll;
float pitch;
float yaw;

float errorRollPitch[3] = {0,0,0};
float errorYaw[3] = {0,0,0};

unsigned int counter = 0;
byte gyro_sat = 0;

float DCM_Matrix[3][3] = {{1, 0, 0},
                          {0, 1, 0},
                          {0, 0, 1}};

float Update_Matrix[3][3] = {{0, 1, 2},
                             {3, 4, 5},
                             {6, 7, 8}};  // gyros here

float Temporary_Matrix[3][3] = {{0, 0, 0},
                                {0, 0, 0},
                                {0, 0, 0}};

// ------------------------------------------------------------------------------------------------
void 
setup()
{
    Serial.begin(115200);
    pinMode(STATUS_LED, OUTPUT);  // status LED

    i2c_init();

    digitalWrite(STATUS_LED, LOW); 
    delay(1500);

    accel_init();
    compass_init();
    gyro_init();

    delay(20);

    for (int i = 0; i < 32; i++)  // we take some readings...
    {
        read_gyro();
        read_accel();

        for (int y = 0; y < 6; y++)  // cumulate values
            AN_OFFSET[y] += AN[y];

        delay(20);

    } // end for

    for (int y = 0; y < 6; y++)
        AN_OFFSET[y] = AN_OFFSET[y] / 32;

    AN_OFFSET[5] -= GRAVITY * SENSOR_SIGN[5];

    // Serial.println("Offset:");
    // for (int y = 0; y < 6; y++)
       // Serial.println(AN_OFFSET[y]);

    delay(2000);
    digitalWrite(STATUS_LED, HIGH);

    timer = millis();
    delay(20);
    counter = 0;

} // setup

// ------------------------------------------------------------------------------------------------
void 
loop() // main Loop
{
    if ((millis() - timer) >= 20)  // main loop runs at 50Hz
    {
        timer_old = timer;
        timer = millis();

        if (timer > timer_old)
        {
            G_Dt = (timer - timer_old) / 1000.0;    // real time of loop run. We use this on the DCM algorithm (gyro integration time)

            if (G_Dt > 0.2)
                G_Dt = 0;  // ignore integration times over 200 ms
        }
        else
            G_Dt = 0;

        // *** DCM algorithm
        // data adquisition
        read_gyro();   // this read gyro data
        read_accel();  // read I2C accelerometer

        counter++;

        if (counter > 5)  // read compass data at 10Hz... (5 loop runs)
        {
            counter=0;
            read_compass();     // read I2C magnetometer
            compass_heading();  // calculate magnetic heading

        } // end if

        // calculations...
        matrix_update();
        normalize();
        drift_correction();
        euler_angles();
        // ***

        printdata();

    } // end if

} // loop

// < the end >-------------------------------------------------------------------------------------
