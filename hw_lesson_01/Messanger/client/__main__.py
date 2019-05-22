from argparse import ArgumentParser
import socket
import datetime
import logging
import jim
import settings
import time


def get_presence_msg(action, data):
    time = datetime.datetime.now()
    msg = {
        "action": action,
        "time": time.isoformat(),
        "user": {
                "account_name":  "anonim",
                "status":      "Yep, I am here!"
        },
        "data": data
    }

    return jim.pack(msg)


host = getattr(settings, 'HOST', '127.0.0.1')
port = getattr(settings, 'PORT', 7777)

parser = ArgumentParser()
parser.add_argument('-a', '--addr', type=str, help='Sets ip address')
parser.add_argument('-p', '--port', type=int, help='Sets port')
parser.add_argument('-m', '--mode', type=str, default='w')
parser.add_argument('-t', '--action', type=str, help='Set action')
parser.add_argument('-d', '--data', type=str, help='Set data')
parser.add_argument('-c', '--count', type=int, help='Count for sends repeat')
parser.add_argument('-e', '--exit', type=str, help='Set "yes" if need to send exit msg when finalize')

args = parser.parse_args()

count_sends = -1

if args.addr:
    host = args.addr
if args.port:
    port = args.port
if args.count:
    count_sends = args.count

logger = logging.getLogger('main')
handler = logging.FileHandler('client.log', encoding=settings.ENCODING)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

handler.setLevel(logging.DEBUG)
handler.setFormatter(formatter)

logger.setLevel(logging.DEBUG)
logger.addHandler(handler)

try:
    sock = socket.socket()
    sock.connect((host, port))
    logger.info(f'Client started with {host}:{port}')
    print(f'Client started with {host}:{port}')

    is_continue = True
    i = 0

    if args.mode == 'w':
        while is_continue:
            if args.action:
                action = args.action
            else:
                action = input('Enter action to send:')

            if args.data:
                data = args.data
            else:
                data = input('Enter data to send:')
            if args.exit and i == count_sends - 1:
                msg = get_presence_msg('exit', 'exit')
            else:
                msg = get_presence_msg(action, data)
            print(msg)
            sock.sendall(msg)

            if args.action and args.data:
                time.sleep(10)

            i += 1
            if i == count_sends:
                is_continue = False

    else:
        while True:
            response = sock.recv(settings.BUFFERSIZE)
            response = jim.unpack(response)
            logger.info(f'Got next response from server: {response}')
            print(f'Got next response from server: {response}')
            if response['action'] == 'exit':
                break

except KeyboardInterrupt:
    logger.info('Client  closed')
    print('Client closed')



