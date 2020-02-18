# rps-rfs-configuration
A script for configuring the Receive Packet Steering (RPS) and Receive Flow Steering (RFS) on linux

This script helps in configuring RPS and RFS on a linux machine and works as follows.
1. First it finds the number of CPU cores available on system
2. Finds the number of tx/rx queues available on specified interface
3. Finds the CPU core which is assigned to process the interrupts and handle packets for a tx/rx queue using `/proc/interrupts` output.
4. Configures the CPU mask for RPS based on CPU core set for a particular queue. 

For example, lets say rx-0 queue was assigned CPU core 0 and there are 8 cores available on system. 

if smp_affinity for rx-0 queue - CPU core '0' specified as mask '00000001' (from `/proc/interrupt` output)
then, RPS for rx-0 is configured as '11111110' - Which means interrupt is still handled by CPU core '0' but processing of packets is now distributed among CPU cores 1-7. This reduces load on CPU core '0' and promotes high PPS (packets per second)

Without RPS configuration, the CPU core '0' handles the soft_irq - interrupt generated when a packet is received on interface and also processes the packet - sending the packet to TCP/IP stack. On configuring RPS - this packet processing is offloaded to other cores.

5. RFS configuration is applied on top of RPS configuration

## Reference Links - RPS/RFS
1. https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/6/html/performance_tuning_guide/network-rps
2. https://balodeamit.blogspot.com/2013/10/receive-side-scaling-and-receive-packet.html
3. https://www.kernel.org/doc/Documentation/networking/scaling.txt
4. https://medium.com/@Pinterest_Engineering/building-pinterest-in-the-cloud-6c7280dcc196
5. https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/6/html/performance_tuning_guide/network-rfs

## Sample Usage
```
# python rps.py eth0 --configure-rfs
Number of CPU(s) available.. : 16
Number of queues in interface 'eth0'.. : 8
Mapping the corresponding TX queue to same CPU(s) as RX queue
Setting RPS CPU mask for /sys/class/net/eth0/queues/rx-1/rps_cpus as fbff
Setting RPS CPU mask for /sys/class/net/eth0/queues/tx-1/xps_cpus as fbff
Setting RPS CPU mask for /sys/class/net/eth0/queues/rx-0/rps_cpus as f7ff
Setting RPS CPU mask for /sys/class/net/eth0/queues/tx-0/xps_cpus as f7ff
Setting RPS CPU mask for /sys/class/net/eth0/queues/rx-3/rps_cpus as ff7f
Setting RPS CPU mask for /sys/class/net/eth0/queues/tx-3/xps_cpus as ff7f
Setting RPS CPU mask for /sys/class/net/eth0/queues/rx-2/rps_cpus as fdff
Setting RPS CPU mask for /sys/class/net/eth0/queues/tx-2/xps_cpus as fdff
Setting RPS CPU mask for /sys/class/net/eth0/queues/rx-5/rps_cpus as ffdf
Setting RPS CPU mask for /sys/class/net/eth0/queues/tx-5/xps_cpus as ffdf
Setting RPS CPU mask for /sys/class/net/eth0/queues/rx-4/rps_cpus as feff
Setting RPS CPU mask for /sys/class/net/eth0/queues/tx-4/xps_cpus as feff
Setting RPS CPU mask for /sys/class/net/eth0/queues/rx-7/rps_cpus as bfff
Setting RPS CPU mask for /sys/class/net/eth0/queues/tx-7/xps_cpus as bfff
Setting RPS CPU mask for /sys/class/net/eth0/queues/rx-6/rps_cpus as fff7
Setting RPS CPU mask for /sys/class/net/eth0/queues/tx-6/xps_cpus as fff7
Setting /proc/sys/net/core/rps_sock_flow_entries with value 32768
Configuring /sys/class/net/eth0/queues/rx-7/rps_flow_cnt with value 2048
Configuring /sys/class/net/eth0/queues/rx-5/rps_flow_cnt with value 2048
Configuring /sys/class/net/eth0/queues/rx-3/rps_flow_cnt with value 2048
Configuring /sys/class/net/eth0/queues/rx-1/rps_flow_cnt with value 2048
Configuring /sys/class/net/eth0/queues/rx-6/rps_flow_cnt with value 2048
Configuring /sys/class/net/eth0/queues/rx-4/rps_flow_cnt with value 2048
Configuring /sys/class/net/eth0/queues/rx-2/rps_flow_cnt with value 2048
Configuring /sys/class/net/eth0/queues/rx-0/rps_flow_cnt with value 2048
#
```

_*Note* You might want to update the regex in rps.py script which is used to match the interface queue in `/proc/interrupt` output. This is used to grab the queue number and associated CPU core handling the interrupt_
