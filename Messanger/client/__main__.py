from argparse import ArgumentParser
import socket
import datetime
import logging
import jim
import settings


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

args = parser.parse_args()

if args.addr:
    host = args.addr
if args.port:
    port = args.port

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

    if args.mode == 'w':
        while True:
            action = input('Enter action to send:')
            data = input('Enter data to send:')

            msg = get_presence_msg(action, data)
            sock.sendall(msg)
    else:
        while True:
            response = sock.recv(settings.BUFFERSIZE)
            response = jim.unpack(response)
            logger.info(f'Got next response from server: {response}')
            print(f'Got next response from server: {response}')

except KeyboardInterrupt:
    logger.info('Client  closed')
    print('Client closed')



