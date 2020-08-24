#!/usr/bin/python3
import subprocess, collections

#Wrapper for shell command excecution
def exec_shell_command(command):
    proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    stdout,stderr = proc.communicate()
    if stderr:
        print(stderr)
    return stdout.decode()


def def_value():
    userdata = {}
    userdata['up'] = 0.0
    userdata['down'] = 0.0
    return userdata

traffic = collections.defaultdict(def_value)
command = "podman exec -it v2ppn v2ctl api --server=\"127.0.0.1:10085\" StatsService.QueryStats \'pattern: \"\" reset: false\'"
result = []
result = exec_shell_command(command).split('stat: <')

for stat in result[1:]:
    data = stat.split('\r\n')
    username = data[1].split('>>>')[1]
    traff = float(data[2].split('value:')[1])/1024/1024
    updown = data[1].split('>>>')[3][:-1]
    if updown == 'uplink':
        traffic[username]['up']=traff
    elif updown == 'downlink':
        traffic[username]['down']=traff

traff_sorted = {k:v for k, v in sorted(traffic.items(), key=lambda k_v: k_v[1]['down'], reverse=True)}
for k,v in traff_sorted.items():
    print('User: {:20}   Up: {:10.2f} MB   Down: {:10.2f} MB'.format(k,v['up'], v['down']))
