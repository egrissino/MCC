
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
MfcSlice_t getCurve (MfcSet_t set, base2 s)
{
    MfcSlice_t slice;
    base count = 0;
    for (base x = 0; x < MAX_BASE; x++)
    {
        for (base y = 0; y < MAX_BASE; y++)
        {
            if ((&set.Y[x])[y] == s)
            {
                count++;
            } 
        }
    }
    slice.size = count;
    slice.X = malloc( sizeof(Point_t) * count );
    base idx = 0;
    Point_t* p;
    for (base x = 0; x < MAX_BASE; x++)
    {
        for (base y = 0; y < MAX_BASE; y++)
        {
            if ((&set.Y[x])[y] == s)
            {
                p = &slice.X[idx];
                p->X[0] = x;
                p->X[1] = y;               
            } 
        }
    }
    return slice;
}

MfcSet_t getCurveSet (Mfc_t curve)
{
    MfcSet_t set;
    set.curve = curve;
    set.Y = malloc ( pow(MAX_BASE, 2) );

    Point_t p;
    for (base x = 0; x < MAX_BASE; x++)
    {
        for (base y = 0; y < MAX_BASE; y++)
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

int writeCurveToFile (const char* filename, MfcSlice_t slice)
{
    FILE* outfile = fopen (filename, "w");

    if (!outfile)
    {
        return -1;
    }

    for (int i = 0; i < slice.size; i++)
    {
        fprintf (outfile, "%d,%d\n", slice.X[i].X[0], slice.X[i].X[1]);
    }

    fclose (outfile);
    return 0;
}

int writeCurveSetToFile (const char* filename, MfcSet_t set)
{
    FILE* outfile = fopen (filename, "w");

    if (!outfile)
    {
        return -1;
    }

    for (int x = 0; x < MAX_BASE; x++)
    {
        for (int y = 0; y < MAX_BASE; y++)
        {
            fprintf(outfile, "%d,%d,%d\n", x, y, (&set.Y[x])[y]);
        }
    }

    fclose (outfile);
    return 0;
}