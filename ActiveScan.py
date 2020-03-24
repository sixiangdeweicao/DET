#!/usr/bin/python3.6
# encoding:utf-8
import subprocess, os,json, time
from AddrsToSeq import get_rawIP


def Scan(addr_set, source_ip, output_file, tid):
    """
    运用扫描工具检测addr_set地址集中的活跃地址

    Args：
        addr_set：待扫描的地址集合
        source_ip
        output_file
        tid:扫描的线程id

    Return：
        active_addrs：活跃地址集合
    """

    scan_input = output_file + '/zmap/scan_input_{}.txt'.format(tid)
    scan_output = output_file + '/zmap/scan_output_{}.txt'.format(tid)

    with open(scan_input, 'w', encoding = 'utf-8') as f:
        for addr in addr_set:
            f.write(addr + '\n')

    active_addrs = set()
    command = 'sudo zmap --ipv6-source-ip={} --ipv6-target-file={} -M icmp6_echoscan -p 80 -q -o {}'\
    .format(source_ip, scan_input, scan_output)
    print('[+]Scanning {} addresses...'.format(len(addr_set)))
    t_start = time.time()
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    # ret = p.poll()
    while p.poll() == None:
        pass

    if p.poll() is 0:
        # with open(output_file, 'a', encoding='utf-8') as f:
        # time.sleep(1)
        for line in open(scan_output):
            if line != '':
                active_addrs.add(line[0:len(line) - 1])
                    # f.write(line)
            
    print('[+]Over! Scanning duration:{} s'.format(time.time() - t_start))
    print('[+]{} active addresses detected!'
        .format(len(active_addrs)))
    return active_addrs



if __name__ == '__main__':
    addr_set = set()
    addr_set.add('2400:da00:2::29')
    addr_set.add('2404:0:8f82:a::201e')
    addr_set.add('2404:0:8e04:9::201e')
    Scan(addr_set)
    print('Over!')
