import AnalyzeMany as AM
import GenManyOnUnity3 as GM
import parameters_text as PT
import AnalyzeMany as AM
import re


def clear_writeFile():
    open('ParamSpEff.dat', 'w').close()
    # with open('ParamSpEff.dat') as file:

def write_to_file(p1, p2, ef):

    with open('ParamSpEff.dat') as file:
        file.write(f'{p1} {p2} {ef}')

def fileNameMaker(Lambda, geff):

    return f'LNVF_{Lambda}_' + '{:.3f}'.format(geff)[2:]

def analyzeThis(Lambda, geff):
    FolderName = fileNameMaker(Lambda, geff)
    print(FolderName)
    theseFiles = AM.find_files('Signal/'+FolderName)
    
    from_analysis = AM.run_command(f'/home/dkennedy_umass_edu/LNV/MyFiles/LFVLNV/AnalysisAndSuch/JetFake/main LNVF '+ theseFiles, False)

    eff = re.search(r'Efficiency: \n', from_analysis)

    print(eff)
    write_to_file(Lambda, geff, eff)
    


def main():
    LambdaInfo = {'bounds':(1000, 2000), # GeV
                  'delta': 500}
    geffInfo = {'bounds':(0.17, 0.18),
                'delta': 0.0050}
    print('starting ')
    clear_writeFile()

    Lcols = [l for l in range(LambdaInfo['bounds'][0], LambdaInfo['bounds'][1]+ LambdaInfo['delta'], LambdaInfo['delta'])]
    gRows = [g for g in range(geffInfo['bounds'][0], geffInfo['bounds'][1]+ geffInfo['delta'], geffInfo['delta'])]
    # analyzeThis('LNVF_1000_170')
    print(Lcols)
    print(gRows)

    for l in Lcols:
        for g in gRows:
            analyzeThis(l, g)
            print(f'done {l}, {g}')

if __name__=='__main__':
    main()