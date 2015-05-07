#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Author: R.F. Smith <rsmith@xs4all.nl>
# $Date$
#
# To the extent possible under law, Roland Smith has waived all copyright and
# related or neighboring rights to onepad.py. This work is published from the
# Netherlands. See http://creativecommons.org/publicdomain/zero/1.0/

"""Uses a one time pad to encrypt or decrypt a file."""

import os
import sys
import base64
import bz2


def decode(data):
    """Decode a formatted base64 keystring or an encrypted string.

    Arguments:
        data: Bytes to decode.
    Returns:
        The decoded input.
    """
    data = data.replace(b' ', b'').replace(b'\n', b'')
    return base64.b64decode(data)


def encode(data, chunklen=6, linelen=78):
    """Encode data with base64 and format it.

    Arguments:
        data: String to be encoded.
        chunklen: Number of bytes in a chunk, defaults to 6.
        linelen: Length of a line, defaults to 78 characters.

    Returns:
        The base64 encoded data.
    """
    length = len(data)
    n = int(linelen//(4*chunklen/3))
    chunks = [base64.b64encode(data[j:j+chunklen]).decode('ascii')
              for j in range(0, length, chunklen)]
    lines = [' '.join(chunks[i:i+n]) for i in range(0, len(chunks), n)]
    return '\n'.join(lines)


def main(argv):
    """Main program.

    Arguments:
        argv: command line arguments
    """
    if len(argv) == 1:
        script = os.path.basename(argv[0])
        print("Usage: {} (dec|enc) [datafile keyfile]".format(script))
        sys.exit(0)
    del argv[0]  # delete the name of the script.
    try:
        action = argv[0]
        if action not in ('enc', 'dec'):
            raise ValueError
        datafile = argv[1]
        keyfile = argv[2]
        ext = '.key'
        if not keyfile.endswith(ext):
            keyfile += ext
    except IndexError:
        print('Not enough arguments given.')
        return
    except ValueError:
        print('Command must be either "enc" or "dec".')
        return
    with open(datafile, 'rb') as df:
        data = df.read()
    with open(keyfile, 'rb') as kf:
        key = decode(kf.read())
    if action == 'dec':
        data = decode(data)
    else:
        # Compress before encryption. The slice removes the bz2 header.
        data = bz2.compress(data)[10:]
    if len(data) > len(key):
        print('ERROR: Message longer than the key.')
        return
    rv = bytes([i ^ j for i, j in zip(data, key)])
    if action == 'enc':
        rv = bytes(encode(rv), 'utf-8')
    else:
        # Decompress after decryption. Re-add bz2 header first.
        rv = bz2.decompress(b'BZh91AY&SY' + rv)
    print(rv.decode('utf-8'))

if __name__ == '__main__':
    main(sys.argv)
