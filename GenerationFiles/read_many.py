import sys, os, subprocess, re
# sys.path.append(os.path.abspath('/home/dysontravis/Research/LFVLNV/GenerationFiles/'))
import GenManyOnUnity as GMOU
import numpy as np

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
    # print(truns)
    return find_number_in_string(runs[-1])[0]
    # runs = runs[:len(runs)/2]
    # print("hi")
    

def countEvents(eventTypes, OF):
    # eventTypes = ['LNVF', 'ttbar', 'W3j', 'WZ2j', 'ZZ2j']
    eventCounts = []

    # to_write =
    to_print = 'Number of Events Generated:'
    for typ in eventTypes:
        if typ == '':
            continue
        # to_write = 
        to_print += '\n' + typ + ': '
        files = GMOU.run_command(f'ls /work/pi_mjrm_umass_edu/LNV_collider/Generated/{typ}/Events/*/*delphes_events.root').split('\n')
        eventCounts.append(0)
        for ThisFile in files:
            eventCounts[-1]+= GMOU.find_num_gend(ThisFile)
        NEVENTS = eventCounts[eventTypes.index(typ)]
        to_print += str(NEVENTS)
        # to_write += 
        OF.write(typ + ',' + most_recent_run_num(typ) + ',' + str(NEVENTS) + '\n')

    
    print(to_print)
    return eventCounts

def read_num_events(InFil):
    lines = infile.readlines()
    if lines == []:
        print(f"{InFil} is empty")
        return 0
    for l in range(len(lines)):
        lines[l] = lines[l].strip().split(',')
    print(lines)
    return lines


if __name__ == '__main__':

    fullRecheck = 0
    eventTypes = ['ZZ2j', 'WZ2j', 'LNVF']
    fullCheckTypes = []
    need_to_full_check = []
    for i in range(len(eventTypes)):
        need_to_full_check.append((eventTypes[i], 0))
    infile = open('event_counts.txt', 'r')

    file_info = read_num_events(infile)
    print(file_info)
    if file_info:
        for typ in eventTypes:
            for TYP in file_info:
                if TYP[0]!=typ:
                    continue
                else:
                    curr_run_max = most_recent_run_num(typ)
                    if curr_run_max != TYP[1]:
                        need_to_full_check[eventTypes.index(typ)][1] = 1
                        print(f"Records show {TYP[1]} runs", f"There are {curr_run_max}")
                    else:
                        print(f'No need to full check {typ}')

    else:
        print(f'File empty')
    print(need_to_full_check)
    
        
    # for i in range(len(need_to_full_check)):
    #     if need_to_full_check[i][1]:
    #         eventTypes[i] = ''
    #     else:
    #         continue
    # print(file_info)
    outfile = open('event_counts.txt', 'w')    
    # print(eventTypes)
    # outfile.write("hi")
    need_to_full_check = np.array(need_to_full_check)
    # print(need_to_full_check[:,0])

    '''
    Yeah so countEvents() takes in a list of event types and counts the total events for each
    It then writes that information to the outfile (OF) like so:
    <type>,<highest run number>,<total n events>\n
    '''
    temp = []
    for i in range(len(need_to_full_check)):
        print(bool(need_to_full_check[i,1]))
        if bool(need_to_full_check[i,1]):
            temp.append(need_to_full_check[i,0])
               
    print(temp)
    print([need_to_full_check[i,0] if bool(need_to_full_check[i,1]) else '' for i in range(len(need_to_full_check))])
    # countEvents([need_to_full_check[i,0] if need_to_full_check[i,1] else continue for i in range(len(need_to_full_check))], outfile) 

    '''
    Because outfile is write only, it deletes (I believe) the contents. 
    So if there are any events that we did not recheck then that info would be lost.
    The next bit writes the file info for whatever event types we did not need to recheck
    '''    
    # for i in range(len(need_to_full_check)):
    #     if not need_to_full_check[i][1]:
    #         to_write = ''
    #         for j in range(3):
    #             print(file_info[i][j])
    #             to_write += str(file_info[i][j]) + ','
    #         outfile.write(to_write+'\n')