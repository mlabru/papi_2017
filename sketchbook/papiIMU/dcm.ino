// ------------------------------------------------------------------------------------------------
void
dcm_normalize(void)
{
    float error = 0;
    float temporary[3][3];
    float renorm = 0;

    error = -vector_dot_product(&DCM_Matrix[0][0], &DCM_Matrix[1][0]) *.5;  // eq.19

    vector_scale(&temporary[0][0], &DCM_Matrix[1][0], error);  // eq.19
    vector_scale(&temporary[1][0], &DCM_Matrix[0][0], error);  // eq.19

    vector_add(&temporary[0][0], &temporary[0][0], &DCM_Matrix[0][0]); // eq.19
    vector_add(&temporary[1][0], &temporary[1][0], &DCM_Matrix[1][0]); // eq.19

    vector_cross_product(&temporary[2][0], &temporary[0][0], &temporary[1][0]);  // c = a x b // eq.20

    renorm = .5 * (3 - vector_dot_product(&temporary[0][0], &temporary[0][0]));  // eq.21
    vector_scale(&DCM_Matrix[0][0], &temporary[0][0], renorm);

    renorm = .5 * (3 - vector_dot_product(&temporary[1][0], &temporary[1][0]));  // eq.21
    vector_scale(&DCM_Matrix[1][0], &temporary[1][0], renorm);

    renorm = .5 * (3 - vector_dot_product(&temporary[2][0], &temporary[2][0]));  // eq.21
    vector_scale(&DCM_Matrix[2][0], &temporary[2][0], renorm);

} // normalize

// ------------------------------------------------------------------------------------------------
void
dcm_drift_correction(void)
{
    float mag_heading_x;
    float mag_heading_y;
    float errorCourse;

    // Compensation the Roll, Pitch and Yaw drift
    static float Scaled_Omega_P[3];
    static float Scaled_Omega_I[3];

    float Accel_magnitude;
    float Accel_weight;

    //*****Roll and Pitch***************

    // calculate the magnitude of the accelerometer vector
    Accel_magnitude = sqrt(Accel_Vector[0] * Accel_Vector[0] + Accel_Vector[1] * Accel_Vector[1] + Accel_Vector[2] * Accel_Vector[2]);
    Accel_magnitude = Accel_magnitude / GRAVITY;  // Scale to gravity

    // dynamic weighting of accelerometer info (reliability filter)
    // Weight for accelerometer info (<0.5G = 0.0, 1G = 1.0 , >1.5G = 0.0)
    Accel_weight = constrain(1 - 2 * abs(1 - Accel_magnitude), 0, 1);

    vector_cross_product(&errorRollPitch[0], &Accel_Vector[0], &DCM_Matrix[2][0]);  // adjust the ground of reference
    vector_scale(&Omega_P[0], &errorRollPitch[0], Kp_ROLLPITCH * Accel_weight);

    vector_scale(&Scaled_Omega_I[0], &errorRollPitch[0], Ki_ROLLPITCH * Accel_weight);
    vector_add(Omega_I, Omega_I, Scaled_Omega_I);

    //*****YAW***************
    // we make the gyro YAW drift correction based on compass magnetic heading

    mag_heading_x = cos(MAG_Heading);
    mag_heading_y = sin(MAG_Heading);

    errorCourse = (DCM_Matrix[0][0] * mag_heading_y) - (DCM_Matrix[1][0] * mag_heading_x);  // Calculating YAW error
    vector_scale(errorYaw, &DCM_Matrix[2][0], errorCourse);  // Applys the yaw correction to the XYZ rotation of the aircraft, depeding the position

    vector_scale(&Scaled_Omega_P[0], &errorYaw[0], Kp_YAW);  // .01 proportional of YAW.
    vector_add(Omega_P, Omega_P, Scaled_Omega_P);  //Adding  Proportional.

    vector_scale(&Scaled_Omega_I[0], &errorYaw[0], Ki_YAW); // .00001 Integrator
    vector_add(Omega_I, Omega_I, Scaled_Omega_I);  //adding integrator to the Omega_I

} // drift_correction

// ------------------------------------------------------------------------------------------------
/* void
dcm_accel_adjust(void)
{
    Accel_Vector[1] += Accel_Scale(speed_3d * Omega[2]);  // Centrifugal force on Acc_y = GPS_speed * GyroZ
    Accel_Vector[2] -= Accel_Scale(speed_3d * Omega[1]);  // Centrifugal force on Acc_z = GPS_speed * GyroY

} // accel_adjust */

// ------------------------------------------------------------------------------------------------
void
dcm_matrix_update(void)
{
    Gyro_Vector[0] = Gyro_Scaled_X(gyro_x);  // gyro x roll
    Gyro_Vector[1] = Gyro_Scaled_Y(gyro_y);  // gyro y pitch
    Gyro_Vector[2] = Gyro_Scaled_Z(gyro_z);  // gyro Z yaw

    Accel_Vector[0] = accel_x;
    Accel_Vector[1] = accel_y;
    Accel_Vector[2] = accel_z;

    vector_add(&Omega[0], &Gyro_Vector[0], &Omega_I[0]);   // adding proportional term
    vector_add(&Omega_Vector[0], &Omega[0], &Omega_P[0]);  // adding Integrator term

    // accel_adjust();  // remove centrifugal acceleration. We are not using this function in this version - we have no speed measurement

    #if OUTPUTMODE==1
    Update_Matrix[0][0] = 0;
    Update_Matrix[0][1] = -G_Dt * Omega_Vector[2]; // -z
    Update_Matrix[0][2] =  G_Dt * Omega_Vector[1]; // y
    Update_Matrix[1][0] =  G_Dt * Omega_Vector[2]; // z
    Update_Matrix[1][1] = 0;
    Update_Matrix[1][2] = -G_Dt * Omega_Vector[0]; // -x
    Update_Matrix[2][0] = -G_Dt * Omega_Vector[1]; // -y
    Update_Matrix[2][1] =  G_Dt * Omega_Vector[0]; // x
    Update_Matrix[2][2] = 0;
    #else  // Uncorrected data (no drift correction)
    Update_Matrix[0][0] = 0;
    Update_Matrix[0][1] = -G_Dt * Gyro_Vector[2]; // -z
    Update_Matrix[0][2] =  G_Dt * Gyro_Vector[1]; // y
    Update_Matrix[1][0] =  G_Dt * Gyro_Vector[2]; // z
    Update_Matrix[1][1] = 0;
    Update_Matrix[1][2] = -G_Dt * Gyro_Vector[0];
    Update_Matrix[2][0] = -G_Dt * Gyro_Vector[1];
    Update_Matrix[2][1] =  G_Dt * Gyro_Vector[0];
    Update_Matrix[2][2] = 0;
    #endif // OUTPUTMODE

    matrix_multiply(DCM_Matrix, Update_Matrix, Temporary_Matrix); // a * b = c

    for (int x = 0; x < 3; x++)  // matrix addition (update)
        for (int y = 0; y < 3; y++)
            DCM_Matrix[x][y] += Temporary_Matrix[x][y];

} // matrix_update

// ------------------------------------------------------------------------------------------------
void
dcm_euler_angles(void)
{
    pitch = -asin(DCM_Matrix[2][0]);
    roll  = atan2(DCM_Matrix[2][1], DCM_Matrix[2][2]);
    yaw   = atan2(DCM_Matrix[1][0], DCM_Matrix[0][0]);

} // euler_angles

// < the end >-------------------------------------------------------------------------------------
