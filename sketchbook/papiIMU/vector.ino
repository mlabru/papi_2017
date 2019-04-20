// ------------------------------------------------------------------------------------------------
// computes the sum of two vectors
void
vector_add(float vectorOut[3], float vectorIn1[3], float vectorIn2[3])
{
    for (int iNdx = 0; iNdx < 3; iNdx++)
        vectorOut[iNdx] = vectorIn1[iNdx] + vectorIn2[iNdx];

} // vector_add

// ------------------------------------------------------------------------------------------------
// computes the cross product of two vectors
void
vector_cross_product(float vectorOut[3], float v1[3], float v2[3])
{
    vectorOut[0] = (v1[1] * v2[2]) - (v1[2] * v2[1]);
    vectorOut[1] = (v1[2] * v2[0]) - (v1[0] * v2[2]);
    vectorOut[2] = (v1[0] * v2[1]) - (v1[1] * v2[0]);

} // vector_cross_product

// ------------------------------------------------------------------------------------------------
// computes the dot product of two vectors
float
vector_dot_product(float vector1[3], float vector2[3])
{
    float op = 0;

    for (int iNdx = 0; iNdx < 3; iNdx++)
        op += vector1[iNdx] * vector2[iNdx];

    return op;

} // vector_dot_product

// ------------------------------------------------------------------------------------------------
// multiply the vector by a scalar
void
vector_scale(float vectorOut[3], float vectorIn[3], float scale2)
{
    for (int iNdx = 0; iNdx < 3; iNdx++)
        vectorOut[iNdx] = vectorIn[iNdx] * scale2;

} // vector_scale

// < the end >-------------------------------------------------------------------------------------
