import subprocess
import numpy as np
import re
import ROOT
import combineHistos

def run_command(command, verbs=False):
    try:
        output = subprocess.check_output(command, shell=True, encoding='latin-1', stderr=subprocess.STDOUT)
        if verbs:
            print(f"Output of command '{command}' is",  f'{output}', sep='\n')
    except subprocess.CalledProcessError:
        output = str(f"Something when wrong when running {command}")
        if verbs:
            print("Error. Generation probably failed")
            print(output)
    return output

def find_files(typ):
    return run_command(f'ls /work/pi_mjrm_umass_edu/LNV_collider/Generated/{typ}/Events/*/*delphes_events.root', False).replace('\n', ' ')

def single_analysis(typ):
    from_analysis = run_command(f'/home/dkennedy_umass_edu/LNV/MyFiles/LFVLNV/AnalysisAndSuch/JetFake/main '+ typ + ' ' + find_files(typ), False)
    print("FROM ANALYSIS")
    print(from_analysis)
    theNumbersProcessing = re.search(r'Cut\n+\d+\n+\d+\n+\d+\n+\d+\n+\d+\n', from_analysis).group().split('\n')[1:-1]
    print(theNumbersProcessing)
    # theNumbersProcessing = theNumbersProcessing.remove('Cut')
    # print(theNumbersProcessing)
    return [int(number) for number in theNumbersProcessing]


def multi_analysis(typList):

    cutNumbers = {}
    for e_typ in typList:
        print(e_typ)
        cutNumbers.update({e_typ:single_analysis(e_typ)})
    
    return cutNumbers


def get_significance(cutNum):
    
    crossX = {'LNVF':0.0001279,
              'WZ2j':0.09764,
              'ZZ2j':0.005395,
              'W3j':409.9,
              'ttbar':22.74} #pb
    intd_lumin = 0.139 #pb^-1
    
    effCrossX = {}
    
    for typ in cutNum:
        effCrossX.update({typ:np.array([(ev_count*crossX[typ]) for ev_count in cutNum[typ]])})

    print(effCrossX)
    BorS = {X:effCrossX[X]*intd_lumin/cutNum[X][0] for X in effCrossX}
    # for X in effCrossX:
    #     BorS.update({X:effCrossX[X]*intd_lumin/cutNum[X][0]})
    
    B = np.zeros(len(BorS['LNVF']))
    # S = 0
    for typ in BorS:
        if typ == 'LNVF':
            # S += BorS[typ]
            continue
        else:
            B += BorS[typ]
    
    print("LNVF", BorS['LNVF'])
    print("B", B)
    return BorS['LNVF']/(BorS['LNVF']+B)**(1/2)




        



def main():
    list_of_data_types = [
        # 'LNVF',
        'WZ2j',
        'ZZ2j',
        'W3j',
        # 'ttbar'
        ]

    
    nEventsByCuts = multi_analysis(list_of_data_types)

    sig_arr = get_significance(nEventsByCuts)

    # print(sig_arr)
    # stacks = combineHistos(list_of_data_types)
    combineHistos.OnCluster()

    for i in range(len(sig_arr)):
        print(f'Cut {i}: {sig_arr[i]}')

    

if __name__=='__main__':
    main()