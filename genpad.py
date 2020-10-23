#!/usr/bin/env python3
# file: genpad.py
# vim:fileencoding=utf-8:ft=python
#
# Copyright © 2015 R.F. Smith <rsmith@xs4all.nl>. All rights reserved.
# Created: 2015-05-08 00:22:28 +0200
# Last modified: 2017-06-04 15:51:52 +0200
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY AUTHOR AND CONTRIBUTORS "AS IS" AND ANY EXPRESS
# OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
# OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.  IN
# NO EVENT SHALL AUTHOR OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA,
# OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,
# EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""Generate a one time pad and writes it to a file in base64 encoded form."""

import argparse
import base64
import logging
import os
import sys

__version__ = "2017.06.04"


def main(argv):
    """
    Entry point for genpad.

    Arguments:
        argv: command line arguments
    """
    logging.basicConfig(level="WARNING", format="%(levelname)s: %(message)s")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("-v", "--version", action="version", version=__version__)
    parser.add_argument(
        "-l",
        "--length",
        type=int,
        metavar="K",
        default=10,
        help="length of the key in kB (default 10)",
    )
    parser.add_argument("filename", type=str, help="name of the key-file.")
    args = parser.parse_args(argv)
    if args.length < 0:
        logging.error("Length must be a positive integer")
    keystring = genkey(args.length * 1024)
    if not args.filename.endswith(".key"):
        args.filename = args.filename + ".key"
    with open(args.filename, "w+") as kf:
        kf.write(keystring)


def genkey(length, chunklen=6, linelen=78):
    """
    Generate a one time pad.

    Arguments:
        length: Minimum length of the key in bytes.
        chuncklen: Length of the key segments (default 6 characters).
        linelen: Length of the output lines (default 78 characters).

    Returns:
        A string containing the base64 encoded key.
    """
    rem = length % 6
    if rem:
        length += 6 - rem
    nchunks = int(length // chunklen)
    rem = length % chunklen
    n = int(linelen // (4 * chunklen / 3))
    nums = [chunklen] * nchunks + [rem]
    chunks = [base64.b64encode(os.urandom(j)).decode("ascii") for j in nums]
    lines = [" ".join(chunks[i : i + n]) for i in range(0, len(chunks), n)]
    return "\n".join(lines)


if __name__ == "__main__":
    main(sys.argv[1:])
