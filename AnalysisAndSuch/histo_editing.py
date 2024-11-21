import subprocess
import numpy as np
import re
import ROOT


def main():

    histopath = '/work/pi_mjrm_umass_edu/LNV_collider/AnalysisOutput/LNVF/plots/Mass_2jW.root'
    thisHistFile = ROOT.TFile.Open(histopath, "READ")
    canvas = ROOT.TCanvas("test")
    canvas.cd()
    thisHist = thisHistFile.Get("c1")
    thisHist.SetLineColor(ROOT.kRed)
    thisHist.Draw()
    print("Printing")
    canvas.SaveAs('Work/LNV_collider/AnalysisOutput/test_histo.png')
    

if __name__ == "__main__":
    main()
    