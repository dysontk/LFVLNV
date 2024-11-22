import ROOT

init_dir = '/work/pi_mjrm_umass_edu/LNV_collider/AnalysisOutput/'
def combineHistos(start_dir=init_dir):

    eventTypes = ['LNVF', 'ZZ2j', 'WZ2j', 'ttbar', 'W3j']
    Stack = ROOT.THStack('WjPair', 'Inv_Mass_2Jets_close_to_W')

    Files = []
    for typ in eventTypes:
        print(type(typ))
        print(type(init_dir))
        filepath = init_dir+typ+'/plots/Mass_2jW.root'
        Files.append(ROOT.TFile.Open(filepath))
    
    LNVHisto = Files[0].Get('Inv_Mass_2Jets_close_to_W')
    ZZHisto = Files[1].Get('Inv_Mass_2Jets_close_to_W')
    ZZHisto = Files[2].Get('Inv_Mass_2Jets_close_to_W')
    ttbarHisto = Files[3].Get('Inv_Mass_2Jets_close_to_W')
    W3Histo = Files[3].Get('Inv_Mass_2Jets_close_to_W')
    print("i have it")


    Stack.Add(LNVHisto)
    Stack.Add(ZZHisto)
    Stack.Add(ZZHisto)
    Stack.Add(ttbarHisto)
    Stack.Add(W3Histo)
    print("I added them")

    can = ROOT.TCanvas('Canvas')
    can.cd()
    Stack.Draw()
    can.Print(start_dir+'/plots/stackTest.png')

    return Stack


if __name__=='__main__':
    
    eventTypes = ['LNVF', 'ZZ2j', 'WZ2j', 'ttbar', 'W3j']
    combineHistos(eventTypes)