# coding=utf-8

import sys
import json
from vm import vm, record

def filter_vm_list(vm_list, search):
    for vm in vm_list[:]:
        if vm['name'].lower().find(search.lower()) < 0 :
            vm_list.remove(vm)
    return vm_list

def sort_vm_list(vm_list, list):
    map = {}
    for i, line in enumerate(list):
        map[line] = i

    for vm in vm_list:
        if vm['uuid'] in map:
            vm['index'] = map[vm['uuid']]
        else:
            vm['index'] = sys.maxsize

    vm_list = sorted(vm_list, key=lambda x:x['index'])

    return vm_list

def output(vm_list):
    items = []
    for vm in vm_list:
        items.append({
            'title': vm['name'],
            'subtitle': 'Shutdown【save state】' if vm['is_running'] else 'Start【running background】',
            "icon": {
                "path": "./images/shutdown.png" if vm['is_running'] else "./images/running.png",
            },
            'arg': vm['uuid'],
            'variables': {
                "status": 'shutdown' if vm['is_running'] else 'start',
                "type": 'savestate' if vm['is_running'] else 'headless',
            },

            'mods': {
                'cmd': {
                    "subtitle": "Shutdown【normal】" if vm['is_running'] else "Start【show window】",
                    'variables': {
                        "status": 'shutdown' if vm['is_running'] else 'start',
                        "type": 'acpipowerbutton' if vm['is_running'] else 'gui',
                    },
                },
                'alt': {
                    "subtitle": "Shutdown【power off】" if vm['is_running'] else "Start【show window】",
                    'variables': {
                        "status": 'shutdown' if vm['is_running'] else 'start',
                        "type": 'poweroff' if vm['is_running'] else 'gui',
                    },
                }
            },

            'text': {
                'copy': 'VBoxManage controlvm '+vm['name']+' savestate' if vm['is_running'] else 'VBoxManage startvm '+vm['name']+' --type headless',
                'largetype': 'VBoxManage controlvm '+vm['name']+' savestate' if vm['is_running'] else 'VBoxManage startvm '+vm['name']+' --type headless',
            }
        })

    if len(items) <= 0:
        items = [{
            'title': 'Machine not found.',
            'subtitle': ''
        }]

    data = { 'items': items }
    return json.dumps(data)

if len(sys.argv) == 1:
    vm_list = vm.get_vm_list()
    list = record.get()
    vm_list = sort_vm_list(vm_list, list)
else:
    search = sys.argv[1]
    vm_list = vm.get_vm_list()
    list = record.get()
    vm_list = sort_vm_list(vm_list, list)
    vm_list = filter_vm_list(vm_list, search)

print(output(vm_list))
