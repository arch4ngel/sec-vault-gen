#!/usr/bin/env python3

from argparse import ArgumentParser
from lib.utils import (attack, lolbas, network_scan)
from logging import getLogger
from sys import exit

log = getLogger('main')

def stripArgs(args:dict, *fields):

    for field in fields:
        del(args[field])

if __name__ == '__main__':

    parser = ArgumentParser()

    # Always track util_cls and parser
      # util_cls = the utility class that will be executed
      # parser = the current parser, ensuring that the proper
        # help is displayed.
    parser.set_defaults(
        util_cls=None,
        parser=parser)
    subparsers = parser.add_subparsers()

    # ======
    # ATTACK
    # ======

    attack_p = subparsers.add_parser('mitre-attack',
        help='Parse, format, and output the MITRE ATT&CK framework '
            'for Obsidian.')
    attack_p.set_defaults(parser=attack_p)
    attack_sp = attack_p.add_subparsers()

    # BUILD ATT&CK
    attack_build_p = attack_sp.add_parser('build',
        help='Build the ATT&CK Framework directory. Save this in an '
            'Obsidian vault.',
        parents=(attack.Build.arg_parser,))

    attack_build_p.set_defaults(
        util_cls=attack.Build,
        parser=attack_build_p)

    # LINK INTO ATT&CK
    attack_link_p = attack_sp.add_parser('link',
        help='Link vault files into ATT&CK Framework files, allowing '
          'Obsidian to visualize related files.',
        parents=(attack.Link.arg_parser,))

    attack_link_p.set_defaults(
        util_cls=attack.Link,
        parser=attack_link_p)

    # ======
    # LOLBAS
    # ======

    lolbas_p = subparsers.add_parser('lolbas',
        help='Parse, format, and output LOLBAS for Obsidian.')
    lolbas_p.set_defaults(parser=lolbas_p)
    lolbas_sp = lolbas_p.add_subparsers()

    # BUILD LOLBAS
    lolbas_build_p = lolbas_sp.add_parser('build',
        help='Build the LOLBAS directory. Save this in an Obsidian '
          'vault.',
        parents=(lolbas.Build.arg_parser,))

    lolbas_build_p.set_defaults(
        util_cls=lolbas.Build,
        parser=lolbas_build_p)

    # ============
    # NETWORK SCAN
    # ============

    ns_p = subparsers.add_parser('network-scan',
        help='Parse and format Nmap and Nessus scans.')
    ns_p.set_defaults(parser=ns_p)
    ns_sp = ns_p.add_subparsers()

    # BUILD NETWORK SCAN
    ns_build_p = ns_sp.add_parser('build',
        help='Build the output from Nmap and Nessus scans.',
        parents=(network_scan.Build.arg_parser,))

    ns_build_p.set_defaults(
        util_cls=network_scan.Build,
        parser=ns_build_p)

    # ===================
    # PARSE THE ARGUMENTS
    # ===================

    args = parser.parse_args()

    if not args.util_cls:
        args.parser.print_help()
        exit()

    # Instantiate a utility
    util = args.util_cls()

    # Prepare an argument dictionary
    dargs = args.__dict__
    stripArgs(
        dargs, 'parser', 'util_cls'
    )

    log.info(f'Executing utility module: {util}')
    util(**dargs)
