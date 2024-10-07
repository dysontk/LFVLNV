import sys, os
import subprocess
# sys.path.append(os.path.abspath('/home/dysontravis/Research/LFVLNV/GenerationFiles/'))
# import GenManyOnUnity as GMOU

def run_command(command):
    try:
        output = subprocess.check_output(command, shell=True, encoding='utf8', stderr=subprocess.STDOUT)
        print(f"Output of command '{command}' is",  f'{output}', sep='\n')
    except subprocess.CalledProcessError:
        print("Error. Generation probably failed")
        output = str(f"Something when wrong when running {command}")
    return output

def find_num_gend(fi):
        output = run_command(f"./read_root_file {fi}")
        m = re.search(r'\d+$', output)
        return int(m.group()) if m else 0

# def find_

if __name__ == '__main__':

    eventTypes = ['ttbar']
    eventCounts = []

    to_print = 'Number of Events Generated:'
    for typ in eventTypes:
        to_print += '\n' + typ + ': '
        files = run_command(f'ls /work/pi_mjrm_umass_edu/LNV_collider/Generated/{typ}/Events/*/*delphes_events.root').split('\n')
        eventCounts.append(0)
        for ThisFile in files:
            eventCounts[-1]+= find_num_gend(ThisFile)
        to_print += eventCounts[eventTypes.index(typ)]
    
    print(to_print)
