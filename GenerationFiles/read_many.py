import sys, os, subprocess, re
# sys.path.append(os.path.abspath('/home/dysontravis/Research/LFVLNV/GenerationFiles/'))
import GenManyOnUnity as GMOU

# def run_command(command):
#     try:
#         output = subprocess.check_output(command, shell=True, encoding='utf8', stderr=subprocess.STDOUT)
#         print(f"Output of command '{command}' is",  f'{output}', sep='\n')
#     except subprocess.CalledProcessError:
#         print("Error. Generation probably failed")
#         output = str(f"Something when wrong when running {command}")
#         print(output)
#     return output

# def find_num_gend(fi):
#         output = run_command(f"./read_root_file {fi}")
#         m = re.search(r'\d+$', output)
#         return int(m.group()) if m else 0

# def find_

def find_number_in_string(strin):
    return re.findall('\d+', strin)

def most_recent_run_num(eventType):
    runs = GMOU.run_command(f'ls /work/pi_mjrm_umass_edu/LNV_collider/Generated/{eventType}/Events/').split('\n')[:-1]
    # print(len(runs))
    print(runs)
    return find_number_in_string(runs[-1])
    # runs = runs[:len(runs)/2]
    # print("hi")
    

def countEvents(eventTypes, outfile):
    # eventTypes = ['LNVF', 'ttbar', 'W3j', 'WZ2j', 'ZZ2j']
    eventCounts = []

    to_print = 'Number of Events Generated:'
    for typ in eventTypes:
        to_print += '\n' + typ + ': '
        files = GMOU.run_command(f'ls /work/pi_mjrm_umass_edu/LNV_collider/Generated/{typ}/Events/*/*delphes_events.root').split('\n')
        eventCounts.append(0)
        for ThisFile in files:
            eventCounts[-1]+= GMOU.find_num_gend(ThisFile)
        to_print += str(eventCounts[eventTypes.index(typ)])
    
    print(to_print)
    return eventCounts

if __name__ == '__main__':

    fullRecheck = False

    eventTypes = ['ttbar', 'W3j', 'WZ2j', 'ZZ2j']
    
    print(most_recent_run_num('ttbar'))
    # countEvents(eventTypes)
