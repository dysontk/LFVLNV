import AnalyzeMany as AM
import GenManyOnUnity3 as GM
import parameters_text as PT
import ParamSpAnalyzer as PSAnal
import numpy as np
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

def edit_proc(LInfo, gInfo, VRB=False):
    procPath = '/home/dkennedy_umass_edu/LNV/MyFiles/LFVLNV/GenerationFiles/LNVF_proc.dat' if not testing else 'test.dat'
    formatted_geff = '_'.join('{:.3f}'.format(gInfo['current']).split('.'))
    to_write = PT.procText + '_' + str(int(LInfo['current'])) + '_' + formatted_geff

    with open(procPath, 'w') as file:
        if VRB:
            print(to_write)
        file.write(to_write)
    return procPath

def gen_events(nRuns, thisLambda, thisgeff):
    allAttempts = GM.AllRunHandler([GM.RunConfig('LNVF', nRuns, 0, thisLambda, thisgeff)])

# def checkExistingRuns(thisLambda, thisgeff, VERB):
#     FolderName = PSAnal.fileNameMaker(thisLambda, thisgeff)
#     if VERB:
#         print(f"This folder will be called {[FolderName]}")
#     ParamPointList = AM.run_command('ls /work/pi_mjrm_umass_edu/LNV_collider/Generated/Signal/').split()
#     if VERB:
#         print(ParamPointList)
#     doesProcExist = False
#     n_runs = 0
#     for paramPoint in ParamPointList:
#         if paramPoint==FolderName:
#             if VERB:
#                 print(f"{paramPoint} and {FolderName} are the same")
#             doesProcExist = True
#             break
#         elif VERB:
#             print(f"{paramPoint} and {FolderName} are not the same")
#             print(type(paramPoint))
#             print(type(FolderName))
#     if doesProcExist:
#         EventsFileNames = AM.run_command('ls /work/pi_mjrm_umass_edu/LNV_collider/Generated/Signal/'+FolderName+'/Events/*/*delphes_events.root')
#         print(EventsFileNames)
#         if EventsFileNames[0] != 't':
#             print(f"There are no runs in {FolderName}")
#             print(EventsFileNames)
#             return 0
#         else:
#             EventsFileNames = EventsFileNames.split()
#             for eFile in EventsFileNames:
#                 n_runs += 1 if (GM.find_num_gend(eFile) > 2800) else 0
#             print("oopsies")
#     print("There are already ", n_runs, " runs")
#     return n_runs

def checkExistingFolders(Linf, ginf, VERB):
    
    lambdas = np.arange(Linf['bounds'][0], Linf['bounds'][1]+Linf['delta'], Linf['delta'])
    geffs = np.arange(ginf['bounds'][0], ginf['bounds'][1]+ginf['delta'], ginf['delta'])
    if VERB:
        print(lambdas)
        print(geffs)

    foldersToBeMade = []
    for l in lambdas:
        for g in geffs:
            foldersToBeMade.append(PSAnal.fileNameMaker(l, g))
    ExistingFolders = AM.run_command('ls /work/pi_mjrm_umass_edu/LNV_collider/Generated/Signal').split()
    if VERB:
        print("pre-existing folders ", ExistingFolders)
        print("Folders I want to make ", foldersToBeMade)
    for pre in ExistingFolders:
        willBeAsked = False
        for new in foldersToBeMade:
            if pre == new:
                willBeAsked = True
                break
        if not willBeAsked:
            if VERB:
                print('I want to delete this one ', pre)
            AM.run_command('rm -vr /work/pi_mjrm_umass_edu/LNV_collider/Generated/Signal/'+pre+'/', True)
def getPreExistingFolders(start_d, VRB):
    fromls = AM.run_command('ls ' + start_d)
    # print(fromls)
    runlist = fromls.split()
    if VRB:
        print("List of existing proc folders: \n", runlist)
    return runlist

def get_runs(sd, foldername, VRB):
    # n_runfolders = 0
    runlist = AM.run_command('ls ' + sd + foldername + 'Events/').split()
    n_runfolders = len(runlist)
    n_runs = 0
    if not n_runfolders:
        if VRB:
            print(f"There are no runs for this process: {foldername}")
        return 0
    else:
        # events = []
        for run in runlist:
            nEvents = 0
            thisFile = AM.run_command(f"ls /work/pi_mjrm_umass_edu/LNV_collider/Generated/Signal/{foldername}Events/{run}/*delphes_events.root", verbs=VRB).strip()
            if thisFile[-4:] == 'root':
                if VRB:
                    print(f"checking runs in {thisFile}")
                nEvents = GM.find_num_gend(thisFile, verbs=VRB)
                if VRB:
                    print(nEvents)
            else:
                if VRB:
                    print(f"There is no delphes file for {run}")
                continue
            # with open(sd+foldername+ run + '/delphes_events.dat', 'r') as fl:
            #     events = fl.readlines()
            #     events = int(events[0])
            if nEvents>=3000:
                n_runs += 1
    return n_runs 

def howManyPreexistingRuns(L, g, start_dir, VRB):
    newFolderName = PSAnal.fileNameMaker(L, g)
    if VRB:
        print(f'This folder will be called {newFolderName}')
    preexistingFolders = getPreExistingFolders(start_dir, VRB)
    alreadyExists = False
    for folder in preexistingFolders:
        if newFolderName == folder:
            if VRB:
                print(f"{folder} == {newFolderName}")
            alreadyExists = True
            break
    
    if not alreadyExists:
        if VRB:
            print(f"This is a new folder")
        return 0
    else:
        if VRB:
            print(f"process for {L}, {g} already exists. Finding runs ..." )
        return get_runs(start_dir, newFolderName+'/', VRB)

        
def make_safe_grid():
    LI = {'bounds':(1000, 5e3), # GeV
                'delta': 500/2}
    gI = {'bounds':(0.1, 1.1), 
                'delta': 0.2/2}
    LI = set_start(LI)
    gI = set_start(gI)
    outlist = []
    while LI['current'] <= LI['bounds'][1]:
        
        # print("Lambda: ", LambdaInfo['current'])
        geffInfo = set_start(gI)
        templist = []
        while gI['current'] <= gI['bounds'][1]:
            outlist.append((LI['current'], gI['current']))
            gI = incrementParam(gI)
        # outlist.append(templist)
        LI = incrementParam(LI)
    return np.array(outlist)

def in_safe_grid(LI, GI, s_grid):
    in_grid = False
    # print(s_grid)
    for pair in s_grid:
        # print(pair)
        # print(np.array((LI['current'], GI['current'])))
        # print((np.array((LI['current'], GI['current'])) == pair).all())
        if (np.array((LI['current'], GI['current'])) == pair).all():
            # print("hi")
            in_grid = True
    return in_grid

def pull_existing_output():
    #text file stuff 
    proclines = np.array([[]])
    with open('ParamSpEff.dat', 'r') as file:
        lines = file.readlines()
        # print("hi ", lines)
        # proclines = np.array([[float(line.strip().split(' ')[i]) if i<2 else int(line.strip().split(' ')[i]) for i in range(len(line.strip().split(' ')))] for line in lines])
        proclines = np.array([[float(line.strip().split(' ')[i]) for i in range(len(line.strip().split(' ')))] for line in lines])
    
    return proclines
        # print(proclines)
def main():
    overwrite_prev_output = False
    DeleteAllPrevRuns = False
    startingGenDir = '/work/pi_mjrm_umass_edu/LNV_collider/Generated/Signal/'
    if DeleteAllPrevRuns:
        print('I am deleting the previous runs in the parameter space')
        AM.run_command('rm -vr /work/pi_mjrm_umass_edu/LNV_collider/Generated/Signal/*')
    LambdaInfo = {'bounds':(1000, 5e3), # GeV
                  'delta': 500/4}
    geffInfo = {'bounds':(0.1, 1.1), 
                'delta': 0.2/4}
    print(f'Running a grid from Λ = {LambdaInfo["bounds"][0]} to Λ = {LambdaInfo["bounds"][1]}\n with step size δΛ = {LambdaInfo["delta"]}')
    print(f'Running a grid from g_eff = {geffInfo["bounds"][0]} to g_eff = {geffInfo["bounds"][1]}\n with step size δg_eff = {geffInfo["delta"]}')
    print(f"That's a grid of size {(LambdaInfo['bounds'][1]+LambdaInfo['delta']-LambdaInfo['bounds'][0])/LambdaInfo['delta'] * (geffInfo['bounds'][1]+geffInfo['delta']-geffInfo['bounds'][0])/geffInfo['delta']}")
    prev_out = pull_existing_output()
    print("previous: \n", prev_out)
    # return 0
    checkExistingFolders(LambdaInfo, geffInfo, True)
    sgrid = make_safe_grid()
    # return 0
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
            print("Checking prev output")
            in_prev_out = False
            if not overwrite_prev_output:
                print("testing....")
                for line in prev_out:
                    # print(line[0])
                    # print(LambdaInfo['current'])
                    if line[0] == LambdaInfo['current'] and line[1]== geffInfo['current']:
                        in_prev_out = True
                        print(f"I already did this point {line}")
                        PSAnal.write_to_file(line[0], line[1], line[2])
            if not in_prev_out:
                print("Preexisting runs...")
                existingRuns = howManyPreexistingRuns(LambdaInfo['current'], geffInfo['current'], startingGenDir, False)
                # print(f'there are already {existingRuns} runs')
                # print(f"asking for {nRuns - existingRuns}")
                path_to_process_card = edit_proc(LambdaInfo, geffInfo)
                if not existingRuns:
                    print(f"I'm going to generate a new process for {LambdaInfo['current']}, {geffInfo['current']}")
                    gen_proc_command = '/home/dkennedy_umass_edu/Software/MG5_aMC_v3_5_6/bin/mg5_aMC ' + path_to_process_card
                    # GM.run_command(gen_proc_command)
                    print(f"no existing runs for {LambdaInfo['current']}, {geffInfo['current']}")
                else:
                    print(f"There is already a process for {LambdaInfo['current']} and {geffInfo['current']} with {existingRuns} runs")
                howManyRuns = nRuns - existingRuns
                print(f"asking for {howManyRuns} runs")
                if howManyRuns:
                    print("here is where I'd gen events")
                    # gen_events(howManyRuns, LambdaInfo['current'], geffInfo['current'])
                else:
                    print("generating no events")
                # PSAnal.analyzeThis(LambdaInfo['current'], geffInfo['current'])
                if not in_safe_grid(LambdaInfo, geffInfo, sgrid):
                    print(f"Deleting events from {LambdaInfo['current'], geffInfo['current']}")
                    # AM.run_command(f"rm -vr /work/pi_mjrm_umass_edu/LNV_collider/Generated/Signal/{PSAnal.fileNameMaker(LambdaInfo['current'], geffInfo['current'])}", verbs=True)
                else:
                    print(f"Saving events from {LambdaInfo['current'], geffInfo['current']}")
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