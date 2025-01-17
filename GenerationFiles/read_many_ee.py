import sys, os, subprocess, re
# sys.path.append(os.path.abspath('/home/dysontravis/Research/LFVLNV/GenerationFiles/'))
import GenManyOnUnity_ee as GMOU
import numpy as np


def find_number_in_string(strin):
    return re.findall('\d+', strin)

def most_recent_run_num(eventType, ee=False):
    runs = GMOU.run_command(f'ls /work/pi_mjrm_umass_edu/LNV_collider/Generated/' + 'just_ee/' if ee else ''+'{eventType}/Events/', False).split('\n')[:-1]
    try:
        return find_number_in_string(runs[-1])[0]
    except IndexError:
        return 0

    
# change this to use a dictionary output to make it easier to handle all togher

def countEvents(eventTypes, OF='', ee=False):
    # eventTypes = ['LNVF', 'ttbar', 'W3j', 'WZ2j', 'ZZ2j']
    eventCounts = {}
    print(eventTypes)
    # to_write =
    to_print = 'Number of Events Generated:'
    for typ in eventTypes:
        nEvents = 0
        if typ == '':
            continue

        to_print += '\n' + typ + ': '
        files = GMOU.run_command(f'ls /work/pi_mjrm_umass_edu/LNV_collider/Generated/'+'just_ee/'if ee else ''+'{typ}/Events/*/*delphes_events.root', False).split('\n')
        print("Files: ", files)
        for ThisFile in files:
            # nEvents += GMOU.find_num_gend(ThisFile, False)
            nEvents += GMOU.find_num_gend(ThisFile, True)

        to_print += str(nEvents)
        print(f"finished counting {typ}")
        runs = most_recent_run_num(typ,ee)
        print(typ + ',' + str(runs) + ',' + str(nEvents) + '\n')
        eventCounts.update({typ:{'runs':runs, 'events':nEvents, 'recount':0}})
    
    print(to_print)
    print(eventCounts)
    return eventCounts

def read_num_events(InFil):
    lines = InFil.readlines()
    lineDict = {}
    if lines == []:
        print(f"{InFil} is empty")
        return 0
    for l in range(len(lines)):
        thisLine = lines[l].strip().split(',')
        lineDict.update({thisLine[0]:{'runs':thisLine[1], 'events':thisLine[2]}})
    print(lineDict)
    return lineDict

def create_dict(wanted, in_doc, verbs=False, is_ee=False): #L2ish -- file_info, L1 -- from what is asked
    from_doc = in_doc
    if from_doc:
        for typ in wanted:
            if list(from_doc.keys()).count(typ):
                curr_run_max = most_recent_run_num(typ, ee=is_ee)
                from_doc[typ].update({'recount':0 if curr_run_max==from_doc[typ]['runs'] else 1})
            else:
                from_doc.update({typ:{'runs':0,'events':0,'recount':1}})
    else:
        from_doc = {}
        for typ in wanted:
            from_doc.update({typ:{'runs':0,'events':0,'recount':1}})

    return from_doc


def quick_check(eventTyps, infil, verb=False, ee=False):
    fullRecheck = 0

    file_info = read_num_events(infil)
    if not file_info:
        if verb:
            print("file empty.")
        fullRecheck = 1
        return 0
    else:
        eventType_dict = create_dict(eventTyps, file_info, verb, is_ee=ee)

        if fullRecheck:
            for key in eventType_dict:
                eventType_dict[key]['recount'] = 1
            if verb:
                print("Will recheck all")
        print(eventType_dict)
        return eventType_dict

def countPrep(in_dict, outfil, verbo, is_ee=False):
    if verbo:
        print("here")
        print(in_dict)
    for t in in_dict:
        if verbo:
            print(in_dict)
            print(t, ": ", "Recounting" if in_dict[t]['recount'] else "No Recount Needed")
    newCounts = countEvents([ky if in_dict[ky]['recount'] else '' for ky in in_dict], outfil, is_ee)
    return newCounts

def WriteItAll(eventsAndInfo, outf):
    print("printing updated counts")
    to_write = ''
    for ev in eventsAndInfo:
        to_write += ev + ','
        for info in eventsAndInfo[ev]:
            if info != 'recount':
                to_write += str(eventsAndInfo[ev][info]) + ','
        to_write = to_write[:-1] + '\n'
    print("I'm writing ", to_write)
    outf.write(to_write)

    return eventsAndInfo

def what_to_do_if_empty(ev_t):
    full_dict = {}
    for typ in ev_t:
        full_dict.update({typ:{'runs':0, 'events':0, 'recount':1}})
    return full_dict
    
def redoCounts(eT, fullcheck=0, ee=False):
    additional = 'ee_' if ee else ''
    filename = '/home/dkennedy_umass_edu/LNV/MyFiles/LFVLNV/GenerationFiles/'+ additional + 'event_counts.txt'
    infile = open(filename, 'r')
    print('opening ', filename)
    quick_out = quick_check(eT, infile, verb=True, ee=ee)
    is_empty = False
    if not quick_out:
        is_empty = True
        quick_out = what_to_do_if_empty(eT)
        
    if fullcheck or is_empty:
        for key in quick_out:
            quick_out[key]['recount'] = 1
        print("Will recheck all")
    infile.close()
    outfile = open(filename, 'w')    
    newCounts = countPrep(quick_out, outfile, True, is_ee=ee)
    for typ in newCounts:
        quick_out[typ].update({'events':int(newCounts[typ]['events'])})
        quick_out[typ].update({'runs':int(newCounts[typ]['runs'])})
    final_dict = WriteItAll(quick_out, outfile)
    outfile.close()
    return final_dict

if __name__ == '__main__':

    fullRecheck = 1
    eventTypes = ['ZZ2j', 'WZ2j', 'ttbar', 'W3j', 'LNVF']
    redoCounts(eventTypes, fullRecheck)    
   