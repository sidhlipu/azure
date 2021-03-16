import os
from time import sleep
sourceRG = 'sentfastdb01eusprodentgroup'
destRG = 'rg-fastdbstore-eastus-prod-02'
snapName = 'ss_eusa_'
osName=(os.popen('az vm list -g '+sourceRG+' --query "[].osProfile.computerName" -o tsv').read().strip()).split('\n')
vmList=(os.popen('az vm list -g '+sourceRG+' --query "[].name" -o tsv').read().strip()).split('\n')
map_dict = { 'datanode0':'idbeusadatap00',
  'datanode1':'idbeusadatap01',
  'datanode2':'idbeusadatap02',
  'datanode3':'idbeusadatap03',
  'datanode4':'idbeusadatap04',
  'datanode5':'idbeusadatap05',
  'datanode6':'idbeusadatap06',
  'datanode7':'idbeusadatap07',
  'datanode8':'idbeusadatap08',
  'datanode9':'idbeusadatap09',
  'datanode10':'idbeusadatap10',
  'datanode11':'idbeusadatap11',
 }

bastvm = 'bast'
metavm = 'meta'


for x in vmList:
    if bastvm in x:
        vmList.remove(x)

for x in vmList:
    if metavm in x:
        vmList.remove(x)
vmList.remove('metanode1')
print vmList

#for vmname in vmList:
#		diskid=(os.popen('az vm show -g '+sourceRG+' -n '+vmname+' --query "storageProfile.dataDisks[*].managedDisk.id" -o tsv').read().strip()).split('\n')
#		element = 'stage'
#		for item in diskid:
#    			if element in item:
#        			diskid.remove(item)
#		for disk in diskid:
#			dname=disk.split('/')[-1]
#			print "-----------------Creating SNAPSHOT for "+snapName+dname+"-------------------------"
#			os.system('az snapshot create -g '+destRG+' --source '+disk+' --size-gb 1024 -l "East US" --name '+snapName+dname)
# 			sleep(5)	
snapShots=os.popen('az snapshot list -g '+destRG+' --query "[].id" -o tsv').read().strip().split('\n')
for i in snapShots:
	src_host=(i.split('/')[-1]).split('_')[2]
        trg_host=map_dict[src_host]
	nameDisk=trg_host+'-'+'-'.join((i.split('/')[-1]).split('_')[3:])
	print "-----------------Creating Disk for "+nameDisk+" from "+i.split('/')[-1]+"-------------------------"
	os.system('az disk create -g '+destRG+' --source '+i+' --name '+nameDisk)
        sleep(5)
