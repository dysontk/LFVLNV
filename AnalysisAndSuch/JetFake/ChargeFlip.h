#pragma once

#include <iostream>
#include <string> 
#include <complex>
#include <vector>

#include "TCanvas.h"
#include "TChain.h"
#include "TH1.h"
#include "TH2.h"
#include "TClonesArray.h"
#include "TStyle.h"



#include "ExRootTreeReader.h"

#include "fastjet/PseudoJet.hh"
#include "fastjet/JetDefinition.hh"
#include "fastjet/ClusterSequence.hh"

using namespace std;

float sigma_pT(float pt)
{
    float sigmas[16] = {0.000, 0.018, 0.020, 0.020,  0.017,  0.017,
    0.021, 0.025, 0.033, 0.041, 0.044, 0.057, 0.060, 0.081, 0.112, 1.000};

    int threshs[15] = {30, 34, 38, 43, 48, 55, 62, 69, 78, 88, 100, 115, 140, 200, 400};
    int index=15;
    
    int i = 0;
    while(pt>= threshs[i] && i < sizeof(threshs)/sizeof(int))
    {
        i++;
    }
    index=i;
    
    return sigmas[index];
}


float f_eta(float eta)
{
    float fs[19] = {0.000, 0.029, 0.041, 0.061,  0.093,  0.099,
    0.127, 0.160, 0.000, 0.320, 0.410, 0.630, 0.591, 0.692, 0.861, 0.980, 1.039, 1.496, 2.080};

    float threshs[18] = {0, 0.45, 0.7, 0.9, 1.0, 1.1, 1.2, 1.37, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0, 2.1,
    2.2, 2.3, 2.4};
    int index=15;
    
    int i = 0;
    while(eta>= threshs[i] && i < sizeof(threshs)/sizeof(int))
    {
        i++;
    }
    index=i;
    
    return fs[index];
}

Double_t ChargeFlipRate(Double_t LepEta, Double_t LepPT)
{
    return f_eta(LepEta) * sigma_pT(LepPT);
}