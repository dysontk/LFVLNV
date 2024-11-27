import ROOT

init_dir = '/work/pi_mjrm_umass_edu/LNV_collider/AnalysisOutput/'
files = []

eventTypes = ['LNVF', 'ZZ2j', 'WZ2j', 'ttbar', 'W3j']
Stack = ROOT.THStack('WjPair', 'Inv_Mass_2Jets_close_to_W')
# ROOT.gStyle.SetPalette(ROOT.kOcean)
Files = []
for typ in eventTypes:
    # print(type(typ))
    # print(type(init_dir))
    filepath = init_dir+typ+'/plots/Mass_2jW.root'
    Files.append(ROOT.TFile.Open(filepath))

LNVHisto = Files[0].Get('Inv_Mass_2Jets_close_to_W')
LNVHisto.SetFillColor(ROOT.kRed)
LNVHisto.SetLineColor(ROOT.kBlack)
LNVHisto.SetStats(0)
ZZHisto = Files[1].Get('Inv_Mass_2Jets_close_to_W')
ZZHisto.SetFillColor(ROOT.kGreen+1)
ZZHisto.SetLineColor(ROOT.kBlack)
ZZHisto.SetStats(0)
WZHisto = Files[2].Get('Inv_Mass_2Jets_close_to_W')
WZHisto.SetFillColor(ROOT.kGreen+3)
WZHisto.SetLineColor(ROOT.kBlack)
WZHisto.SetStats(0)
ttbarHisto = Files[3].Get('Inv_Mass_2Jets_close_to_W')
ttbarHisto.SetFillColor(ROOT.kBlue)
ttbarHisto.SetLineColor(ROOT.kBlack)
ttbarHisto.SetStats(0)
W3Histo = Files[4].Get('Inv_Mass_2Jets_close_to_W')
W3Histo.SetFillColor(ROOT.kCyan)
W3Histo.SetLineColor(ROOT.kBlack)
W3Histo.SetStats(0)
print("i have it")


Stack.Add(LNVHisto)
Stack.Add(ZZHisto)
Stack.Add(WZHisto)
Stack.Add(ttbarHisto)
Stack.Add(W3Histo)
print("I added them")

legend = ROOT.TLegend(0.7,0.7,0.9,0.9)
legend.AddEntry(LNVHisto, "signal", "f")
legend.AddEntry(ZZHisto, "Diboson: ZZ2j", 'f')
legend.AddEntry(WZHisto, "Diboson: WZ2j", 'f')
legend.AddEntry(ttbarHisto, "JetFake: ttbar", "f")
legend.AddEntry(W3Histo, "JetFake: W+3j", 'f')


can = ROOT.TCanvas('Canvas')
can.cd()
Stack.Draw()
legend.Draw()

can.Print(init_dir+'/plots/stackTest.png')

Stack.SaveAs(init_dir+'/plots/stackTest.root')

def combineHistos(start_dir=init_dir):

    eventTypes = ['LNVF', 'ZZ2j', 'WZ2j', 'ttbar', 'W3j']
    Stack = ROOT.THStack('WjPair', 'Inv_Mass_2Jets_close_to_W')
    # ROOT.gStyle.SetPalette(ROOT.kOcean)
    Files = []
    for typ in eventTypes:
        # print(type(typ))
        # print(type(init_dir))
        filepath = init_dir+typ+'/plots/Mass_2jW.root'
        Files.append(ROOT.TFile.Open(filepath))
    
    LNVHisto = Files[0].Get('Inv_Mass_2Jets_close_to_W')
    LNVHisto.SetFillColor(ROOT.kRed)
    LNVHisto.SetLineColor(ROOT.kBlack)
    LNVHisto.SetStats(0)
    ZZHisto = Files[1].Get('Inv_Mass_2Jets_close_to_W')
    ZZHisto.SetFillColor(ROOT.kGreen+1)
    ZZHisto.SetLineColor(ROOT.kBlack)
    ZZHisto.SetStats(0)
    WZHisto = Files[2].Get('Inv_Mass_2Jets_close_to_W')
    WZHisto.SetFillColor(ROOT.kGreen+3)
    WZHisto.SetLineColor(ROOT.kBlack)
    WZHisto.SetStats(0)
    ttbarHisto = Files[3].Get('Inv_Mass_2Jets_close_to_W')
    ttbarHisto.SetFillColor(ROOT.kBlue)
    ttbarHisto.SetLineColor(ROOT.kBlack)
    ttbarHisto.SetStats(0)
    W3Histo = Files[4].Get('Inv_Mass_2Jets_close_to_W')
    W3Histo.SetFillColor(ROOT.kCyan)
    W3Histo.SetLineColor(ROOT.kBlack)
    W3Histo.SetStats(0)
    print("i have it")


    Stack.Add(LNVHisto)
    Stack.Add(ZZHisto)
    Stack.Add(WZHisto)
    Stack.Add(ttbarHisto)
    Stack.Add(W3Histo)
    print("I added them")

    legend = ROOT.TLegend(0.7,0.7,0.9,0.9)
    legend.AddEntry(LNVHisto, "signal", "l")
    legend.AddEntry(ZZHisto, "Diboson: ZZ2j", 'l')
    legend.AddEntry(WZHisto, "Diboson: WZ2j", 'l')
    legend.AddEntry(ttbarHisto, "JetFake: ttbar", "l")
    legend.AddEntry(W3Histo, "JetFake: W+3j", 'l')
    

    can = ROOT.TCanvas('Canvas')
    can.cd()
    Stack.Draw()
    legend.Draw()
    # ROOT.gPad.BuildLegend()
    # Stack.GetXaxis().SetTitle("#Delta m_{jj} (GeV)")

    # can.Print(init_dir+'/plots/stackTest.png')

    # Stack.SaveAs(init_dir+'/plots/stackTest.root')


    return legend, Stack


# if __name__=='__main__':
    
#     eventTypes = ['LNVF', 'ZZ2j', 'WZ2j', 'ttbar', 'W3j']
#     leg, stack = combineHistos(eventTypes)

    
#     can = ROOT.TCanvas('Canvas')
#     can.cd()
#     stack.Draw()
#     # leg.Draw()

#     # can.Print(init_dir+'/plots/stackTest.png')

#     stack.SaveAs(init_dir+'plots/stackTest.root')