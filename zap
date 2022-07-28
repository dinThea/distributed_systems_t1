#!/usr/bin/env python3
"""Entrypoint of cli client"""
from argparse import ArgumentParser
import re
from whatsapp.main.prompt import ExitCmdException, TopicPrompt

parser = ArgumentParser('To send some messages')
parser.add_argument('-s', '--serve', dest='serve', action='store_true')
parser.add_argument('-a', '--address', dest='address', type=str, help='Input Address')
parser.add_argument('-t', '--topic', dest='topic', type=str, help='Subscribe to an topic')
parser.add_argument('-u', '--user', dest='user', type=str, help='Login as a user')


def main():

    args = parser.parse_args()
    prompt = TopicPrompt()
    pattern = re.compile(r'(tcp:\/\/[a-zA-Z0-9]+):(\d{1,5})\-(\d{1,5})')

    if args.address:
        address, input_port, output_port = re.findall(pattern, args.address)[0]
        if args.serve:
            print(f'(Cmd) Serving as {address}:{input_port}-{output_port}')
            prompt.do_serve(f'{input_port} {output_port}')
        else:
            prompt.do_connect(f'{address} {input_port} {output_port}')
    if args.topic:
        prompt.do_enter_topic(args.topic)
    if args.user:
        prompt.do_set_user(args.user)

    try:
        prompt.cmdloop()
    except KeyboardInterrupt:
        print("(Cmd) Interrupted")
    except ExitCmdException as _:
        print("(Cmd) bye")


if __name__ == '__main__':
    main()
