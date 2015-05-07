#!/bin/sh
# file: test.sh
# vim:fileencoding=utf-8:ft=sh
#
# Author: R.F. Smith <rsmith@xs4all.nl>
# Created: 2015-04-06 16:06:32 +0200
# $Date$
# $Revision$

../onepad.py enc plain.txt foo.key >enc.txt
../onepad.py dec enc.txt foo >res.txt
diff -Bu plain.txt res.txt
if [ $? -ne 0 ]; then
    echo "Test failed!"
else
    echo "Test succeeded!"
fi
rm -f enc.txt res.txt
