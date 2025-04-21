import AnalyzeMany as AM
import GenManyOnUnity3 as GM
import parameters_text as PT
import AnalyzeMany as AM
import re


def clear_writeFile():
    open('ParamSpEff.dat', 'w').close()
    # with open('ParamSpEff.dat') as file:

def write_to_file(p1, p2, ef):
    print(f'{p1} {p2} {ef}')
    with open('ParamSpEff.dat', 'a') as file:
        file.write(f'{p1} {p2} {ef}\n')

def fileNameMaker(Lambda, geff):

    return f'LNVF_{int(Lambda)}_' + '_'.join('{:.3f}'.format(geff).split('.'))

def analyzeThis(Lambda, geff):
    FolderName = fileNameMaker(Lambda, geff)
    print(FolderName)
    theseFiles = AM.find_files('Signal/'+FolderName)
    
    from_analysis = AM.run_command(f'/home/dkennedy_umass_edu/LNV/MyFiles/LFVLNV/AnalysisAndSuch/JetFake/main LNVF '+ theseFiles, True)
    print(from_analysis)
    eff = from_analysis.split('\n')[-2][7:]
    # print(type(from_analysis))
    # eff = re.search('\d+\.+\d\d\d\d\d', from_analysis)
    # print(from_analysis[-100:])
    # print(eff.group())
    # print(float(eff.group()[12:]))
    write_to_file(Lambda, geff, float(eff))
    


def main():
    LambdaInfo = {'bounds':(1000, 5e3), # GeV
                  'delta': 500}
    geffInfo = {'bounds':(0.1, 1.1), 
                'delta': 0.2}
    print('starting ')
    clear_writeFile()
    print(geffInfo['bounds'][0]*1000, (geffInfo['bounds'][1]+ geffInfo['delta'])*1000, geffInfo['delta']*1000, sep='\n')
    Lcols = [l for l in range(LambdaInfo['bounds'][0], int(LambdaInfo['bounds'][1]+ LambdaInfo['delta']), LambdaInfo['delta'])]
    gRows = [g/1000 for g in range(int(geffInfo['bounds'][0]*1000), int((geffInfo['bounds'][1]+ geffInfo['delta'])*1000), int(geffInfo['delta']*1000))]
    # analyzeThis('LNVF_1000_170')ß
    print(Lcols)
    print(gRows)

    for l in Lcols:
        for g in gRows:
            analyzeThis(l, g)
            print(f'done {l}, {g}')

if __name__=='__main__':
    main()