import subprocess

#p = subprocess.Popen("python3 Messanger/server/__main__.py", shell=True, stdout=open('/dev/null'), stderr=open('/dev/null'))

p_read = subprocess.Popen("python3 Messanger/client/__main__.py -m r", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

p_write = subprocess.Popen("python3 Messanger/client/__main__.py -t echo -d Hello -c 2 -e yes", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


print('Send client output:')
print(p_write.stdout.read().decode())
print(p_write.stderr.read().decode())

print('Read client output:')
print(p_read.stdout.read().decode())
print(p_read.stderr.read().decode())

