#!/usr/bin/env python3
# file: ent.py
# vim:fileencoding=utf-8:ft=python
#
# Author: R.F. Smith <rsmith@xs4all.nl>
# Created: 2012-08-25 23:37:50 +0200
# Last modified: 2015-06-04 21:20:47 +0200
#
"""
Partial implementation of the ‘ent’ program by John "Random" Walker in Python
using the numerical Python extension.

See http://www.fourmilab.ch/random/ for the original.
"""

from __future__ import division, print_function
from os.path import getsize
import argparse
import math
import sys
import numpy as np

__version__ = "0.5.0"


def main(argv):
    """
    Calculates and prints figures about the randomness of the input files.

    Arguments:
        argv: Program options.
    """
    opts = argparse.ArgumentParser(prog="ent", description=__doc__)
    opts.add_argument(
        "-c", action="store_true", help="print occurrence counts (not implemented yet)"
    )
    opts.add_argument("-t", action="store_true", help="terse output in CSV format")
    opts.add_argument("-v", "--version", action="version", version=__version__)
    opts.add_argument(
        "files", metavar="file", nargs="*", help="one or more files to process"
    )
    args = opts.parse_args(argv)
    for fname in args.files:
        data, cnts = readdata(fname)
        e = entropy(cnts)
        c = pearsonchisquare(cnts)
        p = pochisq(c)
        d = math.fabs(p * 100 - 50)
        try:
            scc = correlation(data)
            es = "{:.6f}".format(scc)
        except ValueError:
            es = "undefined"
        if args.t:
            terseout(fname, data, e, c, p, d, es)
        else:
            textout(fname, data, e, c, p, d, es)


def terseout(name, data, e, chi2, p, d, scc):
    """
    Print the results in terse CSV.
    """
    print("0,File-name,File-bytes,Entropy,Chi-square,Mean,Serial-Correlation")
    outs = "1,{},{},{:.6f},{:.2f},{:.4f},{}"
    print(outs.format(name, len(data), e, chi2, data.mean(), scc))


def textout(name, data, e, chi2, p, d, scc):
    """
    Print the results in plain text.
    """
    print('File "{}"'.format(name))
    print("- Entropy is {:.6f} bits per byte.".format(e))
    outs = "- Arithmetic mean value of data bytes is {:.4f}"
    print(outs.format(data.mean()), "(random = 127.5).")
    outs = "- χ² distribution for {} samples is {:.2f}, and randomly"
    print(outs.format(len(data), chi2))
    outs = "  would exceed this value {:.2f} percent of the times."
    print(outs.format(p * 100))
    print("  According to the χ² test, this sequence", end=" ")
    if d > 49:
        print("is almost certainly not random")
    elif d > 45:
        print("is suspected of being not random.")
    elif d > 40:
        print("is close to random, but not perfect.")
    else:
        print("looks random.")
    print("- Serial correlation coefficient is", scc, "(totally uncorrelated = 0.0).")


def readdata(name):
    """Read the data from a file and count how often each byte value
    occurs.

    Arguments:
        name: Path of the file to read

    Returns:
        data: numpy array containing the byte values.
        cnts: numpy array containing the occurance of each byte.
    """
    data = np.fromfile(name, np.ubyte)
    cnts = np.bincount(data)
    return data, cnts


def entropy(counts):
    """
    Calculate the entropy of the data represented by the counts array. Returns
    the entropy in bits per byte.

    Arguments:
        counts: numpy array of counts for all byte values.
    """
    counts = np.trim_zeros(np.sort(counts))
    sz = sum(counts)
    p = counts / sz
    ent = -sum(p * np.log(p) / math.log(256))
    return ent * 8


def pearsonchisquare(counts):
    """
    Calculate Pearson's χ² (chi square) test for an array of bytes. See
    [http://en.wikipedia.org/wiki/Pearson%27s_chi-squared_test
    #Discrete_uniform_distribution]

    Arguments:
        counts: Numpy array of counts.

    Returns:
        χ² value
    """
    np = sum(counts) / 256
    return sum((counts - np) ** 2 / np)


def correlation(d):
    """
    Calculate the serial correlation coefficient of the data.

    Arguments:
        d: numpy array of unsigned byte values.

    Returns:
        Serial correlation coeffiecient.
    """
    totalc = len(d)
    a = np.array(d, np.float64)
    b = np.roll(a, -1)
    scct1 = np.sum(a * b)
    scct2 = np.sum(a) ** 2
    scct3 = np.sum(a * a)
    scc = totalc * scct3 - scct2
    if scc == 0:
        raise ValueError
    scc = (totalc * scct1 - scct2) / scc
    return scc


def poz(z):
    """
    Probability of normal z value.
    Adapted from http://en.wikipedia.org/wiki/Normal_distribution,
    integration by parts of cumulative distribution function.

    Arguments:
        z: normal z value

    Returns:
        Cumulative probability from -∞ to z.
    """
    if z > 3:
        return 1
    elif z < -3:
        return 0
    cnt = 10  # number of expansion elements to use.
    exp = np.array([2 * i + 1 for i in range(0, cnt + 1)])
    za = np.ones(cnt + 1) * z
    num = np.power(za, exp)
    denum = np.cumprod(exp)
    fact = math.exp(-z * z / 2) / math.sqrt(2 * math.pi)
    return 0.5 + fact * np.sum(num / denum)


def pochisq(x, df=255):
    """
    Compute probability of χ² test value. Adapted from: Hill, I. D. and Pike,
    M. C.  Algorithm 299 Collected Algorithms for the CACM 1967 p. 243 Updated
    for rounding errors based on remark in ACM TOMS June 1985, page 185.

    According to http://www.fourmilab.ch/random/:

      We interpret the percentage (return value*100) as the degree to which
      the sequence tested is suspected of being non-random. If the percentage
      is greater than 99% or less than 1%, the sequence is almost certainly
      not random. If the percentage is between 99% and 95% or between 1% and
      5%, the sequence is suspect. Percentages between 90% and 95% and 5% and
      10% indicate the sequence is “almost suspect”.

    Arguments:
        x: Obtained chi-square value.
        df: Degrees of freedom, defaults to 255 for random bytes.

    Returns:
        The degree to which the sequence tested is suspected of being
        non-random.
    """
    # Check arguments first
    if not isinstance(df, int):
        raise ValueError("df must be an integer")
    if x <= 0.0 or df < 1:
        return 1.0
    # Constants
    LOG_SQRT_PI = 0.5723649429247000870717135  # log(√π)
    I_SQRT_PI = 0.5641895835477562869480795  # 1/√π
    BIGX = 20.0
    a = 0.5 * x
    ev = df % 2 == 0

    # Helper functions.

    def even(t, f):
        if ev:
            return t
        return f

    def ex(x):
        if x < -BIGX:
            return 0.0
        return math.exp(x)

    if df > 1:
        y = ex(-a)
    s = even(y, 2.0 * poz(-math.sqrt(x)))
    if df > 2:
        x = 0.5 * (df - 1.0)
        z = even(1.0, 0.5)
        if a > BIGX:
            e = even(0, LOG_SQRT_PI)
            c = math.log(a)
            while z <= x:
                e = math.log(z) + e
                s += ex(c * z - a - e)
                z += 1.0
            return s
        else:
            e = even(1.0, I_SQRT_PI / math.sqrt(a))
            c = 0.0
            while z <= x:
                e = e * a / z
                c = c + e
                z += 1.0
            return c * y + s
    else:
        return s


if __name__ == "__main__":
    main(sys.argv[1:])
