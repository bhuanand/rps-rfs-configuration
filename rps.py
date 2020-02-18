#!/usr/bin/env python

import argparse
import os
import re
import shlex
from subprocess import Popen, PIPE
import sys

def execute_command(cmd):
    proc = Popen(shlex.split(cmd), stdout=PIPE)
    return proc.communicate()[0].strip()

RPS_XPS_CONFIG_PATH   = "/sys/class/net/{iface}/queues/{q}/{config}"
RPS_SOCK_FLOW_ENTRIES = "/proc/sys/net/core/rps_sock_flow_entries"
RPS_FLOW_COUNT = "/sys/class/net/{iface}/queues/{q}/rps_flow_cnt"
SMP_AFFINITY = "/proc/irq/{irq}/smp_affinity"
NUM_CPUS = None

def numcpus():
    global NUM_CPUS
    if not NUM_CPUS:
        NUM_CPUS = int(execute_command("nproc"))

    return NUM_CPUS

def iface_queues(iface, qtype="rx"):
    qs = os.listdir(
        "/sys/class/net/{iface}/queues".format(iface=iface)
    )
    return [q for q in qs if q.startswith(qtype)]

def irq_cpu_map(iface, qtype="rx"):
    p1 = Popen(shlex.split("cat /proc/interrupts"), stdout=PIPE)
    p2 = Popen(shlex.split("egrep -i \"CPU|{}\"".format(iface)), stdin=p1.stdout, stdout=PIPE)
    info = p2.communicate()[0].strip()

    def irq(data):
        return data[0].split(":")[0]

    def queue(data):
        m = re.match("{}-tx-rx-(?P<queue>\d+)".format(iface),
                     data[-1],
                     flags=re.IGNORECASE
        )
        return m.groupdict()["queue"] if m else None

    irq_map = dict()
    for line in info.splitlines():
        line = line.lower()
        if re.search(iface, line) and re.search(qtype, line):
            # sample -> 27: * eth0-Tx-Rx-0
            data = line.split()
            irqnum, q = irq(data), queue(data)
            if irqnum and q:
                irq_map[q] = irqnum

    return irq_map

def irq_smp_affinity(irq):
    with open(SMP_AFFINITY.format(irq=irq), "r") as fd:
        masks = fd.read().strip().split(",")
        return [int(mask, 16) for mask in masks]

def configure_rfs(iface, rps_sock_flow_entries=32768):
    print("Setting {} with value {}".format(RPS_SOCK_FLOW_ENTRIES, rps_sock_flow_entries))

    with open(RPS_SOCK_FLOW_ENTRIES, "wb") as fd:
        fd.write("{}\n".format(rps_sock_flow_entries))

    rps_flow_cnt = rps_sock_flow_entries / numcpus()

    qs = iface_queues(iface, qtype="rx")
    for q in qs:
        path = RPS_FLOW_COUNT.format(iface=iface, q=q)
        print("Configuring {} with value {}".format(path, rps_flow_cnt))

        with open(path, "wb") as fd:
            fd.write("{}\n".format(rps_flow_cnt))

def configure_rps(iface):
    cpus = numcpus()
    print("Number of CPU(s) available.. : {}".format(cpus))

    qs = iface_queues(iface)
    print("Number of queues in interface '{}'.. : {}".format(iface, len(qs)))

    if cpus <= len(qs):
        print("Available CPU(s) <= rx queues.. Nothing to be done here")
        sys.exit(0)

    q_cpu_map = dict()
    for q, irq in irq_cpu_map(iface).items():
        masks = irq_smp_affinity(irq)
        available_cpus = cpus

        rps_cpus = list()
        for mask in masks:
            cur_cpus = min(available_cpus, 32)
            if cur_cpus:
                irq_cpu_mask = (2 ** cur_cpus) - 1
                rps_cpus.append(format(mask ^ irq_cpu_mask, 'x'))
                available_cpus -= cur_cpus

        q_cpu_map[q] = ",".join(rps_cpus)

    rps_xps_configs = [
        ("rx", "rps_cpus"),
        ("tx", "xps_cpus")
    ]

    print("Mapping the corresponding TX queue to same CPU(s) as RX queue")
    for q, mask in q_cpu_map.items():
        for qtype, config in rps_xps_configs:
            path = RPS_XPS_CONFIG_PATH.format(iface=iface, q="{}-{}".format(qtype, q), config=config)
            print("Setting RPS CPU mask for {} as {}".format(path, mask))

            with open(path, "wb") as fd:
                fd.write(mask + "\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script to setup RPS - Receiver Packet Steering on the specified interface")
    parser.add_argument("iface", type=str, help="Network adapter name")
    parser.add_argument("--configure-rfs", action="store_true", help="Configures RFS along with RPS")
    args = parser.parse_args(sys.argv[1:])
    configure_rps(args.iface)

    if args.configure_rfs:
        configure_rfs(args.iface)