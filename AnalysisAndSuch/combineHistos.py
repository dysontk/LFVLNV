import ROOT

init_dir = '/work/pi_mjrm_umass_edu/LNV_collider/AnalysisOutput/'
def combineHistos(start_dir=init_dir):

    File1 = ROOT.TFile.Open(start_dir+'LNVF/plots/Mass_2jW.root')
    File2 = ROOT.TFile.Open(start_dir+'ZZ2j/plots/Mass_2jW.root')

    histo1 = File1.Get('Inv_Mass_2Jets_close_to_W')
    histo2 = File2.Get('Inv_Mass_2Jets_close_to_W')

    Stack = ROOT.THStack('WjPair', 'Inv_Mass_2Jets_close_to_W')
    Stack.Add(histo1)
    Stack.Add(histo2)

    can = ROOT.TCanvas('Canvas')
    can.cd()
    Stack.Draw()
    can.Print(start_dir+'/plots/stackTest.png')

    return Stack


if __name__=='__main__':
    
    combineHistos()