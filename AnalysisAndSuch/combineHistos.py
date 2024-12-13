import ROOT
import uproot
import matplotlib.pyplot as plt
import numpy as np
import read_many2

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

    # print(fake_data)
    return np.array(fake_data)

def get_histo(eventType, hisTyp):
    thisFilePath = init_dir+eventType+'/plots/'+hisTyp+'.root'
    # print(thisFilePath)
    thisOne = uproot.open(thisFilePath)[hisTyp]
    thisHist = thisOne.to_hist().plot(label=eventType)
    return thisHist[0]

def get_data(eventType, histogramtype, startingdir):
    # print(histogramtype)
    histonames2 = {'Mass_2jW': "Inv_Mass_2Jets_close_to_W",
                    'Mass_2jW2l': "Inv_Mass_2Jets_close_to_W_2l",
                    'Mass_2jW1l0': "Inv_Mass_2Jets_close_to_W_1l_0",
                    'Mass_2jW1l1': "Inv_Mass_2Jets_close_to_W_1l_1",
                    'Mass_l2': "Inv_Mass_2l"}
    thisFilePath = startingdir+eventType+'/plots/'+histogramtype+'.root'
    thisOne = uproot.open(thisFilePath)[histonames2[histogramtype]]
    data = thisOne.values()
    output = {'data': data,
              'bounds': (thisOne.axis(0).low, thisOne.axis(0).high)}
    return output 

def pull_init_events():
    file_to_read = open('../GenerationFiles/event_counts.txt')
    evDict = read_many2.read_num_events(file_to_read)
    
    outDict = {}
    for key in evDict:
        outDict.update({key: evDict[key]['events']})
    print(outDict)
    return outDict


def make_histos(eventTypes, histoTypes, startdir, addonDIR=''):
    
    histotitles = {'Mass_2jW': "$\Delta M_{Wjj}$",
                  'Mass_2jW2l': "$\Delta M_{Wjj+ll}$",
                  'Mass_2jW1l0': "$\Delta M_{Wjj+l_0}$",
                  'Mass_2jW1l1': "$\Delta M_{Wjj+l_1}$",
                  'Mass_l2': "$\Delta m_{ll}$"}
    histonames2 = {'Mass_2jW': "Inv_Mass_2Jets_close_to_W",
                    'Mass_2jW2l': "Inv_Mass_2Jets_close_to_W_2l",
                    'Mass_2jW1l0': "Inv_Mass_2Jets_close_to_W_1l_0",
                    'Mass_2jW1l1': "Inv_Mass_2Jets_close_to_W_1l_1",
                    'Mass_l2': "Inv_Mass_2l"}
    
    crossX = {'LNVF':0.0001279, # For real stuff, what should I use for this? IG just the madgraph numbers
              'WZ2j':42.4,
              'ZZ2j':16.0,
              'W3j':32.4,
              'ttbar':208.2} #pb
    intd_lumin = 0.139 #pb^-1

    branchingRatio = {'LNVF':1,
                      'WZ2j':(3.3645/100)*(10.67/100*2), 
                      'ZZ2j':(3.3645/100)**2,
                      'W3j':(10.67/100*2),
                      'ttbar':13.35/100}
    initEvents = pull_init_events()
    scalefactor = {}
    for key in crossX:
        scalefactor.update({key: crossX[key]*branchingRatio[key]*intd_lumin/initEvents[key]})
    
    
    for htyp in histoTypes:
        print("making: ", htyp)
        fig, ax = plt.subplots()
        datas = {}
        for typ in eventTypes:
            datas.update({typ:get_data(typ, htyp, startdir)})

        templateKey = list(datas.keys())[0]
        # print(type(templateKey))
        # print(templateKey)
        bottom = np.zeros(len(datas[templateKey]['data']))
        for typ in datas:
            low = datas[typ]['bounds'][0]
            hi = datas[typ]['bounds'][1]
            bins = len(datas[typ]['data'])
            to_plot = scalefactor[typ]*datas[typ]['data']
            ticks = np.linspace(low, hi, num=bins)
            p = ax.bar(ticks, to_plot, hi/bins,
                        label=typ, bottom=bottom)
            bottom += to_plot
        ax.set_title(histotitles[htyp])
        ax.set_xlabel("GeV")
        if addonDIR!='':
            #this means it's just the no signal
            bounds = {'Mass_2jW2l': [0,1100],
                    'Mass_2jW1l0': [0,900],
                    'Mass_2jW1l1': [0,750],
                    'Mass_l2': [0,450]}
            try:
                ax.set_xlim(bounds[htyp])
            except KeyError:
                print("This must be the Wjj")
        ax.legend()
        figurepath = startdir+addonDIR+histonames2[htyp]+'.png'
        # '/work/pi_mjrm_umass_edu/LNV_collider/AnalysisOutput/'
        # print(figurepath)
        plt.savefig(figurepath)

def NoSignalHistos(hT, startdir):

    make_histos(['W3j', 'ttbar', 'ZZ2j', 'WZ2j'], hT, startdir, addonDIR='NoSignal/')
    


def OnCluster():
    init_dir = '/work/pi_mjrm_umass_edu/LNV_collider/AnalysisOutput/'
    eventTypes = ['LNVF', 'W3j', 'ttbar', 'ZZ2j', 'WZ2j',]
    # histoType = 'bothLeps'

    histotypes = ['Mass_2jW', 'Mass_2jW2l', 'Mass_2jW1l0', 'Mass_2jW1l1', 'Mass_l2']
    histonames = {'WjPair': "Inv_Mass_2Jets_close_to_W",
                    'bothLeps_Wj': "Inv_Mass_2Jets_close_to_W_2l",
                    'leadingLep_Wj': "Inv_Mass_2Jets_close_to_W_1l_0",
                    'subleadingLep_Wj': "Inv_Mass_2Jets_close_to_W_1l_1",
                    'bothLeps': "Inv_Mass_2l"}
    make_histos(eventTypes, histotypes, init_dir)
    NoSignalHistos(histotypes, init_dir)

    
def main():
    init_dir = '/Users/dysonk/Work/AnalysisOutput/'
    eventTypes = ['LNVF', 'W3j', 'ttbar', 'ZZ2j', 'WZ2j']
    # histoType = 'bothLeps'

    histotypes = ['Mass_2jW', 'Mass_2jW2l', 'Mass_2jW1l0', 'Mass_2jW1l1', 'Mass_l2']
    histonames = {'WjPair': "Inv_Mass_2Jets_close_to_W",
                    'bothLeps_Wj': "Inv_Mass_2Jets_close_to_W_2l",
                    'leadingLep_Wj': "Inv_Mass_2Jets_close_to_W_1l_0",
                    'subleadingLep_Wj': "Inv_Mass_2Jets_close_to_W_1l_1",
                    'bothLeps': "Inv_Mass_2l"}

    make_histos(eventTypes, histotypes, init_dir)
    NoSignalHistos(histotypes, init_dir)

if __name__=='__main__':
    main()
