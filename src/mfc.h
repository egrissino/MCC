/*
 * Multi Focal Curves
 *  Copyright GrissinoPublishing 2024
 *  Evan Grissino
 */

#pragma once

#include <stdint.h>
#include <math.h>

#define NUM_DIM 2
#define NUM_FOCI 3

typedef uint8_t base;
typedef uint16_t base2;

#define BASE_SIZE   (sizeof(base)*8)
#define MAX_BASE    (1 << BASE_SIZE)-1

typedef struct Point_s {
    base X[NUM_DIM];
} Point_t;

typedef struct Mfc_s {
    Point_t foci[NUM_FOCI];
    Point_t C;
} Mfc_t;

typedef struct MfcSlice_s {
    uint64_t size;
    Point_t* X;
} MfcSlice_t;

typedef struct MfcSet_s {
    Mfc_t curve;
    base2* Y;
} MfcSet_t;

void printPoint (Point_t p);

Point_t centroid (Mfc_t curve);

base getDistance (Point_t a, Point_t b);

base2 getDistanceSum (Mfc_t curve, Point_t p);

MfcSlice_t getCurve (MfcSet_t set, base2 s);

MfcSet_t getCurveSet (Mfc_t curve);

int writeCurveToFile (const char* filename, MfcSlice_t curve);

int writeCurveSetToFile (const char* filename, MfcSet_t set);
