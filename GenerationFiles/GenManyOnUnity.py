import subprocess
import re
from dataclasses import dataclass, asdict
import time

def run_command(command):
    output = subprocess.check_output(command, shell=True, encoding='utf8', stderr=subprocess.STDOUT)
    print(f"Output of command '{command}' is '{output}'")
    return output

@dataclass
class EventConfig:
    event: str
    instance_count: int

class Event:

    def __init__(self, event, instance, base_file_num):
        self.event = event
        self.proc = None
        self.instance = instance
        self.base_file_num = base_file_num
        self.log = None

        self.start_process()

    def __del__(self):
        if self.log is not None:
            close(self.log)

    def start_process(self):
        print(run_command(f"ls logs"))
        self.log = open(f"logs/{self.event}_{self.instance}.log", "a") #The file doesn't already exist
        self.proc = subprocess.Popen(f"/work/pi_mjrm_umass_edu/LNV_collider/Generated/{self.event}/bin/madevent {self.event}_run.dat", stdout=self.log, stderr=self.log, shell=True)
    
    @property
    def is_running(self):
        if self.proc.poll() is None:
            return True
        return False
    
    @property
    def output_filename(self):
        output = run_command(f"ls /work/pi_mjrm_umass_edu/LNV_collider/Generated/{self.event}/Events/run_{self.instance+self.base_file_num:02d}/*delphes_events.root")

        return output
    
    @property
    def generated_count(self):
        if self.is_running:
            return 0
        output = run_command(f"./read_root_file {self.output_filename}")
        m = re.search(r'\d+$', output)
        return int(m.group()) if m else 0 

    def print_info(self):
        if self.is_running:
            print(f"{self.event} #{self.instance} is running.")
        else:
            print(f"{self.event} #{self.instance} completed with {self.generated_count} generated events")


class EventHandler:

    def __init__(self, event, instance_count):
        self.instance_count = instance_count
        self.event = event
        begin_num = self._find_base_num()
        self.events = []

        for rn in range(instance_count):
            self.events.append(Event(event, rn, begin_num))


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
            e.print_info()
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
    
    allAttemptsConfig = [EventConfig('ttbar', 2)]
    allAttempts = AllEventHandler(allAttemptsConfig)
    allAttempts.print_info()

    # totEventsByType = {}

    while allAttempts.is_running:

        allAttempts.print_info()
        time.sleep(15)
        
        