// Spin 0 and Spin 2
//
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

#include "TMath.h"
#include "TFile.h"
#include "TSystem.h"
#include "TGStatusBar.h"
#include "TSystem.h"
// #include "TXMLEngine.h"
#include "TTree.h"

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

#include "fastjet/PseudoJet.hh"
#include "fastjet/JetDefinition.hh"
#include "fastjet/ClusterSequence.hh"


#include "classes/DelphesClasses.h"

//#include <random>
#include <cstdlib>
#include <time.h>
#include <unistd.h>
#include <iterator>
#include<stdio.h>
#include "TRandom3.h"

using namespace std;
using namespace TMath;
using namespace fastjet;

#include "observables.h"
#include "ran.h"
// #include "mt2_bisect.h"
// #include "mt2w_bisect.h"

double EtaToTheta (double eta);
double EtaToTheta (double eta){
    return 2*atan(exp(- eta));
}

void Export_TH1F (TH1F * target_H1F, ofstream &out_file);//use &out_file, becasue ofstream cannot be copied
void Export_TH1F (TH1F * target_H1F, ofstream &out_file){
    double num_entries = target_H1F->GetEntries();
    for( int i = 1; i <= target_H1F->GetNbinsX(); i++){
        out_file<<target_H1F->GetXaxis()->GetBinCenter(i)<<" "<<(target_H1F->GetBinContent(i)/num_entries)<<endl;
    }//return normalized histogram
}

//------- bubble sort begins ------

//exchange the 2 items a and b
void swap(double &a, double &b)
{
    a = a + b;
    b = a - b;
    a = a - b;
}

//ergodic the buf and print it
void ergodic(double  *p,int length)
{
    for (int i = 0; i < length; i++)
    {
        cout << p[i] << " ";
    }
}

void BubbleSort(double  *p, int length)
{
    for (int i = 0; i < length; i++)
    {
        for (int j = 0; j < length - i - 1; j++)
        {
            if (p[j] > p[j + 1])
            {
                swap(p[j], p[j + 1]);
            }
        }
    }
}

//--------- bubble sort ends -----------

const double R_CA=0.4;
const JetDefinition JET_DEF(antikt_algorithm, R_CA);
const double ptmin=30.0;

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

/*
0 for signal
1 for diboson
2 for charge flip
3 for jet fake (ttbar, t+jets, w+jets)
4 for jet fake (QCD jets)

*/

int  BGTYPE=3; 


//declare

double sigma_pT(double pt);
double f_eta(double eta);
double ChargeFlipRate_new(double LepEta, double LepPT);

int main(int argc, const char * argv[]) {

    //----------------------------------------------
    //READING A CHAIN
    //----------------------------------------------
    TChain chain("Delphes");

    int   i;
       for (i = 1; i<argc; i++) {

       	cout<< chain.Add(argv[i])<<endl;

       	// cout<<argv[i]<<endl;
       }

    // chain.Add("/home/_5.root");

    //----------------------------------------------
    //VARIOUS PREPARATIONS BEFORE ANALYSZING A CHAIN
    //----------------------------------------------

    // Naming the output files

    // char label[] = "jet0";

    char label[] ="NA";


    char lFileFormat[] = ".dat";

    char lEgy1Head[50] = "Mee_";//The length of final name should not exceed 50 chars.
    char lEgy2Head[50] = "MllW_";
    char lEgy3Head[50] = "Mll_";
    char lEgy4Head[50] = "Ptj_";
    char lEgy5Head[50] = "Ml2W_";
    char lEgy6Head[50] = "Ml1W_";
    char lEgy7Head[50] = "Ptb1_";
    char lEgy8Head[50] = "Ptb2_";
    char lEgy9Head[50] = "Mt_";

    char lEta1Head[50] = "Etal1_";
    char lEta2Head[50] = "Etab1_";
    char lEta3Head[50] = "Etajj_";
    char lEta4Head[50] = "dphijj_";

    char lCth1Head[50] = "CtheM_";
    char lCth2Head[50] = "CtheP_";
    char lCth3Head[50] = "CthmuM_";
    char lCth4Head[50] = "CthmuP_";

    char *lEgy1, *lEgy2, *lEgy3, *lEgy4, *lEgy5, *lEgy6, *lEgy7, *lEgy8, *lEgy9;
    char *lEta1, *lEta2, *lEta3, *lEta4;
    char *lCth1, *lCth2, *lCth3, *lCth4;
    lEgy1 = strcat( strcat(lEgy1Head, label), lFileFormat);
    lEgy2 = strcat( strcat(lEgy2Head, label), lFileFormat);
    lEgy3 = strcat( strcat(lEgy3Head, label), lFileFormat);
    lEgy4 = strcat( strcat(lEgy4Head, label), lFileFormat);
    lEgy5 = strcat( strcat(lEgy5Head, label), lFileFormat);
    lEgy6 = strcat( strcat(lEgy6Head, label), lFileFormat);
    lEgy7 = strcat( strcat(lEgy7Head, label), lFileFormat);
    lEgy8 = strcat( strcat(lEgy8Head, label), lFileFormat);
    lEgy9 = strcat( strcat(lEgy9Head, label), lFileFormat);

    lEta1 = strcat( strcat(lEta1Head, label), lFileFormat);
    lEta2 = strcat( strcat(lEta2Head, label), lFileFormat);
    lEta3 = strcat( strcat(lEta3Head, label), lFileFormat);
    lEta4 = strcat( strcat(lEta4Head, label), lFileFormat);

    lCth1 = strcat( strcat(lCth1Head, label), lFileFormat);
    lCth2 = strcat( strcat(lCth2Head, label), lFileFormat);
    lCth3 = strcat( strcat(lCth3Head, label), lFileFormat);
    lCth4 = strcat( strcat(lCth4Head, label), lFileFormat);

    TH1F *hEgy1 = new TH1F("","",30,75,105);
    // TH1F *hEgy2 = new TH1F("","",35,0,700); // low-mass SR1
    TH1F *hEgy2 = new TH1F("","",15,80,680); // high-mass SR1
    TH1F *hEgy3 = new TH1F("","",30,0,300);
    TH1F *hEgy4 = new TH1F("","",30,0,100);
    // TH1F *hEgy5 = new TH1F("","",11,40,260); //low-mass SR1
    TH1F *hEgy5 = new TH1F("","",17,20,360); //high-mass SR1
    TH1F *hEgy6 = new TH1F("","",21,60,480); //high-mass SR1

    TH1F *hEgy7 = new TH1F("","",94,0,800);// vs MET dist. in root using MissingET
    TH1F *hEgy8 = new TH1F("","",20,0,200);
    TH1F *hEgy9 = new TH1F("","",50,0,500);

    TH1F *hEta1 = new TH1F("","",6,0,6);
    TH1F *hEta2 = new TH1F("","",30,0,6);
    TH1F *hEta3 = new TH1F("","",30,0,6);
    TH1F *hEta4 = new TH1F("","",30,0,6);

    TH1F *hCth1 = new TH1F("","",86,-3.14,3.14);
    TH1F *hCth2 = new TH1F("","",50,-1,1);
    TH1F *hCth3 = new TH1F("","",50,-1,1);
    TH1F *hCth4 = new TH1F("","",50,-1,1);

    TH1F *hCnts = new TH1F("","",10,0,0.5);

    TCanvas *c1D = new TCanvas("c1D","c1D",10,10,700,900);
   c1D ->Divide(2,2);
    TH1D *h1 = new TH1D("h1","",20,0,200);
    TH1D *h2 = new TH1D("h2","",20,0,200);
    TH1D *h3 = new TH1D("h3","",20,0,200);
    TH1D *h4 = new TH1D("h4","",20,0,200);
//    h1->SetLineColor(1);


    ofstream o_hEgy1, o_hEgy2, o_hEgy3, o_hEgy4, o_hEgy5, o_hEgy6, o_hEgy7, o_hEgy8, o_hEgy9;
    ofstream o_hEta1, o_hEta2, o_hEta3, o_hEta4;
    ofstream o_hCth1, o_hCth2, o_hCth3, o_hCth4;

    // o_hEgy1.open(lEgy1);
    o_hEgy2.open(lEgy2);
    o_hEgy3.open(lEgy3);
    // o_hEgy4.open(lEgy4);
    o_hEgy5.open(lEgy5);
    o_hEgy6.open(lEgy6);
    // o_hEgy7.open(lEgy7);
    // o_hEgy8.open(lEgy8);
    // o_hEgy9.open(lEgy9);
    //
    // o_hEta1.open(lEta1);
    // o_hEta2.open(lEta2);
    // o_hEta3.open(lEta3);
    // o_hEta4.open(lEta4);

    // o_hCth1.open(lCth1);
    // o_hCth2.open(lCth2);
    // o_hCth3.open(lCth3);
    // o_hCth4.open(lCth4);

    ofstream n_size1, n_size2;

    // n_size1.open("n_size1.dat");
    // n_size2.open("n_size2.dat");

    ofstream cut_eff, cut_eff_bkg;

    cut_eff.open("cut_eff.dat",ios::app);
    // cut_eff.open("cut_eff_bkg.dat",ios::app);

    ofstream m1, m2;
    // m1.open("m1_NA.dat");
    // m2.open("m2_NA.dat");

    // Create object of class ExRootTreeReader
    ExRootTreeReader *treeReader = new ExRootTreeReader(&chain);
    Long64_t numberOfEntries = treeReader->GetEntries();

    // Get pointers to branches used in this analysis
    TClonesArray *branchJet = treeReader->UseBranch("Jet");
    TClonesArray *branchElectron = treeReader->UseBranch("Electron");
    TClonesArray *branchMuon = treeReader->UseBranch("Muon");
    // TClonesArray *branchPhoton = treeReader->UseBranch("Photon");
    TClonesArray *branchMET = treeReader->UseBranch("MissingET");
    // TClonesArray *branchMET = treeReader->UseBranch("old_MET");

    TRootLHEFEvent *event;
    TRootLHEFParticle *particle;

    // store various particles in a single event
    vector<PseudoJet> f_all_jet, f_tau_jet, f_b_jet, f_reg_jet;
    vector<PseudoJet> f_eM, f_eP, f_muM, f_muP, f_lep;
    vector<PseudoJet> f_MET, f_ePM, f_muPM, f_lepP, f_lepM;
    vector<PseudoJet> f_gamma;
    vector<PseudoJet> f_w_jet, f_bd_jet, f_nonb_jet;
    vector<int> f_every_count;
    f_every_count = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
    MissingET *met;

    Jet *jet;

     // event counts after each cut
    vector<int> cntCuts;
    cntCuts.clear();

    std::vector<double> scalevector;
    scalevector.clear();

    double scale=0.0;

    int cnt0 = 0, cnt1 = 0, cnt2 = 0, cnt3 = 0, cnt4 = 0, cnt5 =0;

    double cntarry[100] = {0.0};


    if (numberOfEntries ==0) {

      cout<<"  ------------------  "<<endl;
      cout<<"  no event analyzed  "<<endl;
      cout<<"  ------------------  "<<endl;
    }

    else {

    }

    cout<< "Loading events ..." <<endl;


    // Loop over all events
    for(Int_t entry = 0; entry < numberOfEntries; ++entry)
    {

        f_all_jet.clear();
        f_tau_jet.clear();
        f_b_jet.clear();
        f_reg_jet.clear();
        f_eM.clear();
        f_eP.clear();
        f_muM.clear();
        f_muP.clear();
        f_lep.clear();
        f_MET.clear();
        f_gamma.clear();
        f_nonb_jet.clear();
        f_w_jet.clear();
        f_bd_jet.clear();
        f_ePM.clear();
        f_muPM.clear();
        f_lepP.clear();
        f_lepM.clear();
      
        // Load selected branches with data from specified event
        treeReader->ReadEntry(entry);

        // Store particles in a single event
        PseudoJet tmp, misset(0,0,0,0);
        PseudoJet visA, visB, ptmiss;


        // electron
        for(int i = 0; i < branchElectron->GetEntries(); i++){
            Electron * electmp = (Electron *) branchElectron->At(i);
            // if(abs(electmp->Eta)<2.5 && electmp->PT> 20.0) {

              tmp.reset((electmp->P4()).Px(), (electmp->P4()).Py(), (electmp->P4()).Pz(), (electmp->P4()).E());

              if(electmp->Charge == 1){
                  f_eP.push_back(tmp);
              }
              else {
                  f_eM.push_back(tmp);
              }
            // }

        }



        // muon
        for(int i = 0; i < branchMuon->GetEntries(); i++){
            Muon * muontmp = (Muon *) branchMuon->At(i);
            // if(abs(muontmp->Eta)<6 && muontmp->PT>0) {

              tmp.reset((muontmp->P4()).Px(), (muontmp->P4()).Py(), (muontmp->P4()).Pz(), (muontmp->P4()).E());
              if(muontmp->Charge == 1){
                  f_muP.push_back(tmp);
              }
              else {
                  f_muM.push_back(tmp);
              }
            // }

        }


        // Jet
        for(int i = 0; i < branchJet->GetEntries(); i++){
            Jet * jettmp = (Jet *) branchJet->At(i);
            // if(jettmp->PT>20.0 && abs(jettmp->Eta)<2.8) {

              tmp.reset((jettmp->P4()).Px(), (jettmp->P4()).Py(), (jettmp->P4()).Pz(), (jettmp->P4()).E());
              if(jettmp->BTag == 1){
                  f_b_jet.push_back(tmp);
              }
              else {
                f_nonb_jet.push_back(tmp);
                if (jettmp->TauTag == 1){
                    f_tau_jet.push_back(tmp);
                }
                else {
                    f_reg_jet.push_back(tmp);
                }
              }
            // }

        }
        /*
        // photon
        for(int i = 0; i < branchPhoton->GetEntries(); i++){
            Photon * photontmp = (Photon *) branchPhoton->At(i);
            tmp.reset((photontmp->P4()).Px(), (photontmp->P4()).Py(), (photontmp->P4()).Pz(), (photontmp->P4()).E());
            f_gamma.push_back(tmp);
        }

        */

        // MissingET
        for(int i = 0; i < branchMET->GetEntries(); i++){
            MissingET * METtmp = (MissingET *) branchMET->At(i);
            tmp.reset((METtmp->P4()).Px(), (METtmp->P4()).Py(), (METtmp->P4()).Pz(), (METtmp->P4()).E());
            misset+=tmp;
            f_MET.push_back(tmp);
        }

        // cout<< branchElectron->GetEntries()<<endl;
        // cout<< branchJet->GetEntries()<<endl;
        // cout<< branchMET->GetEntries()<<endl;

        // cout<< (branchMET->At(0)->P4()).MET()<<endl;

        for( int i=0; i<f_reg_jet.size(); i++) f_all_jet.push_back(f_reg_jet[i]);
        for( int i=0; i<f_b_jet.size(); i++) f_all_jet.push_back(f_b_jet[i]);
        for( int i=0; i<f_tau_jet.size(); i++) f_all_jet.push_back(f_tau_jet[i]);

        for( int i=0; i<f_eM.size(); i++) f_lep.push_back(f_eM[i] );
        for( int i=0; i<f_eP.size(); i++) f_lep.push_back(f_eP[i] );
        // for( int i=0; i<f_muM.size(); i++) f_lep.push_back(f_muM[i] );
        // for( int i=0; i<f_muP.size(); i++) f_lep.push_back(f_muP[i] );

        for( int i=0; i<f_eM.size(); i++) f_lepM.push_back(f_eM[i] );
        for( int i=0; i<f_eP.size(); i++) f_lepP.push_back(f_eP[i] );
        for( int i=0; i<f_muM.size(); i++) f_lepM.push_back(f_muM[i] );
        for( int i=0; i<f_muP.size(); i++) f_lepP.push_back(f_muP[i] );

        std::sort(f_lep.begin(), f_lep.end(), sort_by_pt());
        std::sort(f_lepP.begin(), f_lepP.end(), sort_by_pt());
        std::sort(f_lepM.begin(), f_lepM.end(), sort_by_pt());

        std::sort(f_eP.begin(), f_eP.end(), sort_by_pt());
        std::sort(f_eM.begin(), f_eM.end(), sort_by_pt());
        std::sort(f_muP.begin(), f_muP.end(), sort_by_pt());
        std::sort(f_muM.begin(), f_muM.end(), sort_by_pt());

        std::sort(f_all_jet.begin(), f_all_jet.end(), sort_by_pt());


// **********************************
//             basic cuts
// **********************************

    int cutOrder = 1;

// cut 0
    f_every_count[0]++;
   if(cntCuts.size() < cutOrder) cntCuts.push_back(0);


   double w=1.0;
   double rs = gRandom->Uniform();


   if (Below_DeltaR_Diff(f_lep,f_all_jet,0.4)) continue;
   if (Below_DeltaR_Same(f_lep,0.4)) continue;
   if (Below_DeltaR_Same(f_all_jet,0.4)) continue;

   ++cntCuts[cutOrder-1];
   cntarry[cutOrder-1] += w;
   ++cutOrder;
  f_every_count[1]++;





//cut 1

   if(cntCuts.size() < cutOrder) cntCuts.push_back(0);


   if (f_lepP.size() < 2 && f_lepM.size() < 2) continue;
  f_every_count[2]++;
   if ((f_lep[0]+f_lep[1]).m() < 10.0 ) continue;
  f_every_count[3]++;


/*
   if (f_eP.size() > 1 || f_eM.size() > 1) {

     if (f_lep[0].pt() < 25 || f_lep[1].pt() < 15) continue;

     if (abs((f_lep[0]+f_lep[1]).m() - 91.2) < 20.0) continue;


   }

   else if (f_muP.size() > 1 || f_muM.size() > 1) {

     if (f_lep[0].pt() < 20 || f_lep[1].pt() < 10) continue;


   }

   else if ((f_eP.size()+f_muP.size()) > 1 || (f_eM.size()+f_muM.size()) > 1) {

     if (f_lep[0].pt() < 25 || f_lep[1].pt() < 10) continue;


   }

*/

// ee
  // if (f_lep[0].pt() < 25 || f_lep[1].pt() < 15) continue;
  // if (abs((f_lep[0]+f_lep[1]).m() - 91.2) < 20.0) continue;

// mumu
  // if (f_lep[0].pt() < 20 || f_lep[1].pt() < 10) continue;

// emu
  // if (f_lep[0].pt() < 25 || f_lep[1].pt() < 10) continue;

    // low-mass SR1
    // double r1=0.15;
    // double r2=0.48;

    // high-mass SR1
    double r1=0.18;
    double r2=0.31;

   if (rs < r1) {

     if (f_lep[0].pt() < 25 || f_lep[1].pt() < 15) continue;

     if (abs((f_lep[0]+f_lep[1]).m() - 91.2) < 20.0) continue;

   }

   else if (rs > r1 && rs < r2) {

     if (f_lep[0].pt() < 20 || f_lep[1].pt() < 10) continue;

   }

   else {

     if (f_lep[0].pt() < 25 || f_lep[1].pt() < 10) continue;

   }
  f_every_count[4]++;
   if (f_lep.size()>2) {

     if (f_lep[2].pt()>10) continue;
   }
  f_every_count[5]++;



  ++cntCuts[cutOrder-1];
  cntarry[cutOrder-1] += w;
  ++cutOrder;


//cut 2

  if(cntCuts.size() < cutOrder) cntCuts.push_back(0);

	if (f_all_jet.size()<2) continue;
f_every_count[6]++;

	double pt=0.0;
	double ht=0.0;


	for(int i=0; i<f_all_jet.size(); i++) {
	  pt = f_all_jet[i].pt();

    // if (pt < 20) continue; // low-mass SR1
    if (pt < 25) continue; // high-mass SR1


	}
  f_every_count[7]++;
  ++cntCuts[cutOrder-1];
  cntarry[cutOrder-1] += w;
  ++cutOrder;


//cut 3


  if(cntCuts.size() < cutOrder) cntCuts.push_back(0);

  double htsum=0;

  for(int i = 0; i < f_all_jet.size(); i++) {

   htsum += f_all_jet[i].pt();

  }
  
  for(int i = 0; i < f_lep.size(); i++) {

   htsum += f_lep[i].pt();

  }

  hEgy4->Fill(pow(f_MET[0].pt(),2)/htsum);

  // if (f_MET[0].pt() > 80) continue; // low-mass SR1
  cout << f_MET.size() << endl;
  if(f_b_jet.size() > 0) continue;
  f_every_count[8]++;
  if (pow(f_MET[0].pt(),2)/htsum > 15.0) continue; // high-mass SR1
  f_every_count[9]++;
  ++cntCuts[cutOrder-1];
  cntarry[cutOrder-1] += w;
  ++cutOrder;


//cut 4

  if(cntCuts.size() < cutOrder) cntCuts.push_back(0);

  if (f_all_jet.size() ==2) {

    for( int i=0; i<f_all_jet.size(); i++) f_w_jet.push_back(f_all_jet[i] );

  }

  else if (f_all_jet.size() == 3) {

    double dmjj01=0.0, dmjj02=0.0, dmjj12=0.0;

    dmjj01 = abs((f_all_jet[0]+f_all_jet[1]).m()-80.4);
    dmjj02 = abs((f_all_jet[0]+f_all_jet[2]).m()-80.4);
    dmjj12 = abs((f_all_jet[1]+f_all_jet[2]).m()-80.4);

    double mwcarry[3] = {dmjj01, dmjj02, dmjj12};

    BubbleSort(mwcarry, sizeof(mwcarry) / sizeof(double));

    if (abs(mwcarry[0]-dmjj01)<pow(10,-3)) {

      f_w_jet.push_back(f_all_jet[0] );
      f_w_jet.push_back(f_all_jet[1] );
    }
    else if (abs(mwcarry[0]-dmjj02)<pow(10,-3)) {

      f_w_jet.push_back(f_all_jet[0] );
      f_w_jet.push_back(f_all_jet[2] );

    }

    else {

      f_w_jet.push_back(f_all_jet[1] );
      f_w_jet.push_back(f_all_jet[2] );

    }

  }

  else if (f_all_jet.size() > 3) {

    double dmjj01=0.0, dmjj02=0.0, dmjj03=0.0, dmjj12=0.0, dmjj13=0.0, dmjj23=0.0;

    dmjj01 = abs((f_all_jet[0]+f_all_jet[1]).m()-80.4);
    dmjj02 = abs((f_all_jet[0]+f_all_jet[2]).m()-80.4);
    dmjj03 = abs((f_all_jet[0]+f_all_jet[3]).m()-80.4);
    dmjj12 = abs((f_all_jet[1]+f_all_jet[2]).m()-80.4);
    dmjj13 = abs((f_all_jet[1]+f_all_jet[3]).m()-80.4);
    dmjj23 = abs((f_all_jet[2]+f_all_jet[3]).m()-80.4);


    double mwcarry[6] = {dmjj01, dmjj02, dmjj03, dmjj12, dmjj13, dmjj23};

    BubbleSort(mwcarry, sizeof(mwcarry) / sizeof(double));

    if (abs(mwcarry[0]-dmjj01)<pow(10,-3)) {

      f_w_jet.push_back(f_all_jet[0] );
      f_w_jet.push_back(f_all_jet[1] );
    }
    else if (abs(mwcarry[0]-dmjj02)<pow(10,-3)) {

      f_w_jet.push_back(f_all_jet[0] );
      f_w_jet.push_back(f_all_jet[2] );

    }
    else if (abs(mwcarry[0]-dmjj03)<pow(10,-3)) {

      f_w_jet.push_back(f_all_jet[0] );
      f_w_jet.push_back(f_all_jet[3] );

    }
    else if (abs(mwcarry[0]-dmjj12)<pow(10,-3)) {

      f_w_jet.push_back(f_all_jet[1] );
      f_w_jet.push_back(f_all_jet[2] );

    }
    else if (abs(mwcarry[0]-dmjj13)<pow(10,-3)) {

      f_w_jet.push_back(f_all_jet[1] );
      f_w_jet.push_back(f_all_jet[3] );

    }

    else {

      f_w_jet.push_back(f_all_jet[2] );
      f_w_jet.push_back(f_all_jet[3] );

    }

  }

  // if ((f_w_jet[0]+f_w_jet[1]+f_lep[0]+f_lep[1]).m() > 300 ) continue; // low-mass SR1, SR2
  if ((f_w_jet[0]+f_w_jet[1]).m() < 30 || (f_w_jet[0]+f_w_jet[1]).m() > 150 ) continue; // high-mass SR1
  f_every_count[10]++;
	hEgy2->Fill((f_w_jet[0]+f_w_jet[1]+f_lep[0]+f_lep[1]).m());

	hEgy3->Fill((f_lep[0]+f_lep[1]).m());

  hEgy5->Fill((f_w_jet[0]+f_w_jet[1]+f_lep[1]).m());

  hEgy6->Fill((f_w_jet[0]+f_w_jet[1]+f_lep[0]).m());


  // scale += w; //used to output the sum of charge flip probabilities after pre-selection cuts
  //
  // scalevector.push_back(scale);


   ++cntCuts[cutOrder-1];
   cntarry[cutOrder-1] += w;
   ++cutOrder;



    } //end of analyzing a single event

    // cout<< hEgy2->GetEntries() <<" "<<hEgy2->Integral()<<endl;



    //----------------------------------------------
    //OUTPUT RESULTS
    //----------------------------------------------

    cout<<"BGTYPE:  "<<BGTYPE<<endl;

    cout<<"Number of Entries = "<<numberOfEntries<<endl;

    for (int i=0; i<cntCuts.size(); i++){
        cout<<"after cut "<<i<<" = "<<cntCuts[i] <<"  "<< cntarry[i]<<endl;

    }

    // cout<<"charge flip probability for total events: " <<scale/cntCuts[0]<<endl;

    // cout<<"lepton number: " <<cnt0 <<" "<<cnt1 <<" "<<cnt2  <<endl;

    cout<<setprecision(6) <<std::fixed<<1.0*cntCuts[cntCuts.size()-1]/numberOfEntries<<endl;

    for (int i=0; i<cntCuts.size(); i++){

    	// cut_eff<<setprecision(5) <<std::fixed<<1.0*cntarry[i]/numberOfEntries<<endl;
    	cut_eff<<setprecision(5) <<std::fixed<<cntarry[i]<<endl;
    }


    TCanvas *c1 = new TCanvas("c1","Root Canvas",900,20,540,550);
    c1->Show();
    //cout<<hPtLep->GetEntries()<<endl;
    // hEta1->Draw();
    hEgy4->Draw();
    // hCth3->Draw();
    // hEta1->Draw();
    //hCnts->Draw();
    c1->SaveAs("delphes_out_1.png");

    c1D->cd(1);
    hEgy2->Draw();
    c1D->cd(2);
    hEgy3->Draw();
    c1D->cd(3);
    hEgy5->Draw();
    c1D->cd(4);
    hEgy6->Draw();
    c1D->SaveAs("kin.png");


    Export_TH1F(hEgy1, o_hEgy1);
    Export_TH1F(hEgy2, o_hEgy2);
    Export_TH1F(hEgy3, o_hEgy3);
    // Export_TH1F(hEgy4, o_hEgy4);
    Export_TH1F(hEgy5, o_hEgy5);
    Export_TH1F(hEgy6, o_hEgy6);
    // Export_TH1F(hEgy7, o_hEgy7);
    // Export_TH1F(hEgy8, o_hEgy8);
    // Export_TH1F(hEgy9, o_hEgy9);
    //
    // Export_TH1F(hEta1, o_hEta1);
    // Export_TH1F(hEta2, o_hEta2);
    // Export_TH1F(hEta3, o_hEta3);
    // Export_TH1F(hEta4, o_hEta4);

    // Export_TH1F(hCth2, o_hCth2);
    // Export_TH1F(hCth3, o_hCth3);

    /*
     // Show resulting histograms
     cJetPt->cd();
     histJetPT->Draw();
     cJetPt->SaveAs("JetPt.pdf");
     */
    cout << "events remaining after each cut"<< endl;
    for (int i=0; i< f_every_count.size(); i++)
    {
      cout << f_every_count[i] << endl;
    }
    cout << endl;
    return 0;
}

double sigma_pT(double pt){
    if (pt >= 400)
        {return 1.000;}
  if (pt >= 200 && pt < 400)
        {return 0.112;}
  if (pt >= 140 && pt < 200)
    {return 0.081;}
  if (pt >= 115 && pt < 140)
    {return 0.060;}
  if (pt >= 100 && pt < 115)
    {return 0.057;}
  if (pt >= 88 && pt < 100)
    {return 0.044;}
  if (pt >= 78 && pt < 88)
    {return 0.041;}
  if (pt >= 69 && pt < 78)
    {return 0.033;}
  if (pt >= 62 && pt < 69)
    {return 0.025;}
  if (pt >= 55 && pt < 62)
    {return 0.021;}
  if (pt >= 48 && pt < 55)
    {return 0.017;}
  if (pt >= 43 && pt < 48)
    {return 0.017;}
  if (pt >= 38 && pt < 43)
    {return 0.020;}
  if (pt >= 34 && pt < 38)
    {return 0.020;}
  if (pt >= 30 && pt < 34)
    {return 0.018;}
  else
    {return 0.000;}
}

double f_eta(double eta){
    if (abs(eta) >= 2.4)
    {return 2.080;}
  if (abs(eta) >= 2.3 && abs(eta) < 2.4)
    {return 1.496;}
  if (abs(eta) >= 2.2 && abs(eta) < 2.3)
    {return 1.039;}
  if (abs(eta) >= 2.1 && abs(eta) < 2.2)
    {return 0.980;}
  if (abs(eta) >= 2.0 && abs(eta) < 2.1)
    {return 0.861;}
  if (abs(eta) >= 1.9 && abs(eta) < 2.0)
    {return 0.692;}
  if (abs(eta) >= 1.8 && abs(eta) < 1.9)
    {return 0.591;}
  if (abs(eta) >= 1.7 && abs(eta) < 1.8)
    {return 0.630;}
  if (abs(eta) >= 1.6 && abs(eta) < 1.7)
    {return 0.410;}
  if (abs(eta) >= 1.5 && abs(eta) < 1.6)
    {return 0.320;}
  if (abs(eta) >= 1.37 && abs(eta) < 1.5)
    {return 0.000;}
  if (abs(eta) >= 1.2 && abs(eta) < 1.37)
    {return 0.160;}
  if (abs(eta) >= 1.1 && abs(eta) < 1.2)
    {return 0.127;}
  if (abs(eta) >= 1.0 && abs(eta) < 1.1)
    {return 0.099;}
  if (abs(eta) >= 0.9 && abs(eta) < 1.0)
    {return 0.093;}
  if (abs(eta) >= 0.7 && abs(eta) < 0.9)
    {return 0.061;}
  if (abs(eta) >= 0.45 && abs(eta) < 0.7)
    {return 0.041;}
  if (abs(eta) >= 0 && abs(eta) < 0.45)
    {return 0.029;}
  else
    {return 0.000;}
}

double ChargeFlipRate_new(double LepEta, double LepPT) //charge flip misidentification ratio
{

    return f_eta(LepEta) * sigma_pT(LepPT);
}
