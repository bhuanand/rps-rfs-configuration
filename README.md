# rps-rfs-configuration
A script for configuring the Receive Packet Steering (RPS) and Receive Flow Steering (RFS) on linux

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
#```
