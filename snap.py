import os
from time import sleep
sourceRG = 'sourceRG'
destRG = 'destinationRG'
snapName = 'ss_eusa_'
osName=(os.popen('az vm list -g '+sourceRG+' --query "[].osProfile.computerName" -o tsv').read().strip()).split('\n')
vmList=(os.popen('az vm list -g '+sourceRG+' --query "[].name" -o tsv').read().strip()).split('\n')
map_dict = { 'node0':'idbeusadatap00',
  'node1':'datap01',
  'node2':'datap02',
  'node3':'datap03',
  'node4':'datap04',
  'node5':'datap05',
  'node6':'datap06',
  'node7':'datap07',
  'node8':'datap08',
  'node9':'datap09',
  'node10':'datap10',
  'node11':'datap11',
 }

bastvm = 'bast'
metavm = 'meta'


for x in vmList:
    if bastvm in x:
        vmList.remove(x)

for x in vmList:
    if metavm in x:
        vmList.remove(x)
vmList.remove('node1')
print vmList

for vmname in vmList:
		diskid=(os.popen('az vm show -g '+sourceRG+' -n '+vmname+' --query "storageProfile.dataDisks[*].managedDisk.id" -o tsv').read().strip()).split('\n')
		element = 'stage'
		for item in diskid:
    			if element in item:
        			diskid.remove(item)
		for disk in diskid:
			dname=disk.split('/')[-1]
			print "-----------------Creating SNAPSHOT for "+snapName+dname+"-------------------------"
			os.system('az snapshot create -g '+destRG+' --source '+disk+' --size-gb 1024 -l "East US" --name '+snapName+dname)
 			sleep(5)	
snapShots=os.popen('az snapshot list -g '+destRG+' --query "[].id" -o tsv').read().strip().split('\n')
for i in snapShots:
	src_host=(i.split('/')[-1]).split('_')[2]
        trg_host=map_dict[src_host]
	nameDisk=trg_host+'-'+'-'.join((i.split('/')[-1]).split('_')[3:])
	print "-----------------Creating Disk for "+nameDisk+" from "+i.split('/')[-1]+"-------------------------"
	os.system('az disk create -g '+destRG+' --source '+i+' --name '+nameDisk)
        sleep(5)
