import subprocess
import numpy as np
import re

def run_command(command, verbs=True):
    try:
        output = subprocess.check_output(command, shell=True, encoding='utf8', stderr=subprocess.STDOUT)
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
    from_analysis = run_command(f'/home/dkennedy_umass_edu/LNV/MG5_aMC_v3_5_4/MyFiles/LFVLNV/AnalysisAndSuch/JetFake/main {typ} '+ find_files(typ), True)

    theNumbersProcessing = re.search(r'Cut\n+\d+\n+\d+\n+\d+\n+\d+\n+\d+\n', from_analysis).group().split('\n')
    theNumbersProcessing = theNumbersProcessing.remove('Cut').remove('')
    print(theNumbersProcessing)
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
    
    BorS = {}
    
    for typ in cutNum:
        BorS.update({typ:np.array([(ev_count/cutNum[typ][0]*crossX[typ]*intd_lumin) for ev_count in cutNum[typ]])})

    print(BorS)
    
    B = np.zeros(len(BorS['LNVF']))
    # S = 0
    for typ in BorS:
        if typ == 'LNVF':
            # S += BorS[typ]
            continue
        else:
            B += BorS[typ]
    return cutNum['LNVF']/(cutNum['LNVF']+B)**(1/2)


def main():
    list_of_data_types = ['LNVF', 'WZ2j']
    
    nEventsByCuts = multi_analysis(list_of_data_types)

    sig_arr = get_significance(nEventsByCuts)

    print(sig_arr)

if __name__=='__main__':
    main()