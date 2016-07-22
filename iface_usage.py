__author__ = 'Serhii Sheiko'
# MIT licence
import subprocess
import sys

# vnstat -tr 3 -i eth0
base_command = ['vnstat']

def help_message():
    help_msg = '''Interface usage plugin.
Requirements: vnstat
params:
-i - interface
-t - time for checking in seconds
-rx - limitations for input trafic
-tx - limitations for output trafic
for limitations warning and critical edge sepatated by comma. ex: 10,20
example:
iface_usage.py -i eth0 -t 3 -rx 10,20 -tx 10,20'''
    print()

def get_parameters():
    all_params = sys.argv
    run_params = []
    check_params = {}
    pass_iteration = False
    for i in range(0, len(all_params)):
        if pass_iteration == True:
            pass_iteration = False
            continue
        if all_params[i] == '-i':
            #run_params.append('-i ' + all_params[i+1])
            run_params.append('-i')
            run_params.append(all_params[i+1])
            pass_iteration = True
        elif all_params[i] == '-t':
            #run_params.append('-tr ' + all_params[i+1])
            run_params.append('-tr')
            run_params.append(all_params[i+1])
            pass_iteration = True
        elif all_params[i] == '-rx':
            check_params['rx'] = all_params[i+1]
            pass_iteration = True
        elif all_params[i] == '-tx':
            check_params['tx'] = all_params[i+1]
            pass_iteration = True
    return run_params, check_params

def get_output(run_params):
    run_command = base_command + run_params
    p = subprocess.Popen(run_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    out_data, out_err = p.communicate()
    if out_err is not None:
        print(out_err)
        sys.exit(128)
    splited_data = out_data.splitlines()
    result_data = {}
    for line in splited_data:
        if len(line.split())>1:
            if line.split()[0] == 'rx':
                if line.split()[2] == 'Mbit/s':
                    result_data['rx'] = float(line.split()[1].replace(',', '.')) * 1024
                else:
                    result_data['rx'] = float(line.split()[1].replace(',', '.'))
            elif line.split()[0] == 'tx':
                if line.split()[2] == 'Mbit/s':
                    result_data['tx'] = float(line.split()[1].replace(',', '.')) * 1024
                else:
                    result_data['tx'] = float(line.split()[1].replace(',', '.'))
    return result_data

def check_data(params_in):
    run_params, check_params = params_in
    output_data = get_output(run_params)
    result_string = 'Bandwitch usage: '
    error_code = 0
    for c_param in check_params:
        if not output_data.has_key(c_param):
            result_string = result_string + c_param + ' is unknown parameter; '
            continue
        control_data = check_params[c_param].split(',')
        warn_level = float(control_data[0])
        critical_level = float(control_data[1])
        result_data = float(output_data[c_param])
        if result_data > warn_level and result_data < critical_level:
            result_string = result_string + c_param + ': ' + str(result_data) + ' kbit/s warning; '
            if 1 > error_code:
                error_code = 1
        elif result_data > critical_level:
            result_string = result_string + c_param + ': ' + str(result_data) + ' kbit/s critical; '
            if 2 > error_code:
                error_code = 2
        else:
            result_string = result_string + c_param + ': ' + str(result_data) + ' kbit/s OK; '

    print(result_string)
    sys.exit(error_code)

check_data(get_parameters())
