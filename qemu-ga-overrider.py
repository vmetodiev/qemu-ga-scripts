#!/usr/bin/python

from subprocess import call
import os
import json
import sys

# Guest Agent Monitoring features
class GA_Monitor(object):
    # Define base strings
    CMD_GA = 'virsh qemu-agent-command'
    CMD_LIBVIRT_LST = 'virsh list --all'
    SPACE = ' '
    DELIMITER_BEGN = '\"name\"'
    DELIMITER_END = '\",\"'

    SH_INFO = '{"execute":"guest-info"}'
    SH_CPU = '{"execute":"guest-get-vcpus"}'
    SH_MEM_BLKS = '{"execute":"guest-get-memory-blocks"}'
    SH_MEM_BLK_INFO = '{"execute":"guest-get-memory-block-info"}'    

    def __init__(self):
        pass

    def show_cpus(self, vm_name):
	running = monitor._check_if_vm_running(vm_name)
        if running:
		print 'Number of vCPUs being used:',
		p = os.popen(self.CMD_GA + self.SPACE + vm_name + self.SPACE + json.dumps(self.SH_CPU))
        	output_str = p.readline()
		print output_str.count("logical-id")
	else:
		print 'VM not running, exiting'
		sys.exit()
	return

    def show_mem(self, vm_name):
        running = monitor._check_if_vm_running(vm_name)
	if running:
                p = os.popen(self.CMD_GA + self.SPACE + vm_name + self.SPACE + json.dumps(self.SH_MEM_BLKS))
                output_str = p.readline()
		mem_blks = output_str.count("phys-index")
		print("Number of memory blocks: %d" % mem_blks)
		
		p = os.popen(self.CMD_GA + self.SPACE + vm_name + self.SPACE + json.dumps(self.SH_MEM_BLK_INFO))
		del output_str
		output_str = p.readline()
		begn_ofs = output_str.find('\"size\"')
		mem_blk_size_str = output_str[begn_ofs + 7 : len(output_str) - 3]
		mem_blk_size = int(mem_blk_size_str)
		mem_blk_size_mb =  mem_blk_size / 1024 / 1024
		print("Size of each memory block: %d mbytes" % mem_blk_size_mb)	

		print("Available memory for VM: %d mbytes" % (mem_blk_size_mb * mem_blks))
	else:
		print 'VM not running, exiting'
		sys.exit()
        return

    def show_avaialbe_ops(self):
        p = os.popen(self.CMD_GA + self.SPACE + 'home_vm' + self.SPACE + json.dumps(self.SH_INFO))
	output_str = p.readline() 
	output_str = output_str.replace('success', '\n')
	output_str_lines = output_str.split()
	
	print 'Available Operations are from the QEMU-GA:',
	for line in output_str_lines:
		filter_begn = line.find(self.DELIMITER_BEGN) + len(self.DELIMITER_BEGN) + 2
		filter_end = line.find(self.DELIMITER_END) + 1
		print line[filter_begn : filter_end].replace('\"', '')

    def _check_if_vm_running(self, vm_name):
        p = os.popen(self.CMD_LIBVIRT_LST)
	while 1:
		line = p.readline()
		if not line: break
		if vm_name in line:
			if 'running' in line:
				return True
	return False

if __name__ == '__main__':
    args = len(sys.argv)
    cmd_args = str(sys.argv)
    
    monitor = GA_Monitor()

    if (args < 2):
	print 'Type this for help: \"python ga-overrider.py -h\"'
	sys.exit()

    if (sys.argv[1] == '-h'):
	print "Usage: python ga-overrider.py -n <vm_name> -o <operation>"
	print '<operation>:' + '\n' + 'showcpus - Shows vCPU(s) used by VM' + '\n' + 'showmem  - Shows memory used by VM'
	print '\n'
	monitor.show_avaialbe_ops()
	sys.exit()

    if (args == 5) and (sys.argv[4] == 'showcpus'):
	monitor.show_cpus(sys.argv[2])
	sys.exit()	

    if (args == 5) and (sys.argv[4] == 'showmem'):
	monitor.show_mem(sys.argv[2])
	sys.exit()
 
#END

