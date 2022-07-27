
import zmq


def main():
    ctx = zmq.Context.instance()

    publisher = ctx.socket(zmq.PUB)
    publisher.connect("tcp://localhost:6001")

    while True:
        message = input()
        print(f'PUBLISHING {message}')
        publisher.send(message.encode('utf-8'))


if __name__ == '__main__':
    main()
