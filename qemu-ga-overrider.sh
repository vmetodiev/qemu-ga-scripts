#!/bin/bash
CMD_GA='virsh qemu-agent-command '
CMD_LIBVIRT_LST='virsh list --all'

SH_INFO='{\"execute\":\"guest-info\"}'
SH_CPU='{\"execute\":\"guest-get-vcpus\"}'
SH_MEM_BLKS='{\"execute\":\"guest-get-memory-blocks\"}'
SH_MEM_BLK_INFO='{\"execute\":\"guest-get-memory-block-info\"}'

VM_NAME=$2
VM_NAME+=" " #append space char delimiter -> easier to concatenate the following part of the string


function vm_exists() {
     local vm_list=$CMD_LIBVIRT_LST
     eval $vm_list | grep "running" | grep $VM_NAME > /tmp/vm_exist.var
     local result='cat /tmp/vm_exist.var'
     if [[ $result ]]; then
	echo "" #Do nothing
     else
  	echo "string empty"
     fi
}

function show_cpus() {
     local result='cat /tmp/vm_exist.var'
     if [[ $result ]]; then
        local cpu_sh_var=$CMD_GA$VM_NAME$SH_CPU
	printf "Number of vCPUs being used:"
	eval $cpu_sh_var | cat -n | grep "logical-id" | awk '{ print $1 }'
	rm -f /tmp/vm_exist.var
     else
        echo "VM does not exist, exiting";
        exit;
     fi
}

function show_mem() {
     local result='cat /tmp/vm_exist.var'
     if [[ $result ]]; then
        local mem_blk_cmd=$CMD_GA$VM_NAME$SH_MEM_BLKS
	eval $mem_blk_cmd > /tmp/mem_blks_seperate
	local mem_blks="$(cat /tmp/mem_blks_seperate | grep -o \"phys-index\" -n | wc -l)"
	rm -f /tmp/mem_blks_seperate

	local mem_blk_size_cmd=$CMD_GA$VM_NAME$SH_MEM_BLK_INFO
	eval $mem_blk_size_cmd > /tmp/mem_blk_size
	local mem_blk_size="$(cat /tmp/mem_blk_size | tr -dc '0-9')"
	rm -f /tmp/mem_blk_size
     else
        echo "VM does not exist, exiting";
        exit;
     fi

     local mem_blk_size_mb=$(( $mem_blk_size / 1024 /  1024 ))
     local all_avail_mem=$(( $mem_blks * $mem_blk_size_mb))
     printf "Number of memory blocks:"; echo $mem_blks
     printf "Size of each memory block:"; echo $mem_blk_size_mb "mbytes"
     printf "Available memory for VM:"; echo $all_avail_mem "mbytes"

     rm -f /tmp/vm_exist.var
}

function echo_usage() {
    echo "Usage: ./ga-overrider.sh -n <vm_name> -o <operation>"
    echo "<operation>:"
    echo "      showcpus - Shows vCPU(s) used by VM"
    echo "      showmem  - Show memory information"
}

#Before going any further, check if VM exists
vm_exists;

if [ $1 = "-h" ] 
then
   echo_usage;
fi

if [ $1 = "-n" ]; then
    if [ $3 =  "-o" ]; then
	if [ $4 = "showcpus" ] 
	then
           show_cpus;
        fi

        if [ $4 = "showmem" ] 
        then
	   show_mem;
        fi

    else
        exit;
    fi
else
    echo_usage;
    exit;
fi

exit 0;
