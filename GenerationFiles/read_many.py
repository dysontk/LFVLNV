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
    runs = GMOU.run_command(f'ls /work/pi_mjrm_umass_edu/LNV_collider/Generated/{eventType}/Events/', False).split('\n')[:-1]
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
        eventCounts.append([typ,0])
        if typ == '':
            continue
        # to_write = 
        to_print += '\n' + typ + ': '
        files = GMOU.run_command(f'ls /work/pi_mjrm_umass_edu/LNV_collider/Generated/{typ}/Events/*/*delphes_events.root', False).split('\n')
        for ThisFile in files:
            eventCounts[-1][1]+= GMOU.find_num_gend(ThisFile, False)
        NEVENTS = eventCounts[eventTypes.index(typ)]
        to_print += str(NEVENTS)
        # to_write += 
        print(f"finished counting {typ}")
        print(typ + ',' + most_recent_run_num(typ) + ',' + str(NEVENTS) + '\n')
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

def create_dict(L1, L2ish, verbs=False):

    dic = {}
    for l1 in L1:
        dic.update({l1:1})
        if verbs:
            print(f'{l1} added to dictionary')
    if L2ish:
        for l2 in L2ish:
            curr_run_max = most_recent_run_num(l2[0])
            for key in dic:
                if l2[0] == key:
                    if curr_run_max == l2[1]:
                        dic[key] = 0 # This says "don't recount if the file (l2[1]) has the same max run number as ls gives"
                        if verbs:
                            print(f'No need to recount {key}')
                    else:
                        if verbs:
                            print(f'Will recount {key}')
                        continue
                else:
                    dic.update({l2[0]:0})
                    if verbs:
                        print(f'{l2[0]} was in the file but not asked for')
    return dic


if __name__ == '__main__':

    fullRecheck = 0
    eventTypes = ['ZZ2j']
    # fullCheckTypes = []
    need_to_full_check = {}
    # for i in range(len(eventTypes)):
        # need_to_full_check.append((eventTypes[i], 1))
    infile = open('event_counts.txt', 'r')

    file_info = read_num_events(infile)
    print(file_info)
    if not file_info:
        print("file empty.")
        fullRecheck = 1
    
    need_to_full_check = create_dict(eventTypes, file_info, True)

    if fullRecheck:
        for key in need_to_full_check:
            need_to_full_check[key] = 1
        print("Will recheck all")
    print(need_to_full_check)

    outfile = open('event_counts.txt', 'w')    
    '''
    Yeah so countEvents() takes in a list of event types and counts the total events for each
    It then writes that information to the outfile (OF) like so:
    <type>,<highest run number>,<total n events>\n
    '''
   
    print([ky if int(need_to_full_check[ky]) else '' for ky in need_to_full_check])
    for t in need_to_full_check:
        print(t, ": ", "Recounting" if int(need_to_full_check[t]) else "No Recount Needed")
    newCounts = countEvents([ky if int(need_to_full_check[ky]) else '' for ky in need_to_full_check], outfile) 
    '''
    Because outfile is write only, it deletes (I believe) the contents. 
    So if there are any events that we did not recheck then that info would be lost.
    The next bit writes the file info for whatever event types we did not need to recheck
    '''    
    print(need_to_full_check)
    print(file_info)
    # i=0
    # for K in need_to_full_check:
    #     if not int(need_to_full_check[K]):
    #         print(f'{K} : {need_to_full_check[K]}') # This prints the old counts which were not rechecked
    #         to_write = ''
    #         for j in range(3):
    #             to_write += str(file_info[i][j])
    #             to_write += ',' if j<2 else '\n'
    #         outfile.write(to_write)
    #     i += 1

    # for t in newCounts:
    #     if t[0] != '':
    #         print(f'{t[0]} : {t[1]}') # this prints the new counts
    infile.close()
    outfile.close()