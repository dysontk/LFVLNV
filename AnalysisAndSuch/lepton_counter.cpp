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
#include <stdio.h>
#include "TRandom3.h"


using namespace std;
using namespace TMath;
// using namespace fastjet;

#include "observables.h"
#include "ran.h"
#include "ChargeFlip.h"

// #include "mt2_bisect.h"
// #include "mt2w_bisect.h"


int main(int argc, const char * argv[])
{
    
    //Pulls and arranges data as needed.
    TChain chain("Delphes");

    for(int i=1; i<argc; i++)
    {
        chain.Add(argv[i]);
        cout << argv[i]<< endl;
    }

    ExRootTreeReader *treeReader = new ExRootTreeReader(&chain);
    Long64_t NumEntries = treeReader->GetEntries();
    cout << "There are "<< NumEntries <<" Entries." <<endl;
    // TClonesArray *branchJet = treeReader->UseBranch("Jet"); 
    TClonesArray *branchElectron = treeReader->UseBranch("Electron");
    TClonesArray *branchMuon = treeReader->UseBranch("Muon");

    TRootLHEFEvent *event;
    TRootLHEFParticle *particle;

    vector <PseudoJet> v_eM, v_eP, v_muM, v_muP, v_lep, v_e, v_mu, v_lepP, v_lepM;

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
    int e_countingParams[3] = {6, 0, 5};
    TH1F *e_counting = new TH1F("NumberOfElectrons", "Number of Electrons", e_countingParams[0], e_countingParams[1], e_countingParams[2]);
    
    int mu_countingParams[3] = {6, 0, 5};
    TH1F *mu_counting = new TH1F("NumberOfMuons", "Number of Muons", mu_countingParams[0], mu_countingParams[1], mu_countingParams[2]);
    
    int lep_countingParams[3] = {6, 0, 5};
    TH1F *lep_counting = new TH1F("NumberOfLeptons", "Number of Leptons", lep_countingParams[0], lep_countingParams[1], lep_countingParams[2]);
    

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
        // for(int entry=0; entry < NumEntries/4; entry++)
        {
            if (VERBOSE) cout<< "I am on Entry " << entry<< endl;

            v_eM.clear();
            v_eP.clear();
            v_e.clear();
            v_mu.clear();
            v_muP.clear();
            v_muM.clear();
            v_lep.clear();
            v_lepP.clear();
            v_lepM.clear();
           
            // cout << "cleared vectors"<< endl;
            treeReader->ReadEntry(entry);
            int numJet = branchJet->GetEntries();
            int numEl = branchElectron->GetEntries();
            int numMu = branchMuon->GetEntries(); 

            // e_counting->Fill(numEl);
            // mu_counting->Fill(numMu);
            // lep_counting->Fill(numEl+numMu);
            mu_counting->Fill((v_muP.size()> v_muM.size()) ? v_muP.size() : v_muM.size())
            
        }
        cout << "Histo time"<< endl;

        TStyle *st1 = new TStyle("st1","my style");
        // cout << "hi"<< endl;
        st1->SetOptStat(111111111);
        // cout << "707"<< endl;
        st1->cd();  //this becomes now the current style gStyle
        TCanvas *c1 = new TCanvas("c1", "ROOT Canvas", 900, 20, 540, 550);

        const char* ImagePath = "/work/pi_mjrm_umass_edu/LNV_collider/AnalysisOutput/leptonCounting";

        char FullPathM2jW[100] = "";
        char FullPathM2jW_root[100] = "";

        strcpy(FullPathM2jW, ImagePath);
        strcat(FullPathM2jW, "/ss_muons.png");
        // MW2j
        MW2j->GetXaxis()->SetTitle("Highest # of s.s. muons per event");
        MW2j->Draw();
        cout << "Made it. Gotta save it"<< endl;
        c1->SaveAs(FullPathM2jW);
        cout << "boutta save root file" <<endl;
        // cout << FullPathM2jW_root << endl;
        // c1->SaveAs(FullPathM2jW_root);
        TFile F1(FullPathM2jW_root, "RECREATE");
        MW2j->Write();
        F1.Close();
    }

}
