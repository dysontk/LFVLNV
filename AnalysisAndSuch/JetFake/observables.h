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
using namespace fastjet;
class PseudoJetInfo: public fastjet::PseudoJet::UserInfoBase
{
public:

   
    PseudoJetInfo( int PID_, int BTag_) : PID(PID_), BTag(BTag_) {}
    
    int get_PID() const {return PID;}
    int get_BTag() const {return BTag;}

    

    
protected:
    int PID;
    int BTag;

};//end class PseudoJetInfo



struct sort_by_pt:
public std::binary_function<const PseudoJet & , const PseudoJet &, bool>
{
    bool operator()(const PseudoJet& x, const PseudoJet& y)
    {
        return x.pt()>y.pt();
    }
};

template <class T>
class chi2 {
public:
    chi2() {};
    chi2(int i, int j, int k, int l, T c) : i_(i),j_(j),k_(k),l_(l),chi_(c) {};
    T mass_Chi() const {return chi_;};
    int index1() const {return i_;};
    int index2() const {return j_;};
    int index3() const {return k_;};
    int index4() const {return l_;};
    
protected:

    int i_;
    int j_;
    int k_;
    int l_;
    T chi_;
};

struct sort_by_chi:
public std::binary_function<const chi2<double> &, const chi2<double> &, bool>
{
    bool operator()(const chi2<double>& x, const chi2<double>& y)
    {
        return x.mass_Chi()<y.mass_Chi();
    }
};

void chi_sort(vector<PseudoJet>&);


class mw_mass {
    
public:
    double m;
    int i,j;
    mw_mass() {};
    mw_mass(int a, int b, double c) : i(a), j(b), m(c) {};
    double mass() const {return m;};
    int s() const {return i;};
    int l() const {return j;};
    
};

struct sort_by_mw :
public std::binary_function<const mw_mass&, const mw_mass, bool>
{
    bool operator()(const mw_mass& a, const mw_mass& b)
    {
        return a.mass() < b.mass();
    }
};

void mw_sort(vector<PseudoJet> &);

template <typename  T>
void my_swap(T &a, T &b) {
    T c(a); a=b; b=c;
}

template <class T>
class mtop_sort {
public:
    mtop_sort() {};
    mtop_sort(int i, int j, int k,  T c) : i_(i),j_(j),k_(k),mtop_(c) {};
    T mass_Top() const {return mtop_;};
    int index1() const {return i_;};
    int index2() const {return j_;};
    int index3() const {return k_;};

    
protected:
    
    int i_;
    int j_;
    int k_;
    T mtop_;
};
struct sort_by_mtop :
public std::binary_function<const mtop_sort<double>, mtop_sort<double>, bool>
{
    bool operator()(const mtop_sort<double>& a, const mtop_sort<double>& b)
    {
        return a.mass_Top()<b.mass_Top();
    }
    
};

void m_top(vector<PseudoJet>&);

double b_tagging(double,double);


