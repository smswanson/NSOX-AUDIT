from write2excel import writeDevice, buildtable, writetable
from datetime import date
from pullConfig import show_collection, getBackup
import login
from pprint import pprint
import json
# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
badFill = 'FFC7CE'
badFont = '9C0006'
goodFill = 'C6EFCE'
goodFont = '006100'
neutralFill = 'FFEB9C'
neutralFont = '9C5700'
normalFill = 'FFFFFF'
normalFont = '000000'

portTests = [{'data': 'connected', 'fill': goodFill, 'font': goodFont},
             {'data': 'notconnect', 'fill': neutralFill, 'font': neutralFont},
             {'data': 'suspnd', 'fill': badFill, 'font': badFont},
             {'data': 'noOperMem', 'fill': badFill, 'font': badFont},
             {'data': 'down', 'fill': badFill, 'font': badFont},
             {'data': 'errDisable', 'fill': badFill, 'font': badFont},]
portstatus = [{'key': 'state', 'test': portTests}]

def print_setup(time='0000'):
    # Use a breakpoint in the code line below to debug your script.
    version = '0.1'
    script_name = 'NXOS-Audit'
    #Set "True" if script is in testing mode
    test = True
    print(f'Running: {script_name}\nVersion: {version}')
    print(f'Date: {time}')
    if test:
        print('\nRunning in Test Mode\n')
    return test

def write_output(device, filetype='json'):
    datafile = device.name + '-' + device.serial + '.' + filetype
    print(f'Write Raw Data to {datafile} for {device.name}')
    try:
        with open(datafile, 'w') as outfile:
            json.dump(device.data, outfile)
    except:
        print(f'Error Writing {datafile}')

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    timestamp = str(date.today())
    test_mode = print_setup(timestamp)
    ssh_list = login.create_session(test_mode)
    device_list = []
    for s in ssh_list:
        ssh = s['session']
        ip = s['device']
        device = show_collection(ssh)
        backup_file = device.name + '-' + device.serial + '-' + timestamp + '.txt'
        running_cfg = getBackup(ssh, backup_file)
        print(f'Disconnecting SSH Session to {ip}')
        ssh.disconnect()
        #write_output(device)
        #writeDevice(device)
        device_list.append(device)
    filename = 'test0001.xlsx'
    if device_list == []:
        print('No Devices Accessed. Exiting...')
    else:
        nxosTable = buildtable(device_list, 'Nexus Switches')
        writetable(nxosTable, 'testoutput.xlsx')

        for a in device_list:
            portmapTable = buildtable(a.eth, 'Port-Map')
            writetable(portmapTable, 'Port-Map.xlsx', hl=True, TEST=portstatus) # Adds highlight information

