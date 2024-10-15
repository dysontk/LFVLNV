import subprocess
import re
from dataclasses import dataclass, asdict
import time
import read_many
import numpy as np
import math
VERBOSE = True
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

def find_num_gend(fi, verbs=True):
        output = run_command(f"/home/dkennedy_umass_edu/LNV/MG5_aMC_v3_5_4/MyFiles/LFVLNV/AnalysisAndSuch/read_root_file {fi}", verbs)
        m = re.search(r'\d+$', output)
        return int(m.group()) if m else 0

@dataclass
class RunConfig:
    eventType: str
    instance_count: int
    prev_nEvents: int

class Run:

    def __init__(self, eventType, instance, base_file_num):
        self.eventType = eventType
        self.proc = None
        self.base_file_num = base_file_num
        self.instance = instance
        self.run_num = self.instance+self.base_file_num
        self.log = None

        print("base num: ", self.base_file_num)
        print("run num:", self.run_num)

        # self.start_process() Move this to 

    def __del__(self):
        if self.log is not None:
            self.log.close()

    def start_process(self):
        # print(run_command(f"ls logs"))
        # logFileName = 
        self.log = open(f"/home/dkennedy_umass_edu/LNV/MG5_aMC_v3_5_4/MyFiles/LFVLNV/GenerationFiles/logs/{self.eventType}/attempt_{self.run_num:02d}.log", "w")
        print("I am about to Generate events.", "The output of the madgraph generation can be found in:", f"logs/{self.eventType}/attempt_{self.run_num:02d}.log", sep='\n')
        self.proc = subprocess.Popen(f"/work/pi_mjrm_umass_edu/LNV_collider/Generated/{self.eventType}/bin/madevent /home/dkennedy_umass_edu/LNV/MG5_aMC_v3_5_4/MyFiles/LFVLNV/GenerationFiles/{self.eventType}_run.dat", stdout=self.log, stderr=self.log, shell=True)
        # self.proc = "I have finidhes"
    
    @property
    def is_running(self):
        if self.proc.poll() is None:
            return True
        return False
    
    @property
    def output_filename(self):
        try:
            output = run_command(f"ls /work/pi_mjrm_umass_edu/LNV_collider/Generated/{self.eventType}/Events/run_{self.run_num:02d}/*delphes_events.root", VERBOSE)
        except FileNotFoundError:
            print("Generation Failed")
            return 0
        # else:
        #     print("Generation Failed", 'Some error other than FileNotFoundError', sep='\n')
        return output
    
    @property
    def generated_count(self):
        if self.is_running:
            return 0
        gendFileName = self.output_filename
        # print('test2')
        if gendFileName:
            output = run_command(f"/home/dkennedy_umass_edu/LNV/MG5_aMC_v3_5_4/MyFiles/LFVLNV/AnalysisAndSuch/read_root_file {gendFileName}", VERBOSE)
            m = re.search(r'\d+$', output)
            return int(m.group()) if m else 0 
        else:
            return 0

    def print_info(self):
        if self.is_running:
            print(f"{self.eventType} #{self.run_num} is running.")
        else:
            # print("test1")
            print(f"{self.eventType} #{self.instance} completed with {self.generated_count} generated events")


class RunHandler:

    def __init__(self, eventType, instance_count, prev_nEvents):
        self.n_runs = instance_count
        # print(self.instance_count)
        self.eventType = eventType
        begin_num = self._find_base_num()
        self.runs = []
        self.tot_nevents = int(prev_nEvents)
        self.runs_gend = 0   
        
        for rn in range(self.n_runs):
            if self.tot_nevents < 200_000:
                
                thisRun = Run(eventType, rn+1, begin_num)
                thisRun.start_process()
                thisRun.print_info()
                thisRun.proc.wait()
                print(f"{self.eventType} attempt {rn+1} complete (run {rn+1+begin_num})")
                self.runs.append(thisRun)
                self.tot_nevents += thisRun.generated_count
                self.runs_gend += 1
            else:
                # self.runs_gend = rn
                print(f"There are over 10k events for {self.eventType}. \nEnding Event Generation")
                break
        


    def _find_base_num(self):
        # return 0
        output = run_command(f"ls /work/pi_mjrm_umass_edu/LNV_collider/Generated/{self.eventType}/Events/", VERBOSE)

        m = re.search(r'\d+$', output)
        base_num = int(m.group()) if m else 0
        print(f"Base num for event {self.eventType} is {base_num}")

        return base_num
    
    @property
    def is_running(self):
        for rn in self.runs:
            if rn.is_running:
                return True        
        return False

    @property
    def generated_count(self):
        count = 0
        for rn in self.runs:
            count =+ evnt.generated_count
        return count

    def print_info(self):
        print(f"*** EVENT {self.eventType} ***") #change wording
        for evnt in self.events:
            print(f"For run {evnt.run_num} attempt {evnt.instance}", ":")
            evnt.print_info()
            # print('test3')
        print(f"Total events generated: {self.generated_count}")
    

class AllRunHandler:

    def __init__(self, run_config):
        self.runs = []
        # self.tot_events = Nevents0

        for cfg in run_config:
            print(f"initializing {cfg.eventType} runs")
            self.runs.append(RunHandler(**asdict(cfg)))
            # self.tot_events += 
            
    
    @property
    def is_running(self):
        for rn in self.runs:
            if rn.is_running:
                return True        
        return False

    def print_info(self):
        print("")
        for evnt in self.events:
            evnt.print_info()

def HowManyRuns(event_count_dic):
    typeEfficiency = {'LNVF': 0.23,
                  'ttbar': 0.23,
                  'W3j': 0.23,
                  'WZ2j': 0.23,
                  'ZZ2j': 0.23}
    # print(event_count_dic)
    runs2Basked = {typ: math.ceil((200_000-int(event_count_dic[typ]['events']))/(typeEfficiency[typ] * 60_000)) for typ in event_count_dic}
    runs2Basked = {typ: 0 if runs2Basked[typ] < 0 else runs2Basked[typ] for typ in runs2Basked}
    return runs2Basked

if __name__ == '__main__':

    eventTypes = ['LNVF', 
                  'ttbar', 
                  'W3j', 
                  'WZ2j', 
                  'ZZ2j'
                  ]
    print("Hi")
    event_count_dict = read_many.redoCounts(eventTypes, 0)
    print(event_count_dict, type(event_count_dict), sep='\n')
    # runs2Basked = np.array([1 if not i else int(((200_000-i)/0.23)/60_000) for i in event_count_dict])
    runs2Basked = HowManyRuns(event_count_dict)
    
    print("Runs to be asked: ", runs2Basked, sep='\n')
    print("event count: ", event_count_dict, sep='\n')
    print("run count", run_command, sep='\n')
    allAttemptsConfig = []
    for typ in eventTypes:
        allAttemptsConfig.append(RunConfig(typ, runs2Basked[typ], event_count_dict[typ]['events']))
        # print(eventTypes[j], ": ", runs2Basked[j])
    # print(allAttemptsConfig)

    for config in allAttemptsConfig:
        # print(f'{config.eventType}')
        print(f'{config.eventType}: {config.instance_count}: {config.prev_nEvents}')
        print(f'{config.eventType} has {config.instance_count} and will end up with ')
        print(f'{config.instance_count+int(event_count_dict[config.eventType]['runs'])}')


    # RunConfig('ttbar', 1), RunConfig('W3j', 1), RunConfig('LNVF', 1), RunConfig('WZ2j', 1)RunConfig('LNVF', 10), RunConfig('WZ2j', 1), RunConfig('ZZ2j', 1)
    # allAttemptsConfig = [RunConfig('ttbar', 6), RunConfig('W3j', 7), RunConfig('LNVF', 9), RunConfig('WZ2j', 2), RunConfig('ZZ2j', 1)]
    # allAttempts = AllRunHandler(allAttemptsConfig)
    # allAttempts.print_info()

    # while allAttempts.is_running:

    #     allAttempts.print_info()
    #     time.sleep(15)
        
    # edit this to run, check how many have gend, then repeat until 200k... no truncate how many are asked for once 200k is reached. 
        