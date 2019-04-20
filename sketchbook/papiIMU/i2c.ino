// < defines >-------------------------------------------------------------------------------------

#include <L3G.h>
#include <LSM303.h>

// < data >----------------------------------------------------------------------------------------

L3G gyro;
LSM303 compass;

// ------------------------------------------------------------------------------------------------
void 
i2c_init()
{
    Wire.begin();

} // i2c_init

// ------------------------------------------------------------------------------------------------
void 
gyro_init()
{
    gyro.init();
    gyro.enableDefault();
    gyro.writeReg(L3G::CTRL_REG4, 0x20);  // 2000 dps full scale
    gyro.writeReg(L3G::CTRL_REG1, 0x0F);  // normal power mode, all axes enabled, 100 Hz

} // gyro_init

// ------------------------------------------------------------------------------------------------
void 
read_gyro()
{
    gyro.read();

    AN[0] = gyro.g.x;
    AN[1] = gyro.g.y;
    AN[2] = gyro.g.z;

    gyro_x = SENSOR_SIGN[0] * (AN[0] - AN_OFFSET[0]);
    gyro_y = SENSOR_SIGN[1] * (AN[1] - AN_OFFSET[1]);
    gyro_z = SENSOR_SIGN[2] * (AN[2] - AN_OFFSET[2]);

} // read_gyro

// ------------------------------------------------------------------------------------------------
void 
accel_init()
{
    compass.init();
    compass.enableDefault();

    switch (compass.getDeviceType())
    {
        case LSM303::device_D:
            compass.writeReg(LSM303::CTRL2, 0x18);  // 8 g full scale: AFS = 011
            break;

        case LSM303::device_DLHC:
            compass.writeReg(LSM303::CTRL_REG4_A, 0x28);  // 8 g full scale: FS = 10; high resolution output mode
            break;

        default: // DLM, DLH
            compass.writeReg(LSM303::CTRL_REG4_A, 0x30);  // 8 g full scale: FS = 11

    } // end switch

} // accel_init

// ------------------------------------------------------------------------------------------------
// reads x, y and z accelerometer registers
void 
read_accel()
{
    compass.readAcc();

    AN[3] = compass.a.x >> 4;  // shift left 4 bits to use 12-bit representation (1 g = 256)
    AN[4] = compass.a.y >> 4;
    AN[5] = compass.a.z >> 4;

    accel_x = SENSOR_SIGN[3] * (AN[3] - AN_OFFSET[3]);
    accel_y = SENSOR_SIGN[4] * (AN[4] - AN_OFFSET[4]);
    accel_z = SENSOR_SIGN[5] * (AN[5] - AN_OFFSET[5]);

} // read_accel

// ------------------------------------------------------------------------------------------------
void 
compass_init()
{
    // LSM303: doesn't need to do anything because accel_init() should have already called compass.enableDefault()

} // compass_init

// ------------------------------------------------------------------------------------------------
void 
read_compass()
{
    compass.readMag();

    magnetom_x = SENSOR_SIGN[6] * compass.m.x;
    magnetom_y = SENSOR_SIGN[7] * compass.m.y;
    magnetom_z = SENSOR_SIGN[8] * compass.m.z;

} // read_compass

// < the end >-------------------------------------------------------------------------------------
