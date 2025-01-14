import matplotlib.pyplot as plt
import csv

def main():

    histoTypes = ['MWjl1',
                  'MWjl2',
                  'MWjll']
    eventType = 'Diboson'
    shared_add = 'ComparisonPlotTables/'+eventType+'/'
    histoSources = ['CMS', 'Gang']
    colorDict = {'CMS':'green',
                 'Gang':'red'}
    Ms = {}
    count = {}
    for htyp in histoTypes:
        print(htyp)
        # print()
        Ms.update({htyp:{}})
        count.update({htyp:{}})
        for source in histoSources:
            print(source)
            
            thisFileName = shared_add+source+htyp+'.csv'
            thisM = []
            thiscount = []
            with open(thisFileName) as File:
                Line_reader = csv.reader(File, delimiter=',')
                for row in Line_reader:
                    # print(row)
                    thisM.append(float(row[0]))
                    thiscount.append(float(row[1]))
            Ms[htyp].update({source:thisM})
            count[htyp].update({source:thiscount})
    # print(Ms)
    # print(count)
    # print(Ms[histoTypes[0]])
    for htyp in histoTypes:
        figname = htyp+'Comparison.png'
        fig, ax = plt.subplots()
        for source in histoSources:
            p = plt.scatter(Ms[htyp][source], count[htyp][source], color=colorDict[source], label=source)
    # plt.scatter(Ms[histoTypes[0]]['Gang'], count[histoTypes[0]]['Gang'], color='red')
        ax.set_title(htyp)
        ax.set_xlabel('GeV')
        ax.legend()
        # plt.show()
        plt.savefig(figname)
        # plt
    
    

    # print(M1)
    # print(y1)
    # plt.scatter(M1, y1)
    # plt.show()

if __name__=='__main__':
    main()