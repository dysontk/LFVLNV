import ROOT
import uproot
import matplotlib.pyplot as plt
import numpy as np

def rawHisto_to_datArr(startHisto):
    values = startHisto.values()
    edges = startHisto.axis().edges()
    half_width = (edges[1]-edges[0])/2
    mids = []
    for i in range(len(edges)-1):
        mids.append(edges[i]+half_width)

    mids = np.array(mids)
    fake_data = []

    for v in range(len(values)):
        for n in range(int(values[v])):
            fake_data.append(mids[v])

    print(fake_data)
    return np.array(fake_data)

def get_histo(eventType, hisTyp):
    thisFilePath = init_dir+eventType+'/plots/'+hisTyp+'.root'
    print(thisFilePath)
    thisOne = uproot.open(thisFilePath)[hisTyp]
    thisHist = thisOne.to_hist().plot(label=eventType)
    return thisHist[0]

def get_data(eventType, histogramtype, startingdir):
    print(histogramtype)
    thisFilePath = startingdir+eventType+'/plots/'+histogramtype+'.root'
    thisOne = uproot.open(thisFilePath)[histonames2[histogramtype]]
    data = thisOne.values()
    output = {'data': data,
              'bounds': (thisOne.axis(0).low, thisOne.axis(0).high)}
    return output 

def make_histos(eventTypes, histoTypes, startdir):
    
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
            datas.update({typ:get_data(typ, htyp, startdir)})

        bottom = np.zeros(len(datas['LNVF']['data']))
        for typ in datas:
            low = datas[typ]['bounds'][0]
            hi = datas[typ]['bounds'][1]
            bins = len(datas[typ]['data'])
            ticks = np.linspace(low, hi, num=bins)
            p = ax.bar(ticks, datas[typ]['data'], hi/bins,
                        label=typ, bottom=bottom)
            bottom += datas[typ]['data']
        ax.set_title(histotitles[htyp])
        ax.set_xlabel("GeV")
        ax.legend()
        figurepath = '/Users/dysonk/Work/LNV_collider/AnalysisOutput/'+histonames2[htyp]+'.png'
        print(figurepath)
        plt.savefig(figurepath)

def main():
    init_dir = '/work/pi_mjrm_umass_edu/LNV_collider/AnalysisOutput/'
    eventTypes = ['LNVF', 'ZZ2j', 'WZ2j', 'W3j', 'ttbar']
    # histoType = 'bothLeps'

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

    make_histos(eventTypes, histotypes, init_dir)

if __name__=='__main__':
    main()
