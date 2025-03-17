import AnalyzeMany as AM
import GenManyOnUnity3 as GM
import parameters_text as PT
import AnalyzeMany as AM
import re


def analyzeThis(FolderName):
    
    theseFiles = AM.find_files('Signal/'+FolderName)
    
    from_analysis = AM.run_command(f'/home/dkennedy_umass_edu/LNV/MyFiles/LFVLNV/AnalysisAndSuch/JetFake/main LNVF '+ theseFiles, False)

    eff = re.search(r'Efficiency: \n', from_analysis)
    print(eff)


def main():
    LambdaInfo = {'bounds':(1000, 2000), # GeV
                  'delta': 500}
    geffInfo = {'bounds':(0.17, 0.18),
                'delta': 0.0050}
    
    # paramGrid = [l for l in range()]
    analyzeThis('LNVF_1000_170')

