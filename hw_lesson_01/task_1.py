import subprocess
from argparse import ArgumentParser


def host_ping(host_list):
    for host in host_list:
        print(f'Проверяем на доступность хост {host}...')
        p = subprocess.run(["ping", host, "-c 2"], stdout=open('/dev/null'), stderr=open('/dev/null'))

        if p.returncode != 0:
            print(f'Хост {host} недоступен')
        else:
            print((f'Хост {host} доступен'))


parser = ArgumentParser()
parser.add_argument('-a', '--addrs', type=str, help='Sets list of ip addresses or hostlists')

args = parser.parse_args()

hosts_str = ''

if args.addrs:
    hosts_str = args.addrs

host_list = hosts_str.split(',')
host_list = [host.strip(' ') for host in host_list]

if hosts_str == '':
    print('Задайте список хостов, используя параметр -a "host1, host2,..."')
else:
    host_ping(host_list)



