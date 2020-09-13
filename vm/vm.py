# coding=utf-8

import os
import re


def vm(param):
    res = os.popen('/usr/local/bin/vboxmanage list '+param)
    lines = res.read().splitlines()

    vm = {}
    for line in lines:
        m = re.match('^"(.+)" \{([^}]+)\}$', line)
        vm[m.group(2)] = m.group(1)

    return vm

def get_vm_list():
    vm_all = vm('vms')
    vm_running = vm('runningvms')

    vm_list = []
    for uuid, name in vm_all.items():
        vm_list.append({
            'uuid': uuid,
            'name': name,
            'is_running': uuid in vm_running
        })

    return vm_list

def vm_start(uuid, type):
    res = os.popen('/usr/local/bin/vboxmanage startvm '+uuid+' --type '+type)
    return res.read()

def vm_shutdown(uuid, type):
    res = os.popen('/usr/local/bin/vboxmanage controlvm '+uuid+' '+type)
    return res.read()
