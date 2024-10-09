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
    if l2:
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
    eventTypes = ['ZZ2j', 'WZ2j', 'LNVF']
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
    # if not fullRecheck:
    #     for TYP in file_info:
    #         not_asked_for = False
    #         for typ in eventTypes:
    #             if TYP[0] == typ:
    #                 not_asked_for = True
    #                 curr_run_max = most_recent_run_num(typ)
    #                 if curr_run_max != TYP[1]:
    #                     need_to_full_check.update({typ, 1})
    #                     print(f"For {TYP[0]} Records show {TYP[1]} runs", f"There are {curr_run_max}")
    #                 else:
    #                     print(f'No need to full check {typ}')
    #                     need_to_full_check.update({typ: 0})
    #         if not not_asked_for:
    #             print(f'{TYP} was not asked for but is currently in the document')
    #             need_to_full_check.update({TYP[0]: 0})
                

    if fullRecheck:
        for key in need_to_full_check:
            need_to_full_check[key] = 1
        print("Will recheck all")
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
    # need_to_full_check = np.array(need_to_full_check)
    # need_to_check_arr = np.array(shape=(len(need_to_full_check), 2))
    # print(need_to_full_check[:,0])

    '''
    Yeah so countEvents() takes in a list of event types and counts the total events for each
    It then writes that information to the outfile (OF) like so:
    <type>,<highest run number>,<total n events>\n
    '''
    # temp = []
    # for i in range(len(need_to_full_check)):
    #     print(int(need_to_full_check[i,1]))
    #     # print(need_to_full_check[])
    #     if int(need_to_full_check[i,1]):
    #         temp.append(need_to_full_check[i,0])
               
    # print(temp)
    print([ky if int(need_to_full_check[ky]) else '' for ky in need_to_full_check])
    # print()

    for t in need_to_full_check:
        # print(t[1])
        # print(type(t[1]))
        print(t, ": ", "Recounting" if int(need_to_full_check[t]) else "No Recount Needed")
    newCounts = countEvents([ky if int(need_to_full_check[ky]) else '' for ky in need_to_full_check], outfile) 
    # print(newCounts)
    '''
    Because outfile is write only, it deletes (I believe) the contents. 
    So if there are any events that we did not recheck then that info would be lost.
    The next bit writes the file info for whatever event types we did not need to recheck
    '''    
    i=0
    for K in need_to_full_check:
        if not int(need_to_full_check[K]):
            # print(f"{need_to_full_check[i][0]} was not recounted. Reprinting info now")
            print(f'{K} : {need_to_full_check[K]}') # This prints the old counts which were not rechecked
            to_write = ''
            for j in range(3):
                # print(file_info[i][j])
                to_write += str(file_info[i][j])
                to_write += ',' if j<2 else '\n'
                # if j > 3

            outfile.write(to_write)
        i += 1

    for t in newCounts:
        if t[0] != '':
            print(f'{t[0]} : {t[1]}') # this prints the new counts
    infile.close()
    outfile.close()