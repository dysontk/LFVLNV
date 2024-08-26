import os
import re

class Events:

    def __init__(self, attempt, run_num):
        
        # self.client = paramiko.SSHClient()
        # self.client.connect(hostname='unity.rc.umass.edu', username='dkennedy_umass_edu',key_filename='~/.ssh/unity-privkey.key')
        self.run_num = run_num
        self.attempt = attempt
        self.pid = []
        self.begin_num = self.findStartingRunNum()
        self.totEvents = 0
        self.hasCounted = []

        for rn in range(run_num):
            output = os.system(f"nohup /work/pi_mjrm_umass_edu/LNV_collider/Generated/{attempt}/bin/madevent ./MyFiles/LFVLNV/GenerationFiles/{attempt}_run.dat > MyFiles/LFVLNV/GenerationFiles/logs/{attempt}_{rn}.log 2>&1 &")
            self.pid.append(output[-7:])
            self.hasCounted.append(False)
            print(f"I've started {self.attempt}_{rn}")
            print(self.pid)


    def findStartingRunNum(self):
        output = os.system(f"ls /work/pi_mjrm_umass_edu/LNV_collider/Generated/{self.attempt}/Events/")

        m = re.search(r'\d+$', output)

        return int(m.group()) if m else 0
    
    def checkRunning(self, run_num):
        output = os.system(f"ps | grep {self.pid[run_num]}")

        if output:
            return True
        
        return False
    
    def findFileName(self, run_num):
        output = os.system(f"ls /work/pi_mjrm_umass_edu/LNV_collider/Generated/{self.attempt}/Events/run_{run_num+self.begin_num:02d}/*delphes_events.root")

        return output
    
    def check_nEvents(self, run_num):

        if self.hasCounted[run_num]:
            return 0
        
        self.hasCounted[run_num] = True
        output = os.system(f"./read_root_file {self.findFileName(run_num)}")

        m = re.search(r'\d+$', output)

        out = int(m.group()) if m else 0

        self.totEvents += out
        return out
    


if __name__ == '__main__':
    
    
    allAttempts = [Events('ttbar', 2)]

    # totEventsByType = {}

    running = True

    while running:

        running = False
        for att in allAttempts:

            for runNum in range(att.run_num):
                # Within this loop, all attempts are of the same event type
                    if not att.checkRunning(runNum):

                        thisNum = att.check_nEvents(runNum)
                        print(att.attempt, att.run_num, ": ", thisNum)

                    else:
                        running = True

                        


    for at in allAttempts:
        print(at.attempt, ": ", at.totEvents)
        