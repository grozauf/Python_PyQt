import subprocess
from argparse import ArgumentParser
import ipaddress
from tabulate import tabulate


def host_range_ping_tab(host_range):
    dict_list = {'Reachable': list(), 'Unreachable': list()}
    ip1 = ipaddress.ip_address(host_range[0])
    ip2 = ipaddress.ip_address(host_range[1])
    if ip1 > ip2:
        ip1, ip2 = ip2, ip1

    while ip1 <= ip2:
        host = str(ip1)
        print(f'Проверяем на доступность хост {host}...')
        p = subprocess.run(["ping", host, "-c 2"], stdout=open('/dev/null'), stderr=open('/dev/null'))

        if p.returncode != 0:
            dict_list['Unreachable'].append(host)
        else:
            dict_list['Reachable'].append(host)

        ip1 += 1

    print(tabulate(dict_list, headers='keys', tablefmt='grid'))


parser = ArgumentParser()
parser.add_argument('-r', '--range', type=str, help='Sets range of ip addresses')

args = parser.parse_args()

range_str = ''

if args.range:
    range_str = args.range

host_range = range_str.split(',')
host_range = [host.strip(' ') for host in host_range]

if range_str == '':
    print('Задайте диапазон ip адресов, используя параметр -r "ip_begin, ip_end"')
elif len(host_range) != 2:
    print('Неверно задан диапазон ip адресов')
else:
    host_range_ping_tab(host_range)
