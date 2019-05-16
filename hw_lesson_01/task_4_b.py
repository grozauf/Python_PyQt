import subprocess
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument('-r', '--readers', type=int, help='Count of readers')
parser.add_argument('-w', '--writers', type=int, help='Count of writers')

args = parser.parse_args()

readers_count = 1
writers_count = 1

if args.readers:
    readers_count = args.readers
if args.writers:
    writers_count = args.writers

readers_procs = []
writers_procs = []

for i in range(readers_count):
    p_read = subprocess.Popen("python3 Messanger/client/__main__.py -m r", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    readers_procs.append(p_read)


for i in range(writers_count):
    if i != writers_count - 1:
        p_write = subprocess.Popen("python3 Messanger/client/__main__.py -t echo -d Hello -c 2", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:
        p_write = subprocess.Popen("python3 Messanger/client/__main__.py -t echo -d Hello -c 2 -e yes", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    writers_procs.append(p_write)


for r_proc in readers_procs:
    print('Reader stdout:')
    print(r_proc.stdout.read().decode())
    print(r_proc.stderr.read().decode())

for w_proc in writers_procs:
    print('Writer stdout:')
    print(w_proc.stdout.read().decode())
    print(w_proc.stderr.read().decode())
