import subprocess
import re
from dataclasses import dataclass, asdict
import time

def run_command(command):
    output = subprocess.check_output(command, shell=True, encoding='utf8', stderr=subprocess.STDOUT)
    print(f"Output of command '{command}' is",  f'{output}', sep='\n')
    return output

@dataclass
class EventConfig:
    event: str
    instance_count: int

class Event:

    def __init__(self, event, instance, base_file_num):
        self.event = event
        self.proc = None
        self.base_file_num = base_file_num
        self.instance = instance
        self.run_num = self.instance+self.base_file_num
        self.log = None

        # self.start_process() Move this to 

    def __del__(self):
        if self.log is not None:
            self.log.close()

    def start_process(self):
        # print(run_command(f"ls logs"))
        # logFileName = 
        self.log = open(f"logs/{self.event}/attempt_{self.run_num}.log", "w")
        print("I am about to Generate events.", "The output of the madgraph generation can be found in:", f"logs/{self.event}/attempt_{self.run_num}.log", sep='\n')
        self.proc = subprocess.Popen(f"/work/pi_mjrm_umass_edu/LNV_collider/Generated/{self.event}/bin/madevent {self.event}_run.dat", stdout=self.log, stderr=self.log, shell=True)
    
    @property
    def is_running(self):
        if self.proc.poll() is None:
            return True
        return False
    
    @property
    def output_filename(self):
        try:
            output = run_command(f"ls /work/pi_mjrm_umass_edu/LNV_collider/Generated/{self.event}/Events/run_{self.instance+self.base_file_num:02d}/*delphes_events.root")
        except FileNotFoundError:
            print("Generation Failed")
            return 0
        return output
    
    @property
    def generated_count(self):
        if self.is_running:
            return 0
        gendFileName = self.output_filename
        print('test2')
        if gendFileName:
            output = run_command(f"../AnalysisAndSuch/read_root_file {gendFileName}")
            m = re.search(r'\d+$', output)
            return int(m.group()) if m else 0 
        else:
            return 0

    def print_info(self):
        if self.is_running:
            print(f"{self.event} #{self.run_num} is running.")
        else:
            print("test1")
            print(f"{self.event} #{self.instance} completed with {self.generated_count} generated events")


class EventHandler:

    def __init__(self, event, instance_count):
        self.instance_count = instance_count
        self.event = event
        begin_num = self._find_base_num()
        self.events = []

        for rn in range(instance_count):
            thisEvent = Event(event, rn, begin_num)
            thisEvent.start_process()
            thisEvent.print_info()
            thisEvent.proc.wait()
            self.events.append(thisEvent)


    def _find_base_num(self):
        # return 0
        output = run_command(f"ls /work/pi_mjrm_umass_edu/LNV_collider/Generated/{self.event}/Events/")

        m = re.search(r'\d+$', output)
        base_num = int(m.group()) if m else 0
        print(f"Base num for event {self.event} is {base_num}")

        return base_num
    
    @property
    def is_running(self):
        for e in self.events:
            if e.is_running:
                return True        
        return False

    @property
    def generated_count(self):
        count = 0
        for e in self.events:
            count =+ e.generated_count
        return count

    def print_info(self):
        print(f"*** EVENT {self.event} ***") #change wording
        for e in self.events:
            print(f"For run {e.run_num} attempt {e.instance}, ":")
            e.print_info()
            print('test3')
        print(f"Total events generated: {self.generated_count}")
    

class AllEventHandler:

    def __init__(self, event_config):
        self.events = []

        for cfg in event_config:
            self.events.append(EventHandler(**asdict(cfg)))
    
    @property
    def is_running(self):
        for e in self.events:
            if e.is_running:
                return True        
        return False

    def print_info(self):
        print("")
        for e in self.events:
            e.print_info()

if __name__ == '__main__':
    
    allAttemptsConfig = [EventConfig('ttbar', 1)]
    allAttempts = AllEventHandler(allAttemptsConfig)
    allAttempts.print_info()

    # totEventsByType = {}

    while allAttempts.is_running:

        allAttempts.print_info()
        time.sleep(15)
        
        