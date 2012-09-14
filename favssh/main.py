# -*- coding: utf-8 -*-
from favssh.config import Configuration
import sys
import os
import re

def command_list(args):
    for host in args.config.all_hosts():
        print host

def command_show(args):
    for h in args.hosts:
        host = args.config.get_host(h)
        if host:
            print host
        else:
            print >> sys.stderr, "host '%s' not found" % h


def command_grep(args):
    pattern = re.compile(args.pattern, re.I)
    for host in args.config.all_hosts():
        if pattern.search(str(host)):
            print host

def command_add(args):
    args.config.add_host(args.host, hostname=args.hostname, user=args.user, port=args.port)
    args.config.write()

def command_remove(args):
    args.config.remove_host(args.host)
    args.config.write()

def command_update(args):
    args.config.update_host(args.host, args.key, args.value)
    args.config.write()

def main():
    import argparse
    parser =  argparse.ArgumentParser()
    parser.add_argument('-c', '--config-file', dest='config',
        default='~/.ssh/config', type=Configuration.from_argument)
    subparsers = parser.add_subparsers()
    
    parser_list = subparsers.add_parser('list')
    parser_list.set_defaults(func=command_list)
    
    parser_show = subparsers.add_parser('show')
    parser_show.add_argument('hosts', metavar='HOST', nargs='+')
    parser_show.set_defaults(func=command_show)

    parser_grep = subparsers.add_parser('grep')
    parser_grep.add_argument('pattern')
    parser_grep.set_defaults(func=command_grep)

    parser_add = subparsers.add_parser('add')
    parser_add.add_argument('host')
    parser_add.add_argument('hostname')
    parser_add.add_argument('-u', '--user', default=os.getlogin())
    parser_add.add_argument('-p', '--port', default=22, type=int)
    parser_add.set_defaults(func=command_add)
    
    parser_remove = subparsers.add_parser('remove')
    parser_remove.add_argument('host')
    parser_remove.set_defaults(func=command_remove)
    
    parser_add = subparsers.add_parser('update')
    parser_add.add_argument('host')
    parser_add.add_argument('key')
    parser_add.add_argument('value')
    parser_add.set_defaults(func=command_update)
    
    args = parser.parse_args()
    args.func(args)
