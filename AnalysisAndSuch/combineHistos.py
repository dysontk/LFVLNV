import ROOT

init_dir = '/work/pi_mjrm_umass_edu/LNV_collider/AnalysisOutput/'
def combineHistos(eTypes, start_dir=init_dir):

    Stack = ROOT.THStack('WjPair', 'Inv_Mass_2Jets_close_to_W')

    histos = {}
    for typ in eTypes:
        File = ROOT.TFile.Open(start_dir+'LNVF/plots/Mass_2jW.root')
    # File2 = ROOT.TFile.Open(start_dir+'ZZ2j/plots/Mass_2jW.root')

        histo = File.Get('Inv_Mass_2Jets_close_to_W')
        print("i have it")
    # histo2 = File2.Get('Inv_Mass_2Jets_close_to_W')

    # for histo in histos:
        Stack.Add(histo)
        print("I added it")
    # Stack.Add(histo2)

    can = ROOT.TCanvas('Canvas')
    can.cd()
    Stack.Draw()
    can.Print(start_dir+'/plots/stackTest.png')

    return Stack


if __name__=='__main__':
    
    eventTypes = ['LNV', 'ZZ2j']
    combineHistos(eventTypes)