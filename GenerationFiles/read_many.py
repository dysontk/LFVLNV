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
    
# change this to use a dictionary output to make it easier to handle all togher

def countEvents(eventTypes, OF=''):
    # eventTypes = ['LNVF', 'ttbar', 'W3j', 'WZ2j', 'ZZ2j']
    eventCounts = {}

    # to_write =
    to_print = 'Number of Events Generated:'
    for typ in eventTypes:
        if typ == '':
            continue
        eventCounts.update({typ:0})
        # to_write = 
        to_print += '\n' + typ + ': '
        files = GMOU.run_command(f'ls /work/pi_mjrm_umass_edu/LNV_collider/Generated/{typ}/Events/*/*delphes_events.root', False).split('\n')
        for ThisFile in files:
            eventCounts[typ]+= GMOU.find_num_gend(ThisFile, False)
        NEVENTS = eventCounts[typ]
        to_print += str(NEVENTS)
        # to_write += 
        print(f"finished counting {typ}")
        print(typ + ',' + most_recent_run_num(typ) + ',' + str(NEVENTS) + '\n')
        # if OF != '':
        #     OF.write(typ + ',' + most_recent_run_num(typ) + ',' + str(NEVENTS) + '\n')

    
    print(to_print)
    return eventCounts

def read_num_events(InFil):
    lines = InFil.readlines()
    if lines == []:
        print(f"{InFil} is empty")
        return 0
    for l in range(len(lines)):
        lines[l] = lines[l].strip().split(',')
    print(lines)
    for lin in lines:
        try:
            int(lin[2])
        except ValueError:
            lin[2] = '0'
    return lines

def lines_to_rdict(lins):
    run_dict = {}
    event_dict = {}
    for lin in lins:
        run_dict.update({lin[0]:lin[1]})
        event_dict.update({lin[0]:lin[2]})
    # print(run_dict)
    return run_dict, event_dict

def create_dict(L1, L2ish, verbs=False): #L2ish -- file_info, L1 -- from what is asked

    dic = {}
    new_run_dict = {}
    for l1 in L1:
        dic.update({l1:1})
        new_run_dict.update({l1:most_recent_run_num(l1)})
        if verbs:
            print(f'{l1} added to dictionary')
    # print(f"L2ish, {L2ish}")
    # print("before checking the file, the dictionaries are")
    # print(dic)
    # print(new_run_dict)
    if L2ish != [['']]:
        for l2 in L2ish:
            # print(l2)
            asked_for = False
            curr_run_max = most_recent_run_num(l2[0])
            if verbs:
                print("found current runs ", l2, sep='\n')
            # new_run_dict.update({l2[0]:curr_run_max})
            new_run_dict.update({l2[0]:curr_run_max})
            for key in dic:
                # print("Hey", l2[0], key,sep='\n')
                if l2[0] == key:
                    asked_for = True
                    if curr_run_max == l2[2]:
                        dic[key] = 0 # This says "don't recount if the file (l2[1]) has the same max run number as ls gives"
                        if verbs:
                            print(f'No need to recount {key}')
                    else:
                        if verbs:
                            print(f'Will recount {key}')
                        continue
            if not asked_for:
                dic.update({l2[0]:0})
                if verbs:
                    print(f'{l2[0]} was in the file but not asked for')
    return dic, new_run_dict

def quick_check(eventTyps, infil, verb=False):
    fullRecheck = 0
    # need_to_full_check = {}

    file_info = read_num_events(infil)
    # print(file_info)
    if file_info:
        old_r_dict, old_e_dict = lines_to_rdict(file_info)
    # print(file_info)
        if not file_info:
            if verb:
                print("file empty.")
            fullRecheck = 1
        
        need_to_full_check, new_r = create_dict(eventTyps, file_info, verb)

        if fullRecheck:
            for key in need_to_full_check:
                need_to_full_check[key] = 1
            if verb:
                print("Will recheck all")
        print(need_to_full_check)
        return old_e_dict, old_r_dict, need_to_full_check, new_r
    else:
        return 0

def checkWhatever(need2, outfil, verbo):
    if verbo:
        print([ky if int(need2[ky]) else '' for ky in need2])
    for t in need2:
        if verbo:
            print(t, ": ", "Recounting" if int(need2[t]) else "No Recount Needed")
    newCounts = countEvents([ky if int(need2[ky]) else '' for ky in need2], outfil)
    return newCounts

def WriteItAll(olde, oldr, newe, needy, newr, outf):
    print("printing updated counts")
    fin_r_dict = {}
    fin_e_dict = {}
    i=0
    for K in needy:
        if not int(needy[K]):
            # print(f'These weren\'t re checked, {K} : {needy[K]}') # This prints the old counts which were not rechecked
            to_write = K + ',' + oldr[K] + ',' + olde[K] + '\n'          
            # print('Old writing \n', to_write)
            outf.write(to_write)
            print(to_write)
            fin_r_dict.update({K:oldr[K]})
            fin_e_dict.update({K:olde[K]})
        i += 1

    for t in newe:
        if newe[t] != '':
            # print(f'{t} : {newe[t]}') # this prints the new counts
            outf.write(t+','+ str(newe[t]) + ','+ str(newr[t]) + '\n')
            print(to_write)
            fin_r_dict.update({K:newr[t]})
            fin_e_dict.update({K:newe[t]})

    return fin_r_dict, fin_e_dict

def what_to_do_if_empty(ev_t):
    needy, newr = {}, {}
    for typ in ev_t:
        needy.update({typ:1})
        newr.update({typ:most_recent_run_num(typ)})
    return needy, newr

def redoCounts(eT, fullcheck=0):
    infile = open('/home/dkennedy_umass_edu/LNV/MG5_aMC_v3_5_4/MyFiles/LFVLNV/GenerationFiles/event_counts.txt', 'r')
    quick_out = quick_check(eT, infile)
    is_empty = False
    if quick_out:
        old_e_dict, old_r_dict, need_to_full_check, new_r_dict = quick_out
    else:
        is_empty = True
        old_e_dict = {}
        old_r_dict = {}
        print("File is empty. Will count all")
        need_to_full_check, new_r_dict = what_to_do_if_empty(eT)
        

    if fullcheck or is_empty:
        for key in need_to_full_check:
            need_to_full_check[key] = 1
        print("Will recheck all")
    infile.close()



    outfile = open('event_counts.txt', 'w')    
    '''
    Yeah so countEvents() takes in a list of event types and counts the total events for each
    It then writes that information to the outfile (OF) like so:
    <type>,<highest run number>,<total n events>\n
    '''
    newCounts = checkWhatever(need_to_full_check, outfile, False)
    '''
    Because outfile is write only, it deletes (I believe) the contents. 
    So if there are any events that we did not recheck then that info would be lost.
    The next bit writes the file info for whatever event types we did not need to recheck
    '''    

    final_r_count, final_evnt_count = WriteItAll(old_e_dict, old_r_dict, newCounts, need_to_full_check, new_r_dict, outfile)
    outfile.close()
    return final_r_count, final_evnt_count

if __name__ == '__main__':

    fullRecheck = 0
    eventTypes = ['ZZ2j', 'WZ2j', 'ttbar', 'W3j', 'LNVF']
    redoCounts(eventTypes, fullRecheck)    
    # print(need_to_full_check)
    # # print(file_info)
    # i=0
    # for K in need_to_full_check:
    #     if not int(need_to_full_check[K]):
    #         print(f'These weren\'t re checked, {K} : {need_to_full_check[K]}') # This prints the old counts which were not rechecked
    #         to_write = K + ',' + old_r_dict[K] + ',' + old_e_dict[K] + '\n'          
    #         print('Old writing \n', to_write)
    #         outfile.write(to_write)
    #     i += 1

    # for t in newCounts:
    #     if newCounts[t] != '':
    #         print(f'{t} : {newCounts[t]}') # this prints the new counts
    #         # outfile.write(f'{t},{}')
