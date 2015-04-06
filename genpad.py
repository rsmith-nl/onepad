#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Author: R.F. Smith <rsmith@xs4all.nl>
# $Date$
#
# To the extent possible under law, Roland Smith has waived all copyright and
# related or neighboring rights to genpad.py. This work is published from the
# Netherlands. See http://creativecommons.org/publicdomain/zero/1.0/

"""Generates a one time pad."""

import os
import sys
import base64


def genkey(length, chunklen=6, linelen=78):
    """Generates a one time pad.

    :length: minimum length of the key in bytes
    :returns: a string containing the base64 encoded key
    """
    rem = length % 6
    if rem:
        length += 6 - rem
    nchunks = int(length // chunklen)
    rem = length % chunklen
    n = int(linelen//(4*chunklen/3))
    nums = [chunklen]*nchunks + [rem]
    chunks = [base64.b64encode(os.urandom(j)).decode('ascii') for j in nums]
    lines = [' '.join(chunks[i:i+n]) for i in range(0, len(chunks), n)]
    return '\n'.join(lines)


def main(argv):
    """Main program.

    Arguments:
    :argv: command line arguments
    :returns: nothing
    """
    if len(argv) == 1:
        script = os.path.basename(argv[0])
        print("Usage: {} [length filename]".format(script))
        sys.exit(0)
    del argv[0]  # delete the name of the script.
    try:
        length = int(argv[0])
        if length < 0:
            raise ValueError
        filename = argv[1]
        ext = '.key'
        if not filename.endswith(ext):
            filename += ext
    except ValueError:
        s = 'The argument "{}" is not a valid positive integer'
        print(s.format(argv[0]))
        return
    except IndexError:
        print('No filename given.')
        return
    keystring = genkey(length)
    with open(filename, 'w+') as kf:
        kf.write(keystring)


if __name__ == '__main__':
    main(sys.argv)
