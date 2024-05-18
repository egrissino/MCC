
#include <stdio.h>
#include <stdint.h>
#include <mfc.h>
#include <string.h>
#include <stdlib.h>

int main (int argc, char** argv)
{

    printf ("Multi-Focal Curves\n");
    
    Mfc_t curve1;
    curve1.numFoci = NUM_FOCI;
    curve1.foci = malloc (sizeof(Point_t) * NUM_FOCI);

    curve1.foci[0] = (Point_t){134, 23};
    curve1.foci[1] = (Point_t){98, 206};
    curve1.foci[2] = (Point_t){49, 182};
    
    curve1.C = centroid (curve1);

    printf ("Centroid: \n");
    printPoint (curve1.C);
    base2 minDist = getDistanceSum (curve1, curve1.C);
    printf ("Min Dist: %d\n", minDist);

    printPoint (curve1.foci[0]);
    printPoint (curve1.foci[1]);
    printPoint (curve1.foci[2]);

    getCurve (curve1, minDist + 2);

    MfcSet_t set = getCurveSet (curve1);

    // /* Cleanup */
    free (curve1.foci);
    free (set.Y);
}
