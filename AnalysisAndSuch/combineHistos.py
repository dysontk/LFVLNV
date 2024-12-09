import ROOT
import uproot
import matplotlib.pyplot as plt
import numpy as np

def rawHisto_to_datArr(startHisto):
    values = startHisto.values()
    edges = startHisto.axis().edges()
    # print(values)
    # print(len(values))
    # print(edges)
    # print(len(edges))
    half_width = (edges[1]-edges[0])/2
    mids = []
    for i in range(len(edges)-1):
        # print((edges[i+1]-edges[i])/2)
        mids.append(edges[i]+half_width)

    mids = np.array(mids)
    # print(mids)
    # print(len(mids))
    fake_data = []

    for v in range(len(values)):
        # if values[v])
        for n in range(int(values[v])):
            fake_data.append(mids[v])

    print(fake_data)
    return np.array(fake_data)

def get_histo(eventType, hisTyp):
    thisFilePath = init_dir+eventType+'/plots/'+hisTyp+'.root'
    print(thisFilePath)
    thisOne = uproot.open(thisFilePath)[hisTyp]
    # plt.hist(rawHisto_to_datArr(thisOne), 70, stacked=True)
    # plt.show()
    thisHist = thisOne.to_hist().plot(label=eventType)
    # print(type(thisHist[0]))
    return thisHist[0]

def get_data(eventType, histogramtype):
    print(histogramtype)
    thisFilePath = init_dir+eventType+'/plots/'+histogramtype+'.root'
    # print(thisFilePath)
    thisOne = uproot.open(thisFilePath)[histonames2[histogramtype]]
    data = thisOne.values()
    # print(len(thisOne.axis(1)))
    output = {'data': data,
              'bounds': (thisOne.axis(0).low, thisOne.axis(0).high)}
    # print(type(data[0]))
    return output 

def make_histos(eventTypes, histoTypes):
    
    histotitles = {'Mass_2jW': "$\Delta M_{Wjj}$",
                  'Mass_2jW2l': "$\Delta M_{Wjj+ll}$",
                  'Mass_2jW1l0': "$\Delta M_{Wjj+l_0}$",
                  'Mass_2jW1l1': "$\Delta M_{Wjj+l_1}$",
                  'Mass_l2': "$\Delta m_{ll}$"}
    
    for htyp in histoTypes:
        print("making: ", htyp)
        fig, ax = plt.subplots()
        datas = {}
        for typ in eventTypes:
            datas.update({typ:get_data(typ, htyp)})
            # print(len(datas))
        # print(datas)

        bottom = np.zeros(len(datas['LNVF']['data']))
        for typ in datas:
            # print(type(datas[typ]['bounds']))
            low = datas[typ]['bounds'][0]
            hi = datas[typ]['bounds'][1]
            bins = len(datas[typ]['data'])
            ticks = np.linspace(low, hi, num=bins)
            # print(np.shape(ticks))
            # print(np.shape(datas[typ]['data']))
            # print(typ)
            p = ax.bar(ticks, datas[typ]['data'], hi/bins,
                        label=typ, bottom=bottom)
            bottom += datas[typ]['data']
        ax.set_title(histotitles[htyp])
        ax.set_xlabel("GeV")
        ax.legend()
        plt.savefig('/Users/dysonk/Work/LNV_collider/AnalysisOutput/'+histonames2[htyp]+'.png')
        # plt.show()


init_dir = '~/Work/LNV_collider/AnalysisOutput/'
eventTypes = ['LNVF', 'ZZ2j', 'WZ2j', 'W3j', 'ttbar']
histoType = 'bothLeps'

histotypes = ['Mass_2jW', 'Mass_2jW2l', 'Mass_2jW1l0', 'Mass_2jW1l1', 'Mass_l2']
histonames = {'WjPair': "Inv_Mass_2Jets_close_to_W",
                  'bothLeps_Wj': "Inv_Mass_2Jets_close_to_W_2l",
                  'leadingLep_Wj': "Inv_Mass_2Jets_close_to_W_1l_0",
                  'subleadingLep_Wj': "Inv_Mass_2Jets_close_to_W_1l_1",
                  'bothLeps': "Inv_Mass_2l"}
 
histonames2 = {'Mass_2jW': "Inv_Mass_2Jets_close_to_W",
                  'Mass_2jW2l': "Inv_Mass_2Jets_close_to_W_2l",
                  'Mass_2jW1l0': "Inv_Mass_2Jets_close_to_W_1l_0",
                  'Mass_2jW1l1': "Inv_Mass_2Jets_close_to_W_1l_1",
                  'Mass_l2': "Inv_Mass_2l"}

make_histos(eventTypes, histotypes)

# rawHisto_to_datArr()
# get_histo(eventTypes[0], histoType)
# fig, ax = plt.subplots()
# datas = {}
# for typ in eventTypes:
#     datas.update({typ:get_data(typ, histoType)})

# print(datas)

# bottom = np.zeros(len(datas['LNVF']['data']))
# for typ in datas:
#     print(type(datas[typ]['bounds']))
#     low = datas[typ]['bounds'][0]
#     hi = datas[typ]['bounds'][1]
#     bins = len(datas[typ]['data'])
#     ticks = np.linspace(low, hi, num=bins)
#     print(np.shape(ticks))
#     print(np.shape(datas[typ]['data']))
#     print(typ)
#     p = ax.bar(ticks, datas[typ]['data'], hi/bins,
#                 label=typ, bottom=bottom)
#     bottom += datas[typ]['data']
# ax.set_title("$\Delta m_{ll}$")
# ax.set_xlabel("GeV")
# ax.legend()
# plt.show()
# histos = []
# for typ in eventTypes:
#     histos.append(get_histo(typ, histoType))
# plt.legend()
# plt.show()

# histo1 = uproot.open(thisFilePath)[histonames[histoType]].to_hist(metadata='title').plot()
# print(type(histo1[0]))
# thisFilePath1 = init_dir+eventTypes[1]+'/plots/'+histotypes[histoType]+'.root'
# print(thisFilePath1)
# histo1 = uproot.open(thisFilePath1)[histonames[histoType]].to_hist().plot()
# plt.legend()
# plt.show()

# Stack = ROOT.THStack('WjPair', 'Inv_Mass_2Jets_close_to_W')
# # ROOT.gStyle.SetPalette(ROOT.kOcean)
# Files = []
# for typ in eventTypes:
#     # print(type(typ))
#     # print(type(init_dir))
#     filepath = init_dir+typ+'/plots/Mass_2jW.root'
#     Files.append(ROOT.TFile.Open(filepath))

# LNVHisto = Files[0].Get('Inv_Mass_2Jets_close_to_W')
# LNVHisto.SetFillColor(ROOT.kRed)
# LNVHisto.SetLineColor(ROOT.kBlack)
# LNVHisto.SetStats(0)
# ZZHisto = Files[1].Get('Inv_Mass_2Jets_close_to_W')
# ZZHisto.SetFillColor(ROOT.kGreen+1)
# ZZHisto.SetLineColor(ROOT.kBlack)
# ZZHisto.SetStats(0)
# WZHisto = Files[2].Get('Inv_Mass_2Jets_close_to_W')
# WZHisto.SetFillColor(ROOT.kGreen+3)
# WZHisto.SetLineColor(ROOT.kBlack)
# WZHisto.SetStats(0)
# ttbarHisto = Files[3].Get('Inv_Mass_2Jets_close_to_W')
# ttbarHisto.SetFillColor(ROOT.kBlue)
# ttbarHisto.SetLineColor(ROOT.kBlack)
# ttbarHisto.SetStats(0)
# W3Histo = Files[4].Get('Inv_Mass_2Jets_close_to_W')
# W3Histo.SetFillColor(ROOT.kCyan)
# W3Histo.SetLineColor(ROOT.kBlack)
# W3Histo.SetStats(0)
# print("i have it")


# Stack.Add(LNVHisto)
# Stack.Add(ZZHisto)
# Stack.Add(WZHisto)
# Stack.Add(ttbarHisto)
# Stack.Add(W3Histo)
# print("I added them")

# legend = ROOT.TLegend(0.7,0.7,0.9,0.9)
# legend.AddEntry(LNVHisto, "signal", "f")
# legend.AddEntry(ZZHisto, "Diboson: ZZ2j", 'f')
# legend.AddEntry(WZHisto, "Diboson: WZ2j", 'f')
# legend.AddEntry(ttbarHisto, "JetFake: ttbar", "f")
# legend.AddEntry(W3Histo, "JetFake: W+3j", 'f')


# can = ROOT.TCanvas('Canvas')
# can.cd()
# Stack.Draw()
# legend.Draw()

# can.Print(init_dir+'/plots/stackTest.png')

# Stack.SaveAs(init_dir+'/plots/stackTest.root')

# def combineHistos(start_dir=init_dir):

#     eventTypes = ['LNVF', 'ZZ2j', 'WZ2j', 'ttbar', 'W3j']
#     Stack = ROOT.THStack('WjPair', 'Inv_Mass_2Jets_close_to_W')
#     # ROOT.gStyle.SetPalette(ROOT.kOcean)
#     Files = []
#     for typ in eventTypes:
#         # print(type(typ))
#         # print(type(init_dir))
#         filepath = init_dir+typ+'/plots/Mass_2jW.root'
#         Files.append(ROOT.TFile.Open(filepath))
    
#     LNVHisto = Files[0].Get('Inv_Mass_2Jets_close_to_W')
#     LNVHisto.SetFillColor(ROOT.kRed)
#     LNVHisto.SetLineColor(ROOT.kBlack)
#     LNVHisto.SetStats(0)
#     ZZHisto = Files[1].Get('Inv_Mass_2Jets_close_to_W')
#     ZZHisto.SetFillColor(ROOT.kGreen+1)
#     ZZHisto.SetLineColor(ROOT.kBlack)
#     ZZHisto.SetStats(0)
#     WZHisto = Files[2].Get('Inv_Mass_2Jets_close_to_W')
#     WZHisto.SetFillColor(ROOT.kGreen+3)
#     WZHisto.SetLineColor(ROOT.kBlack)
#     WZHisto.SetStats(0)
#     ttbarHisto = Files[3].Get('Inv_Mass_2Jets_close_to_W')
#     ttbarHisto.SetFillColor(ROOT.kBlue)
#     ttbarHisto.SetLineColor(ROOT.kBlack)
#     ttbarHisto.SetStats(0)
#     W3Histo = Files[4].Get('Inv_Mass_2Jets_close_to_W')
#     W3Histo.SetFillColor(ROOT.kCyan)
#     W3Histo.SetLineColor(ROOT.kBlack)
#     W3Histo.SetStats(0)
#     print("i have it")


#     Stack.Add(LNVHisto)
#     Stack.Add(ZZHisto)
#     Stack.Add(WZHisto)
#     Stack.Add(ttbarHisto)
#     Stack.Add(W3Histo)
#     print("I added them")

#     legend = ROOT.TLegend(0.7,0.7,0.9,0.9)
#     legend.AddEntry(LNVHisto, "signal", "l")
#     legend.AddEntry(ZZHisto, "Diboson: ZZ2j", 'l')
#     legend.AddEntry(WZHisto, "Diboson: WZ2j", 'l')
#     legend.AddEntry(ttbarHisto, "JetFake: ttbar", "l")
#     legend.AddEntry(W3Histo, "JetFake: W+3j", 'l')
    

#     can = ROOT.TCanvas('Canvas')
#     can.cd()
#     Stack.Draw()
#     legend.Draw()
#     # ROOT.gPad.BuildLegend()
#     # Stack.GetXaxis().SetTitle("#Delta m_{jj} (GeV)")

#     # can.Print(init_dir+'/plots/stackTest.png')

#     # Stack.SaveAs(init_dir+'/plots/stackTest.root')


#     return legend, Stack


# # if __name__=='__main__':
    
# #     eventTypes = ['LNVF', 'ZZ2j', 'WZ2j', 'ttbar', 'W3j']
# #     leg, stack = combineHistos(eventTypes)

    
# #     can = ROOT.TCanvas('Canvas')
# #     can.cd()
# #     stack.Draw()
# #     # leg.Draw()

# #     # can.Print(init_dir+'/plots/stackTest.png')

# #     stack.SaveAs(init_dir+'plots/stackTest.root')