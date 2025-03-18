import AnalyzeMany as AM
import GenManyOnUnity3 as GM
import parameters_text as PT
import ParamSpAnalyzer as PSAnal
testing = False
# def gen_new_proc():
#     GM.run_command('')

# class InfoPacket()
def set_start(dict):
    # print(dict)
    newdict = dict
    newdict.update({'current': dict['bounds'][0]})
    return newdict

def incrementParam(info):
    newinfo = info
    newinfo.update({'current': round(info['current']+ info['delta'], ndigits=5)})
    return newinfo

# def current_params(Linfo, ginfo, lastLambda, lastgeff, mr):
#     # output = {}
#     newLambda = Linfo['current'] + Linfo['delta']
#     return {'ms': newLambda*mr**(1/5), 'mf': newLambda*mr(-4/5), 'geff': ginfo['current']+ ginfo['delta']}
# # Lambda = (mS^4 * mF)^(1/5). Keep the same mS/mF and incrementing Lambda gives those altered masses

def edit_params(LInf, gInf, mass_r):
    newLambdaInfo = LInf
    newgeffInfo = gInf
    paramPath = f'/home/dkennedy_umass_edu/Software/MG5_aMC_v3_5_6/models/O2_flavor/parameters.py' if not testing else 'test.py'
    # print(PT.Parameters_to_write[0])
    orderOfParams = ['geff' for i in range(4)] + ['ms', 'ms', 'mf'] # this gives us the order that you need to write the parameters, 4 geffs, 2 ms, 1 mf
    # print(len(orderOfParams))
    PTW = PT.Parameters_to_write
    # newgeffInfo = incrementParam(gInf)
    # newLambdaInfo = incrementParam(LInf)
    writeParams = {'ms': LInf['current'] * mass_r**(1/5), 
                   'mf': LInf['current'] * mass_r**(-4/5),
                   'geff': gInf['current']}
    # Lambda = (mS^4 * mF)^(1/5). Keep the same mS/mF and incrementing Lambda gives those altered masses
    # newgeffInfo.update({'current': (newParams)})

    with open(paramPath, 'w') as file:
        print('Writing new parameters')
        for s in range(len(PTW)):
            # print(type(PTW[s]))
            
            file.write(str(PTW[s]))
            if s<len(orderOfParams):
                file.write(str(writeParams[orderOfParams[s]]))
                # print(orderOfParams[s], "HHHHHHHHHHHHHHHHHHHHHHHH")
    
    return newLambdaInfo, newgeffInfo

def edit_proc(LInfo, gInfo):
    procPath = '/home/dkennedy_umass_edu/LNV/MyFiles/LFVLNV/GenerationFiles/LNVF_proc.dat' if not testing else 'test.dat'
    formatted_geff = ('{:.3f}'.format(gInfo['current']))[2:]
    to_write = PT.procText + '_' + str(LInfo['current']) + '_' + formatted_geff

    with open(procPath, 'w') as file:
        print(to_write)
        file.write(to_write)
    return procPath

def gen_events(nRuns, thisLambda, thisgeff):
    allAttempts = GM.AllRunHandler([GM.RunConfig('LNVF', nRuns, 0, thisLambda, thisgeff)])

def main():
    DeleteAllPrevRuns = True
    if DeleteAllPrevRuns:
        print('I am deleting the previous runs in the parameter space')
        AM.run_command('rm -vr /work/pi_mjrm_umass_edu/LNV_collider/Generated/Signal/*')
    LambdaInfo = {'bounds':(1000, 5e3), # GeV
                  'delta': 500}
    geffInfo = {'bounds':(0.1, 1.1), 
                'delta': 0.2}
    print(f'Running a grid from Λ = {LambdaInfo["bounds"][0]} to Λ = {LambdaInfo["bounds"][1]}\n with step size δΛ = {LambdaInfo['delta']}')
    print(f'Running a grid from g_eff = {geffInfo["bounds"][0]} to g_eff = {geffInfo["bounds"][1]}\n with step size δg_eff = {geffInfo['delta']}')
    print(f"That's a grid of size {(LambdaInfo['bounds'][1]-LambdaInfo['bounds'][0])/LambdaInfo['delta'] * (geffInfo['bounds'][1]-geffInfo['bounds'][0])/geffInfo['delta']}")
    startAtBeginning = True
    StartPt = (1000, 0.17) # Change this if not starting at the beginning
    nRuns = 5
    LambdaInfo = set_start(LambdaInfo)
    geffInfo = set_start(geffInfo)
    if not startAtBeginning: #if it had gotten interrupted then set startAtBeginning to false and StartPt to the first value that didn't generate enough events (got interrupted)
        LambdaInfo.update({'current': StartPt[0]})
        geffInfo.update({'current': StartPt[1]})
    else:
        PSAnal.clear_writeFile()
    # print(geffInfo)ß
    mass_ratio = 1.5 #mS/mF
    grid_index = [0,0]
    while LambdaInfo['current'] <= LambdaInfo['bounds'][1]:
        
        # print("Lambda: ", LambdaInfo['current'])
        geffInfo = set_start(geffInfo)
        while geffInfo['current'] <= geffInfo['bounds'][1]:
            # print("geff: ", geffInfo['current'])
            edit_params(LambdaInfo, geffInfo, mass_ratio)
            path_to_process_card = edit_proc(LambdaInfo, geffInfo)
            gen_proc_command = '/home/dkennedy_umass_edu/Software/MG5_aMC_v3_5_6/bin/mg5_aMC ' + path_to_process_card
            GM.run_command(gen_proc_command)
            gen_events(nRuns, LambdaInfo['current'], geffInfo['current'])
            # print("here is where I'd gen events")
            PSAnal.analyzeThis(LambdaInfo['current'], geffInfo['current'])
            geffInfo = incrementParam(geffInfo)
            # print("geff: ", geffInfo['current'])

            grid_index[1] += 1
            
        LambdaInfo = incrementParam(LambdaInfo)
        grid_index[0] += 1
    print("I'm finished. I'm gonna reset to the default the parameters")
    edit_params({'current':1000}, {'current':0.176}, 1)


if __name__ == '__main__':
    main()

    ''' as it is, this file loops through the parameter space with the grid spacings defined in 'delta' within the Info dictionaries
    it writes a new .dat file with an altered output path. and writes a new parameter.py with the updated parameters. 
    Processes get generated properly. 
    Then I'll need to sort out what functions to call to have it generate however many events until it stops. test it with 100 of each. (generating processes too)
    Then It should just be an increase of N, grid points, and grid size!.'''