# coding=utf-8

import sys
from vm import vm, record

def save(vm_all, uuid):
    list = record.get()
    vm_all = vm_all.copy()

    sorted_list = [ uuid ]
    del vm_all[uuid]

    for line in list:
        if line in vm_all:
            sorted_list.append(line)
            del vm_all[line]

    sorted_list += vm_all.keys()
    record.save(sorted_list)


uuid = sys.argv[1]
status = sys.argv[2]
type = sys.argv[3]

vm_all = vm.vm('vms')
save(vm_all, uuid)

if status == 'start' :
    res = vm.vm_start(uuid, type)
    vm_name = vm_all[uuid]
    print('It\'s running【'+vm_name+'】')
elif status == 'shutdown' :
    res = vm.vm_shutdown(uuid, type)
    vm_name = vm_all[uuid]
    print('Shutdown success【'+vm_name+'】')
else :
    del(sys.argv[0])
    print(sys.argv)
    #res = "invalid param: "+",".join(sys.argv)
    # print(res)

#print(res)
