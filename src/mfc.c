
/* A set of Curves is defined by the Foci. Each set is composed of infinitely many curves of constant distance summation */

#include <mfc.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>

/* Utility */
Point_t centroid (Mfc_t curve)
{
    Point_t p;
    for (int i = 0; i < NUM_DIM; i++)
    {
        base sum = 0;
        for (int j = 0; j < NUM_FOCI; j++)
        {
            sum += curve.foci[j].X[i];
        }
        p.X[i] = (sum / NUM_FOCI);
    }
    return p;
}

base getDistance (Point_t a, Point_t b)
{
    base2 distSqr = 0;
    for (int i = 0; i < NUM_DIM; i++)
    {
        distSqr += (a.X[i] - b.X[i]) * (a.X[i] - b.X[i]);
    }
    return sqrt (distSqr);
}

base2 getDistanceSum (Mfc_t curve, Point_t p)
{
    base2 sum = 0;
    for (int i = 0; i < NUM_FOCI; i++)
    {
        sum += getDistance (curve.foci[i], p);
    }
    return sum;
}

/* Solutions */
void getCurve (MfcSet_t set, base2 s)
{
    base2 max = (1 << sizeof(base));
    base count = 0;
    for (base x = 0; x < max; x++)
    {
        for (base y = 0; y < max; y++)
        {
            if ((&set.Y[x])[y] == s)
            {
                count++;
            } 
        }
    }

    set.curve.X = malloc( sizeof(Point_t) * count );
    base idx = 0;
    Point_t* p;
    for (base x = 0; x < max; x++)
    {
        for (base y = 0; y < max; y++)
        {
            if ((&set.Y[x])[y] == s)
            {
                p = &set.curve.X[idx];
                p->X[0] = x;
                p->X[1] = y;               
            } 
        }
    }

}

MfcSet_t getCurveSet (Mfc_t curve)
{
    base max = (1 << (sizeof(base)*8));
    MfcSet_t set;
    set.curve = curve;
    set.Y = malloc ( pow(max, 2) );

    Point_t p;
    for (base x = 0; x < max; x++)
    {
        for (base y = 0; y < max; y++)
        {
            p.X[0] = x;
            p.X[1] = y;
            (&set.Y[x])[y] = getDistanceSum (curve, p);
        }
    }
    return set;
}

/* Output */
void printPoint (Point_t p)
{
    printf("(%d", p.X[0]);
    for (int j = 1; j < NUM_DIM; j++)
    {
        printf(", %d", p.X[j]);
    }
    printf (")\n");
}

void writeToFile (const char* filename, MfcSet_t set)
{

}