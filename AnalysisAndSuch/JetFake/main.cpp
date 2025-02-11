//TO COMPILE:   g++ `root-config --cflags --libs` -o main main.cpp `root-config --libs` `root-config --cflags`
#include <iostream>
#include <string>
#include <complex>

#include "TCanvas.h"
#include "TChain.h"


#include "TROOT.h"
#include "TClonesArray.h"
#include "TRint.h"
#include "TH1F.h"
#include "TH2F.h"
#include "TF1.h"
#include "TF2.h"
#include "TCanvas.h"
#include "TChain.h"
// #include "observables.h"
#include "TMath.h"
#include "TFile.h"
#include "TSystem.h"
#include "TGStatusBar.h"
#include "TSystem.h"
// #include "TXMLEngine.h"
#include "TTree.h"
#include "classes/DelphesClasses.h"
#include "ExRootClasses.h"
#include "ExRootClassifier.h"

#include "ExRootFactory.h"
#include "ExRootFilter.h"
#include "ExRootLHEFReader.h"


#include "ExRootProgressBar.h"
#include "ExRootResult.h"
//#include "ExRootSTDHEPReader.h"
//#include "ExRootStream.h"

#include "ExRootTreeBranch.h"
#include "ExRootTreeReader.h"
#include "ExRootTreeWriter.h"
#include "ExRootUtilities.h"

// #include "fastjet/PseudoJet.hh"
// #include "fastjet/JetDefinition.hh"
// #include "fastjet/ClusterSequence.hh"


// #include "classes/DelphesClasses.h"

//#include <random>
#include <cstdlib>
#include <time.h>
#include <unistd.h>
#include <iterator>
#include<stdio.h>
#include "TRandom3.h"


using namespace std;
using namespace TMath;
// using namespace fastjet;

#include "observables.h"
#include "ran.h"
#include "ChargeFlip.h"

// #include "mt2_bisect.h"
// #include "mt2w_bisect.h"

bool VERBOSE = false; // Allows for some troubleshooting or extra detail if true.
bool lowlepcut = false; //turns on and off Some sort of cut on the low energy lepton?????????????????????????

// const char* EventType = "W3j";

// For the simplification of simulated data in early stages,
// we do not have branches for MET nor Muons. The following Bools are to account for this. 
// When we use data that has MET and Muons, then we set these to true and it'll function properly 
// Used in lines 147-149, 234-237
bool hasMET = false;
bool hasMu = false;
// This is used if we want to post-simulate the LFV with ratios from CMS paper (true) or just leave as single flavor (false)
bool simLFV = true;

void Export_TH1F (TH1F * target_H1F, ofstream &out_file){
    double num_entries = target_H1F->GetEntries();
    for( int i = 1; i <= target_H1F->GetNbinsX(); i++){
        out_file<<target_H1F->GetXaxis()->GetBinCenter(i)<<" "<<(target_H1F->GetBinContent(i)/num_entries)<<endl;
    }//return normalized histogram
}


Bool Below_DeltaR_Same(vector<PseudoJet> par, double delta_R_min);
Bool Below_DeltaR_Same(vector<PseudoJet> par, double delta_R_min){
    if(par.size() < 2){
        return false;
    }
    else {
        for(int i=0; i<par.size()-1; i++){
            for (int j=i+1; j<par.size(); j++) {
                if( par[i].delta_R(par[j]) < delta_R_min ) return true;
            }
        }
    }
    return false;
}

Bool Below_DeltaR_Diff(vector<PseudoJet> par1, vector<PseudoJet> par2, double delta_R_min);
Bool Below_DeltaR_Diff(vector<PseudoJet> par1, vector<PseudoJet> par2, double delta_R_min){
    if(par1.size()==0 || par2.size()==0) {
        return false;
    }
    else {
        for(int i=0; i<par1.size(); i++){
            for (int j=0; j<par2.size(); j++) {
                if( par1[i].delta_R(par2[j]) < delta_R_min ) return true;
            }
        }
    }
    return false;
}

Bool PreselectionCuts(vector<PseudoJet> leptons, int *removalCounts) // This function intakes the vector of all charged leptons already sorted by pt
{ //This function returns true if the event should be kept. This function returns false if the event should be rejected.
    // shouldKeep=true;
    //First cut: remove high P_t 3rd leptons
    if (leptons.size()>2)
    {
        if (leptons[2].pt() > 10) 
        {
            // shouldKeep=false;
            (*removalCounts)++; // this increments the element corresponding to the passed address -- Cut 1a
            return false;
        }
    }
    //Second cut: remove if leading lep pair has low inv. mass
    else if((leptons[0]+leptons[1]).m()<10)
    {
        (*(removalCounts+1))++; // This increments the element corresponding to the one after the passed address -- Cut 1b
        return false;
    } 

    //Third cut: is inv. mass of leading leptons near M_Z?
    else if (abs((leptons[0]+leptons[1]).m() - 91.2) < 20)
    {
        (*(removalCounts+2))++; // same but the one after the the one after the one passed -- Cut 1c
        return false;
    }

    return true;

}

vector<PseudoJet> WPairing(vector<PseudoJet> Jets, double LowDiff=1000)
{
    // For the next part, I need to find Δm_Wj which is the inv mass of
    // the pair of jets with inv mass closes to M_W
    int JLowPairInd[2] = {0,0};
    // double LowDiff = 1000;
    // cout << all_jets.size()<< endl;
    for(int j1=0; j1<Jets.size(); j1++)
    {
        for(int j2=j1; j2<Jets.size(); j2++)
        {
            // cout << "Current Pair (" << j1 << "," << j2<< ")"<< endl;
            double thisDiff = abs((Jets[j1]+Jets[j2]).m()-80.4);
            // cout << "Inv M is off from W by " << thisDiff << endl;
            // cout << "Low diff: " << LowDiff << endl;
            if (thisDiff < LowDiff)
            {
                LowDiff = thisDiff;
                JLowPairInd[0] = j1;
                JLowPairInd[1] = j2;
            }
            else continue;
        }
    }
    vector<PseudoJet> W_pair;
    W_pair.push_back(Jets[JLowPairInd[0]]);
    W_pair.push_back(Jets[JLowPairInd[1]]);
    return W_pair;
}

Bool HMSR1Cuts(vector<PseudoJet> leptons, vector<PseudoJet> Jets, vector<PseudoJet> MET, bool has_MET, int *removalCounts)
{
    // The proceeding three cuts are the definition of High Mass Signal Region 1 (HM SR1)
            // CMS Table 1
            // Each jet must be above 25 GeV pt
            int numJet2 = Jets.size();
            // if (VERBOSE) cout << "Is the length of jet vector the same as branch size? " << (numJet2 == numJet)<< endl;
            int htsum = 0;
            if (Jets[0].pt()<=25) 
            {
                (*removalCounts)++; // this increments the element corresponding to the passed address  -- Cut 2a
                return false;
            }
            // cout << "Here"<< endl;
            for (int i=0; i < numJet2; i++)
            {
                double this_pt = Jets[i].pt();
                htsum += this_pt;
                // if( this_pt < 25) continue;
            }

            for (int j=0; j < leptons.size(); j++)
            {
                htsum += leptons[j].pt();
            }
            // Ratio of missing Trans. momentum^2 and total PT less than 15 GeV
            if (has_MET)
            {
                // cout << v_MET.size()<< endl;
                if (pow(MET[0].pt(),2)/htsum > 15)
                {
                    (*(removalCounts+1))++; // this increments the element corresponding to the passed address  -- Cut 2b
                    return false;
                }
            }
            // For the next part, I need to find Δm_Wj which is the inv mass of
            // the pair of jets with inv mass closes to M_W
            // int JLowPairInd[2] = {0,0};
            // double LowDiff = 1000;
            // // cout << all_jets.size()<< endl;
            // for(int j1=0; j1<Jets.size(); j1++)
            // {
            //     for(int j2=j1; j2<Jets.size(); j2++)
            //     {
            //         // cout << "Current Pair (" << j1 << "," << j2<< ")"<< endl;
            //         double thisDiff = abs((Jets[j1]+Jets[j2]).m()-80.4);
            //         // cout << "Inv M is off from W by " << thisDiff << endl;
            //         // cout << "Low diff: " << LowDiff << endl;
            //         if (thisDiff < LowDiff)
            //         {
            //             LowDiff = thisDiff;
            //             JLowPairInd[0] = j1;
            //             JLowPairInd[1] = j2;
            //         }
            //         else continue;
            //     }
            // }
            // // if (!JLowPairInd[0] && !JLowPairInd[1])
            // // {
            // //     cout << "For some reason, I couldn't pick a smallest"<< endl;
            // // }
            // w_jet_pairs.push_back(Jets[JLowPairInd[0]]);
            // w_jet_pairs.push_back(Jets[JLowPairInd[1]]);
            vector<PseudoJet> w_jet_pairs = WPairing(Jets);
            double M_Wj = (w_jet_pairs[0]+w_jet_pairs[1]).m();
            if (M_Wj < 30 || M_Wj > 150) 
            {
                return false;
                (*(removalCounts+2))++; // this increments the element corresponding to the passed address   -- Cut 2c
            }
            else return true;
            return true;
}

double WhatToPlot(TH1F *Hist, int Params[3], double value)
{
    double HalfbWidth = (Params[2]-Params[1])/(2*Params[0]);
    if (value>Params[2]) return Params[2]-HalfbWidth;
    else return value;
}


/*
Hello, 
This code is meant to isolate a dilepton dijet Lepton Number Violating process from the inputted
data. The purpose is to get rid of mostly jet fakes and diboson backgrounds. In commenting
the cuts made, I will reference https://arxiv.org/abs/1806.10905 
Search for heavy Majorana neutrinos in same-sign dilepton channels in proton-proton collisions at √s= 13 TeV.
Which was done by CMS collaboration. The idea of this code is to mostly replicate the analysis that they did on
experimental data. So any reference to CMS Sections or tables etc. are references to that paper.
EXPECTS:
<path>/main <eventType> <file1> <file2> etc
*/



int main(int argc, const char * argv[])
{
    
    //Pulls and arranges data as needed.
    TChain chain("Delphes");

    const char* EventType = argv[1];
    cout << EventType<< endl;

    const char eTypes[5][10] = {"LNVF", "WZ2j", "ZZ2j", "W3j", "ttbar"};

    bool type_listed = false;
    for(int t=0; t<5; t++)
    {
        cout << EventType << endl;
        cout << eTypes[t] << endl;
        if (!strcmp(EventType,eTypes[t]))
        {
            type_listed = true;
        }
        cout << type_listed << endl;
    }

    if (not type_listed)
    {
        cout << "Improper format. Please use the following format: "<< endl;
        cout<< "<path to analysis>/main <event type> <paths to files separated by spaces>"<<endl;
        cout << "where event types can be ";
        for (int type = 0; type<5; type++)
        {
            cout << eTypes[type]<< ", "<< endl;
        }
        return 0;
    }

    for(int i=2; i<argc; i++)
    {
        chain.Add(argv[i]);
        cout << argv[i]<< endl;
    }

    ExRootTreeReader *treeReader = new ExRootTreeReader(&chain);
    Long64_t NumEntries = treeReader->GetEntries();
    cout << "There are "<< NumEntries <<" Entries." <<endl;
    TClonesArray *branchJet = treeReader->UseBranch("Jet"); 
    TClonesArray *branchElectron = treeReader->UseBranch("Electron");
    TClonesArray *branchMuon;
    if (hasMu) branchMuon = treeReader->UseBranch("Muon");
    TClonesArray *branchMET;
    if (hasMET) branchMET = treeReader->UseBranch("MissingET");

    // TTreeReader *treeReader = new TTreeReader(&chain);
    // Long64_t NumEntries = treeReader->GetEntries();
    // cout << "There are "<< NumEntries <<" Entries." <<endl;
    // TClonesArray *branchJet = treeReader->UseBranch("Jet"); 
    // TClonesArray *branchElectron = treeReader->UseBranch("Electron");
    // TClonesArray *branchMuon;
    // if (hasMu) branchMuon = treeReader->UseBranch("Muon");
    // TClonesArray *branchMET;
    // if (hasMET) branchMET = treeReader->UseBranch("MET");



    TRootLHEFEvent *event;
    TRootLHEFParticle *particle;

    vector <PseudoJet> all_jets, w_jet_pairs; // all_jets = f_all_jets and w_jet_pairs = f_w_jet from Gang's main.cpp
    vector <PseudoJet> v_eM, v_eP, v_muM, v_muP, v_lep, v_e, v_mu, v_lepP, v_lepM;
    vector <PseudoJet> v_MET, b_jets;

    // all_jets = a vector with the every jet object for each entry
    // w_jet_pairs = a vector with pairs of jets that have inv. mass ~ M_W for each entry
    // v_... = {e=electron, mu=muon, P=Plus/+, M=Minus/-, lep=any lepton}
    //v_MET = vector for the Missing transverse energy
    // b_jets = vector of b-tagged jets. 

    MissingET *met;
    Jet *jet;

    int numFlippede = 0;
    int numFlippedmu = 0;

    // HISTOGRAMS---------------------------------------
    //                                                                  , bins, xlow, xhigh)
    // Obj. name; Vert. axis vs. Horiz. axis; images produced by this
    //Invariant mass of the pair of jets closest to W mass -- Hereonout called W jets or W jet pair
    int scaleFactor = (EventType=="LNVF") ? 3: 1;
    // cout << "SCALE FACTOR" << scaleFactor << endl;
    // float scaleFactor2 = (EventType=="O2") ? 1.5 : 1;
    int MW2jHistoParams[3] = {50, 0, 140};
    TH1F *MW2j = new TH1F("Inv_Mass_2Jets_close_to_W", "Inv. Mass 2 Jets", MW2jHistoParams[0], MW2jHistoParams[1], MW2jHistoParams[2]);
    
    // Invariant mass of W jet pair and leading leptons (Are these necessarily going to be s.s. leptons?)
    int MW2j2lHistoParams[3] = {18,0, 660}; // current bounds are to have the same range and bin sizes as Gang's data
    TH1F *MW2j2l = new TH1F("Inv_Mass_2Jets_close_to_W_2l", "Inv. Mass 2 Jets 2 Lep",  MW2j2lHistoParams[0]-5, MW2j2lHistoParams[1], MW2j2lHistoParams[2]);

    //Invariant mass of the leading leptons (Are these necessarily going to be s.s. leptons?)
    int M2lHistoParams[3] = {80, 0, 1100};
    TH1F *M2l;
    if (lowlepcut)  M2l = new TH1F("Inv_Mass_2l", "Inv. Mass 2 Lep above 1GeV",  M2lHistoParams[0], M2lHistoParams[1], M2lHistoParams[2]);
    else M2l = new TH1F("Inv_Mass_2l", "Inv. Mass 2 Lep", M2lHistoParams[0], M2lHistoParams[1], M2lHistoParams[2]);

    //Invariant mass of W jets and leading lepton
    int MW2j1l_0HistoParams[3] = {25, 0, 480};
    // cout << "SF: "<< scaleFactor<< endl;
    // cout << "SF2: " << scaleFactor2<< endl;
    TH1F *MW2j1l_0 = new TH1F("Inv_Mass_2Jets_close_to_W_1l_0", "Inv. Mass 2 Jets + Lep_0", MW2j1l_0HistoParams[0], MW2j1l_0HistoParams[1], MW2j1l_0HistoParams[2]);

    //Invariant mass of W jets and the sub-leading lepton
    int MW2j1l_1HistoParams[3] = {19, 0, 350};
    TH1F *MW2j1l_1  = new TH1F("Inv_Mass_2Jets_close_to_W_1l_1", "Inv. Mass 2 Jets + Lep_1", MW2j1l_1HistoParams[0], MW2j1l_1HistoParams[1], MW2j1l_1HistoParams[2]);
    cout << MW2j2lHistoParams[2]<< endl;
    // TH1F *M2lTroubleshoot = new TH1F("Inv_Mass_2l", "Inv. Mass 2 Lep",  70, 0, 10);

// Figure out how to best use this later based on how I do the cuts
    //    // event counts after each cut
    // vector<int> cntCuts;
    // cntCuts.clear();
    /*
    The four cuts are as follows:
    cut 0: signal definition -- dilepton + dijet
    cut 1: preselection -- ?
    cut 2: HMSR1 -- ?
    cut 3: Misc. -- ?
    numCutCats below counts how many events pass each cut. 
    */
    // int numCutCats[4] = {0, 0, 0, 0}; //events that pass 0: signal def, 1: preselection, 2: HMSR1, 3: Misc.
    vector<int> numCutCats = {0, 0, 0, 0};
    vector<int> deepCuts = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0}; // events that get removed by each cut. 1a-b, 2a-b, 3a-b
    vector<int> deepCuts2 = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0}; // in Gang's order
    vector<int> GangCutCount = {0,0,0,0,0};
    // double cutsSize = sizeof(numCutCats)/sizeof(int);
    cout << "num cuts " << numCutCats.size() << endl;
    for (int c=0; c<numCutCats.size(); c++) cout << numCutCats[c]<< endl;
    // cout << sizeof(numCutCats)<< endl;
    // for (int i=0; i<sizeof(numCutCats)/sizeof(int); i++) cout << numCutCats[i] << ", ";
    // cout << endl;
    // Okay, so all I want to do to start is to write the cut that 
    // Compares pairs of Jets to W boson mass

    if (NumEntries ==0) {

      cout<<"  ------------------  "<<endl;
      cout<<"  no event analyzed  "<<endl;
      cout<<"  ------------------  "<<endl;
    }

    else
    {
        cout << "Loading Events ..." << endl;
        if(VERBOSE) cout <<"There are "<<  NumEntries << " Entries." << endl;

        // Is there a reason to use Int_t as opposed to int
        for(int entry=0; entry < NumEntries; entry++)
        {
            // if (VERBOSE) cout<< "I am on Entry " << entry<< endl;
            all_jets.clear();
            w_jet_pairs.clear();
            v_eM.clear();
            v_eP.clear();
            v_e.clear();
            v_mu.clear();
            v_muP.clear();
            v_muM.clear();
            v_lep.clear();
            v_lepP.clear();
            v_lepM.clear();
            v_MET.clear();
            b_jets.clear();

            // cout << "cleared vectors"<< endl;
            treeReader->ReadEntry(entry);
            int numJet = branchJet->GetEntries();
            int numEl = branchElectron->GetEntries();
            int numMu;
            int numMET; 
            if(hasMu) numMu = branchMuon->GetEntries(); 
            else numMu = 0;
            if(hasMET) numMET = branchMET->GetEntries();
            else 
            {
                numMET = 0;
                PseudoJet TEMP_event;
                TEMP_event.reset(0, 0, 0, 0);
                v_MET.push_back(TEMP_event);
            }
            if (VERBOSE) cout << "Muons" << numMu << endl;
            //I should diagram the rest of this out
            // I want to determine the pairs of jets that are closest to W mass

            // The following loops collects the data as PsuedoJet objects and organizes them in the
            // pre-defined vectors
            PseudoJet tempEvent;
            for(int jt=0; jt < numJet; jt++)
            {
                Jet *jettmp = (Jet *) branchJet->At(jt);
                //for some reason this .reset() causes it not to compile
                tempEvent.reset((jettmp->P4()).Px(), (jettmp->P4()).Py(), (jettmp->P4()).Pz(), (jettmp->P4()).E());
                // cout << jettmp->BTag << endl;
                if(jettmp->BTag == 1) b_jets.push_back(tempEvent);
                all_jets.push_back(tempEvent);
                // cout << "added a jet"<< endl;
            }
            
            //Time to collect some leptons
            //Electrons
            // cout << "Bout to make electrons"<< endl;
            // if (VERBOSE) cout<< "numEl = " << numEl << endl;
            // if (numEl+numMu<2) continue;
            for(int e=0; e < numEl; e++)
            {
                Electron *etmp = (Electron *) branchElectron->At(e);
                tempEvent.reset((etmp->P4()).Px(), (etmp->P4()).Py(), (etmp->P4()).Pz(), (etmp->P4()).E());

                v_lep.push_back(tempEvent);
                v_e.push_back(tempEvent);
                //Charge flip check
                float rando = gRandom->Uniform();
                // PseudoJet this_lepP = v_lepP[l];
                float rate = ChargeFlipRate(etmp->Eta, etmp->PT);
                bool shouldFlip = false;
                if (rate > rando)
                {
                    // cout << "I should flip this electron "<< endl;
                    // cout << "rate: " << rate << " sample: " << rando<< endl;
                    // if (etmp->Charge ==1) cout << "+" << endl;
                    shouldFlip = true;
                    numFlippede++;
                }
                
                if ((etmp->Charge == 1 && !(shouldFlip))||(etmp->Charge==-1 && shouldFlip)) 
                {
                    v_eP.push_back(tempEvent); // Positive 
                    v_lepP.push_back(tempEvent);
                }
                else 
                {
                    v_eM.push_back(tempEvent); // Negative
                    v_lepM.push_back(tempEvent);
                }

            }
            //Muons
            // cout << "bout to make muons"<< endl;
            // if (VERBOSE) cout<< "numMu = " << numMu << endl;

            for(int m=0; m < numMu; m++)
            {
                Muon *mutmp = (Muon *) branchMuon->At(m);
                tempEvent.reset((mutmp->P4()).Px(), (mutmp->P4()).Py(), (mutmp->P4()).Pz(), (mutmp->P4()).E());
                cout << "DOING MUONSSSSSSSSSSS" << endl;
                v_lep.push_back(tempEvent);
                v_mu.push_back(tempEvent);
                if (mutmp->Charge == 1) 
                {
                    v_muP.push_back(tempEvent); // Positive 
                    v_lepP.push_back(tempEvent);
                }
                else
                {
                    v_muM.push_back(tempEvent); // Negative
                    v_lepM.push_back(tempEvent);
                }

            }
            if (v_mu.size()>0) cout << "Muons: " << v_mu.size() << endl;
            // cout << "i'm about to sort vectors" << endl;
            sort(v_lep.begin(), v_lep.end(), sort_by_pt());
            sort(v_lepP.begin(), v_lepP.end(), sort_by_pt());
            sort(v_lepM.begin(), v_lepM.end(), sort_by_pt());
            sort(v_eM.begin(), v_eM.end(), sort_by_pt());
            sort(v_eP.begin(), v_eP.end(), sort_by_pt());
            sort(v_muM.begin(), v_muM.end(), sort_by_pt());
            sort(v_muP.begin(), v_muP.end(), sort_by_pt());
            sort(v_e.begin(), v_e.end(), sort_by_pt());
            sort(v_mu.begin(), v_mu.end(), sort_by_pt());
            // cout << "I made it past the making of vectors"<< endl;
            // Signal definition
            deepCuts2[0]++;
            // Gang's ordering
            //cut 0
            if (Below_DeltaR_Diff(v_lep, all_jets, 0.4) || (Below_DeltaR_Same(v_lep, 0.4)) || (Below_DeltaR_Same(all_jets, 0.4)))
            {
                // deepCuts2[0]++; // Cut 3a
                continue;
            }
            deepCuts2[1]++;

            GangCutCount[0]++;

            if (v_lepP.size() < 2 && v_lepM.size() < 2) 
            {
                // deepCuts2[1]++;

                continue;
                // if (VERBOSE) cout << "No s.s. dilepton pair"<< endl;
                // else
            } 
            deepCuts2[2]++;
            
            if ((v_lep[0]+v_lep[1]).m() < 10.0) continue;
            deepCuts2[3]++;

            double r1 = 0.18;
            double r2 = 0.31;
            int lPairType = 0;
            if (hasMu)
            {
                // if (v_mu[])
                if (abs(v_lep[0].m() - 0.511*pow(10, 3)) < 0.01) // is 0.01 a good cut off for being an electron?
                {
                    if (abs(v_lep[1].m() - 0.511*pow(10,3)) < 0.01) lPairType = 0;
                    else lPairType = 1;
                }
                else
                {
                    if (abs(v_lep[1].m() - 0.511*pow(10,3)) < 0.01) lPairType = 1;
                    else lPairType = 2; 
                }
            }
            else if (simLFV)
            {
                double rs = gRandom->Uniform(); // random number 0-1
                if (rs < r1) lPairType = 0; // 0-0.18 => ee
                else lPairType = (r2 < rs) ? 1 : 2; // 0.18-0.31 =>μμ, 0.31-1 => eμ
            }
            //    CMS Section 5 paragraph 1. Trigger simulation
            int leadingThresh[3] = {25, 25, 20}; // GeV; corresponds to lPairType 0,1,2 indices
            int trailingThresh[3] = {15, 10, 10};
            if ((v_lep[0].pt() < leadingThresh[lPairType] || v_lep[1].pt() < trailingThresh[lPairType])) // Double check that the logical statements here match up w Gang
            {
                // deepCuts[3]++; //Cut 3c
                continue;
            }
            deepCuts2[4]++;
                // Gang only has the near Z mass cut for ee type, but not the others...?

            if(v_lep.size()>2)
            {
                // deepCuts2[4]
                if(v_lep[2].pt()>10) continue;
            }
            GangCutCount[1]++;
            deepCuts2[5]++;


            if (all_jets.size() <= 1) 
            {   
                // deepCuts[0]++;
                // if (VERBOSE)cout << "Not enough jets"<< endl;
                continue;
            }
            GangCutCount[2]++;
            deepCuts2[6]++;

            


            int htsum = 0;
            // if (Jets[0].pt()<=25) 
            // {
            //     (*removalCounts)++; // this increments the element corresponding to the passed address  -- Cut 2a
            //     return false;
            // }
            // cout << "Here"<< endl;
            for (int i=0; i < all_jets.size(); i++)
            {
                double this_pt = all_jets[i].pt();
                htsum += this_pt;
                // if( this_pt < 25) continue;
            }
            deepCuts2[7]++;

            if(b_jets.size()>0)
            {
                // deepCuts[9]++; // Cut 3b
                continue;
            }
            deepCuts2[8]++;

            for (int j=0; j < v_lep.size(); j++)
            {
                htsum += v_lep[j].pt();
            }
            // Ratio of missing Trans. momentum^2 and total PT less than 15 GeV
            if (hasMET)
            {
                // cout << v_MET.size()<< endl;
                if (pow(v_MET[0].pt(),2)/htsum > 15)
                {
                    // (*(removalCounts+1))++; // this increments the element corresponding to the passed address  -- Cut 2b
                    // return false;
                    continue;
                }
            }
            GangCutCount[3]++;
            deepCuts2[9]++;


            w_jet_pairs = WPairing(all_jets);

            double M_Wj = (w_jet_pairs[0]+w_jet_pairs[1]).m();
            if (M_Wj < 30 || M_Wj > 150) 
            {
                continue;
                // return false;
                // (*(removalCounts+2))++; // this increments the element corresponding to the passed address   -- Cut 2c
            }
            GangCutCount[4]++;
            deepCuts2[10]++;

            //HERE -----------------------------------------------------------
            //remove events with 1 or less jets
            // if (all_jets.size() <= 1) 
            // {   
            //     // deepCuts[0]++;
            //     // if (VERBOSE)cout << "Not enough jets"<< endl;
            //     continue;
            // }
            // int lPairType = 0; // ee->0, eμ -> 1, μμ -> 2
            // bool lPairPlus = false; // false: --, true: ++

            // // First make sure that there are s.s. dilep pairs
            // if (v_lepP.size() < 2 && v_lepM.size() < 2) 
            // {
            //     // deepCuts[1]++;

            //     continue;
            //     // if (VERBOSE) cout << "No s.s. dilepton pair"<< endl;
            //     // else
            // } 
            //TO HERE ------------------------------------------------------------
            // Here, I'm commenting out the part asking for any s.s. pairs and writing one that only asks for electron s s pairs
            //This is temporary. Change it later
            // if (v_eP.size() < 2 && v_eP.size() < 2)
            // {
            //     deepCuts[1]++;
            //     continue;
            // }
            // cout << "+: " << v_lepP.size() << endl;
            // cout << "-: " << v_lepM.size() << endl;
            // cout << "all: "<< v_lep.size() << endl;

            // if (VERBOSE) cout << "There is an s.s. dilepton pair"<< endl;
            // numCutCats[0]++;

            //All events that made it here should have s.s. dilepton pair and 2+ jets
            // Preselection Criteria: CMS Sec 5.1
// Preselection -----------------------------------------------------
            // if (!PreselectionCuts(v_lep, &deepCuts[2])) continue; // Preselection returns false if the event should be rejected.
            // numCutCats[1]++;
            
            // High Mass SR 1-------------------------------------------------------------------------------------------------------------------------
            // // The proceeding three cuts are the definition of High Mass Signal Region 1 (HM SR1)
            // // CMS Table 1
            // if (!HMSR1Cuts(v_lep, all_jets, v_MET, hasMET, &deepCuts[5])) continue;
            // w_jet_pairs = WPairing(all_jets);
            // // Each jet must be above 25 GeV pt
            // int numJet2 = all_jets.size();
            // // if (VERBOSE) cout << "Is the length of jet vector the same as branch size? " << (numJet2 == numJet)<< endl;
            // int htsum = 0;
            // if (all_jets[0].pt()<=25) continue;
            // // cout << "Here"<< endl;
            // for (int i=0; i < numJet2; i++)
            // {
            //     double this_pt = all_jets[i].pt();
            //     htsum += this_pt;
            //     // if( this_pt < 25) continue;
            // }

            // for (int j=0; j < v_lep.size(); j++)
            // {
            //     htsum += v_lep[j].pt();
            // }
            // // Ratio of missing Trans. momentum^2 and total PT less than 15 GeV
            // if (hasMET)
            // {
            //     // cout << v_MET.size()<< endl;
            //     if (pow(v_MET[0].pt(),2)/htsum > 15) continue;
            // }
            // // For the next part, I need to find Δm_Wj which is the inv mass of
            // // the pair of jets with inv mass closes to M_W
            // int JLowPairInd[2] = {0,0};
            // double LowDiff = 1000;
            // // cout << all_jets.size()<< endl;
            // for(int j1=0; j1<all_jets.size(); j1++)
            // {
            //     for(int j2=j1; j2<all_jets.size(); j2++)
            //     {
            //         // cout << "Current Pair (" << j1 << "," << j2<< ")"<< endl;
            //         double thisDiff = abs((all_jets[j1]+all_jets[j2]).m()-80.4);
            //         // cout << "Inv M is off from W by " << thisDiff << endl;
            //         // cout << "Low diff: " << LowDiff << endl;
            //         if (thisDiff < LowDiff)
            //         {
            //             LowDiff = thisDiff;
            //             JLowPairInd[0] = j1;
            //             JLowPairInd[1] = j2;
            //         }
            //         else continue;
            //     }
            // }
            // // if (!JLowPairInd[0] && !JLowPairInd[1])
            // // {
            // //     cout << "For some reason, I couldn't pick a smallest"<< endl;
            // // }
            // w_jet_pairs.push_back(all_jets[JLowPairInd[0]]);
            // w_jet_pairs.push_back(all_jets[JLowPairInd[1]]);
            // double M_Wj = (w_jet_pairs[0]+w_jet_pairs[1]).m();
            // if (M_Wj < 30 || M_Wj > 150) continue;

            // numCutCats[2]++;
            // We have concluded the HMSR1 cuts

            // Here come the Miscellaneous Cuts-------------------------------------------------------------------------------------------------------------------------
            // First, we want angularly well separated events
            // ΔR information from CMS Sec. 4.1 & 4.2
            // Uncommented these for trouble shooting. They should come back
            // bool rejectDeltaR = false;
            //HERE ------------------------------------------------------------------------------------------
        //     if (Below_DeltaR_Diff(v_lep, all_jets, 0.4) || (Below_DeltaR_Same(v_lep, 0.4)) || (Below_DeltaR_Same(all_jets, 0.4)))
        //     {
        //         // deepCuts[8]++; // Cut 3a
        //         continue;
        //     }

        //     //Now we remove all the B_tagged events (This doesn't seem to come from CMS paper)
        //     //Not sure why we are doing it.
        //     if(b_jets.size()>0)
        //     {
        //         // deepCuts[9]++; // Cut 3b
        //         continue;
        //     }

        //     /*
        //         Now We do a bit of a funky thing
        //         For now, we are not simulating any μ events. However according to CMS Sec 5 (paragraph 1)
        //         we want events with leptons at least loosely isolated. We use the "offline requirements".
        //         These requirements are different for ee, μμ, and eμ. 
        //         since we have no μ events, then we have to use ratios to split up ee events.
        //         I don't yet know where these ratios came from.
        //     */

        //    double r1 = 0.18;
        //    double r2 = 0.31;
        //    if (hasMu)
        //    {
        //         // if (v_mu[])
        //         if (abs(v_lep[0].m() - 0.511*pow(10, 3)) < 0.01) // is 0.01 a good cut off for being an electron?
        //         {
        //             if (abs(v_lep[1].m() - 0.511*pow(10,3)) < 0.01) lPairType = 0;
        //             else lPairType = 1;
        //         }
        //         else
        //         {
        //             if (abs(v_lep[1].m() - 0.511*pow(10,3)) < 0.01) lPairType = 1;
        //             else lPairType = 2; 
        //         }
        //    }
        //     else if (simLFV)
        //    {
        //         double rs = gRandom->Uniform(); // random number 0-1
        //         if (rs < r1) lPairType = 0; // 0-0.18 => ee
        //         else lPairType = (r2 < rs) ? 1 : 2; // 0.18-0.31 =>μμ, 0.31-1 => eμ
        //    }
        // //    CMS Section 5 paragraph 1. Trigger simulation
        //    int leadingThresh[3] = {25, 25, 20}; // GeV; corresponds to lPairType 0,1,2 indices
        //    int trailingThresh[3] = {15, 10, 10};
        //    if ((v_lep[0].pt() < leadingThresh[lPairType] || v_lep[1].pt() < trailingThresh[lPairType]))
        //    {
        //         // deepCuts[10]++; //Cut 3c
        //         continue;
        //    }
        //    numCutCats[3]++;
        //TO HERE --------------------------------------------------------------------------------------------

            
            // w_jet_pairs.push_back(all_jets[JLowPairInd[0]]);
            // w_jet_pairs.push_back(all_jets[JLowPairInd[1]]);
            if (VERBOSE) cout << "I'm filling the histograms now"<< endl;
            MW2j->Fill((w_jet_pairs[0]+w_jet_pairs[1]).m());
            MW2j2l->Fill((w_jet_pairs[0]+w_jet_pairs[1]+v_lep[0]+v_lep[1]).m());
            MW2j1l_0->Fill((w_jet_pairs[0]+w_jet_pairs[1]+v_lep[0]).m());
            MW2j1l_1->Fill((w_jet_pairs[0]+w_jet_pairs[1]+v_lep[1]).m());
            if (lowlepcut)
            {
                if ((v_lep[0]+v_lep[1]).m()>1) M2l->Fill((v_lep[0]+v_lep[1]).m());
            }
            else
            {
                M2l->Fill((v_lep[0]+v_lep[1]).m());
            }
            
            // TIME TO PLOT

            // cout << "num cuts " << cutsSize << endl;

            // return 0;
        }
        cout << "Histo time"<< endl;

        TStyle *st1 = new TStyle("st1","my style");
        cout << "hi"<< endl;
        st1->SetOptStat(111111111);
        cout << "707"<< endl;
        st1->cd();  //this becomes now the current style gStyle
        TCanvas *c1 = new TCanvas("c1", "ROOT Canvas", 900, 20, 540, 550);

        const char* ImagePath = "/work/pi_mjrm_umass_edu/LNV_collider/AnalysisOutput/";

        char FullPathM2jW[100] = "";
        char FullPathM2jW_root[100] = "";

        strcpy(FullPathM2jW, ImagePath);
        strcat(FullPathM2jW, EventType);
        strcat(FullPathM2jW_root, FullPathM2jW);
        strcat(FullPathM2jW, "/plots/Mass_2jW.png");
        strcat(FullPathM2jW_root, "/plots/Mass_2jW.root");
        // MW2j
        MW2j->GetXaxis()->SetTitle("GeV");
        MW2j->Draw();
        cout << "Made it. Gotta save it"<< endl;
        c1->SaveAs(FullPathM2jW);
        cout << "boutta save root file" <<endl;
        // cout << FullPathM2jW_root << endl;
        // c1->SaveAs(FullPathM2jW_root);
        TFile F1(FullPathM2jW_root, "RECREATE");
        MW2j->Write();
        F1.Close();

        cout << "Done Wj" << endl;

        char FullPathM2jW2l[100] = "";
        char FullPathM2jW2l_root[100] = "";

        strcpy(FullPathM2jW2l, ImagePath);
        strcat(FullPathM2jW2l, EventType);
        strcat(FullPathM2jW2l_root, FullPathM2jW2l);
        strcat(FullPathM2jW2l, "/plots/Mass_2jW2l.png");
        strcat(FullPathM2jW2l_root, "/plots/Mass_2jW2l.root");
        MW2j2l->GetXaxis()->SetTitle("GeV");
        MW2j2l->Draw();
        c1->SaveAs(FullPathM2jW2l);
        // c1->SaveAs(FullPathM2jW2l_root);
        TFile F2(FullPathM2jW2l_root, "RECREATE");
        MW2j2l->Write();
        F2.Close();
        cout << "Done both j both l" << endl;

        char FullPath2jW1l0[100] = "";
        char FullPath2jW1l0_root[100] = "";

        strcpy(FullPath2jW1l0, ImagePath);
        strcat(FullPath2jW1l0, EventType);
        strcat(FullPath2jW1l0_root, FullPath2jW1l0);
        strcat(FullPath2jW1l0, "/plots/Mass_2jW1l0.png");
        strcat(FullPath2jW1l0_root, "/plots/Mass_2jW1l0.root");
        // MW2j1l_0->SetOptStat(11111111111)
        MW2j1l_0->GetXaxis()->SetTitle("GeV");
        MW2j1l_0->Draw();
        c1->SaveAs(FullPath2jW1l0);
        // c1->SaveAs(FullPath2jW1l0_root);
        TFile F3(FullPath2jW1l0_root, "RECREATE");
        MW2j1l_0->Write();
        F3.Close();

        cout << "Done both j leading l" << endl;
        char FullPathMass_2jW1l1[100] = "";
        char FullPathMass_2jW1l1_root[100] = "";

        strcpy(FullPathMass_2jW1l1, ImagePath);
        strcat(FullPathMass_2jW1l1, EventType);
        strcat(FullPathMass_2jW1l1_root, FullPathMass_2jW1l1);
        strcat(FullPathMass_2jW1l1, "/plots/Mass_2jW1l1.png");
        strcat(FullPathMass_2jW1l1_root, "/plots/Mass_2jW1l1.root");
        MW2j1l_1->GetXaxis()->SetTitle("GeV");
        MW2j1l_1->Draw();
        c1->SaveAs(FullPathMass_2jW1l1);
        cout << FullPathMass_2jW1l1 << endl;
        // c1->SaveAs(FullPathMass_2jW1l1_root);
        TFile F4(FullPathMass_2jW1l1_root, "RECREATE");
        MW2j1l_1->Write();
        F4.Close();
        cout << "DOne both j subleadin l" <<endl;

        char FullPathMass_l2[100] = "";
        char FullPathMass_l2_root[100] = "";
        
        strcpy(FullPathMass_l2, ImagePath);
        strcat(FullPathMass_l2, EventType);
        strcat(FullPathMass_l2_root, FullPathMass_l2);

        M2l->GetXaxis()->SetTitle("GeV");
        M2l->Draw();

        strcat(FullPathMass_l2, "/plots/Mass_l2.png");
        strcat(FullPathMass_l2_root, "/plots/Mass_l2.root");
        c1->SaveAs(FullPathMass_l2);
        // c1->SaveAs(FullPathMass_l2_root);
        TFile F5(FullPathMass_l2_root, "RECREATE");
        M2l->Write();
        F5.Close();
        cout << "Done both l" << endl;

        cout << "I flipped this many electrons "<< numFlippede << endl;
        cout << "I flipped this many muons "<< numFlippedmu << endl; 

        // cout << "Events by Cut Group"<< endl;
        // cout << NumEntries << endl;
        // for (int c=0; c<numCutCats.size(); c++) cout << numCutCats[c]<< endl;

        // cout << "Events removed by Cut" << endl;
        // for (int r=0; r<deepCuts.size(); r++) cout << deepCuts[r] << endl;
        cout << "events removed by each ind. cut "<< endl;
        for(int d=0; d<deepCuts2.size(); d++) cout << deepCuts2[d]<< endl;
        cout << endl;

        cout <<"Events remaining after each cut group" << endl;
        for (int c=0; c<GangCutCount.size(); c++) cout << GangCutCount[c] << endl;
        
    }

}
