import ROOT

init_dir = '/work/pi_mjrm_umass_edu/LNV_collider/AnalysisOutput/'
def combineHistos(eTypes, start_dir=init_dir):

    Stack = ROOT.THStack('WjPair', 'Inv_Mass_2Jets_close_to_W')

    histos = []
    for typ in eTypes:
        histos.append(ROOT.TH1D())
    
    for i in range(len(eTypes)):

        File = ROOT.TFile.Open(start_dir+eTypes[i]+'/plots/Mass_2jW.root')
        histos[i] = File.Get('Inv_Mass_2Jets_close_to_W')
        print("i have it")


        Stack.Add(histos[1])
        Stack.Add(histos[2])
        print("I added them")

    can = ROOT.TCanvas('Canvas')
    can.cd()
    Stack.Draw()
    can.Print(start_dir+'/plots/stackTest.png')

    return Stack


if __name__=='__main__':
    
    eventTypes = ['LNVF', 'ZZ2j']
    combineHistos(eventTypes)