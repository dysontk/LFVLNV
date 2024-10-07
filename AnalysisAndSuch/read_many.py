import sys, os
sys.path.append(os.path.abspath('/home/dysontravis/Research/LFVLNV/GenerationFiles/'))
import GenManyOnUnity.py as GMOU

# def find_

if __name__ == '__main__':

    eventTypes = ['ttbar']
    eventCounts = []

    to_print = 'Number of Events Generated:'
    for typ in eventTypes:
        to_print += '\n' + typ + ': '
        files = GMOU.run_command(f'ls /work/pi_mjrm_umass_edu/LNV_collider/Generated/{self.event}/Events/*/*delphes_events.root').split('\n')
        eventCounts.append(0)
        for ThisFile in files:
            eventCounts[-1]+= GMOU.find_num_gend(ThisFile)
        to_print += eventCounts[eventTypes.index(typ)]
    
    print(to_print)
