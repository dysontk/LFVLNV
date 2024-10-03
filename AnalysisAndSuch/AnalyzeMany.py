import subprocess

def run_command(command):
    try:
        output = subprocess.check_output(command, shell=True, encoding='utf8', stderr=subprocess.STDOUT)
        print(f"Output of command '{command}' is",  f'{output}', sep='\n')
    except subprocess.CalledProcessError:
        # print("Error. Generation probably failed")
        output = str(f"ERROR: Something when wrong when running {command}")
    return output


if __name__=='__main__':

    list_of_data_types = ['LNVF', 'WZ2j']
    Analyze = './JetFake/main '

    list_of_files = []

    for dtyp in list_of_data_types:
        theseFiles = run_command(f'ls /work/pi_mjrm_umass_edu/LNV_collider/Generated/{dtyp}/Events/*/*delphes_events.root')
        list_of_files.append(theseFiles.replace('\n', ' '))
        # print(theseFiles.replace('\n', ' '))


    for file in list_of_files:
        Analyze += file

    print('Running: ', Analyze, sep='\n')
    run_command(Analyze)