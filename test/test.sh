#!/bin/sh
# file: test.sh
# vim:fileencoding=utf-8:ft=sh
#
# Author: R.F. Smith <rsmith@xs4all.nl>
# Created: 2015-04-06 16:06:32 +0200
# Last modified: 2015-05-17 12:04:05 +0200

echo "* Testing key randomness."
../genpad.py -l 1000 foo.key
./ent.py foo.key
rm -f foo.key

echo
echo "* Testing encryption/decryption."
../genpad.py foo.key
../onepad.py enc plain.txt foo.key >enc.txt
../onepad.py dec enc.txt foo.key >res.txt
diff -Bu plain.txt res.txt
if [ $? -ne 0 ]; then
    echo "Test failed!"
    rv=1
else
    echo "Test succeeded!"
    rv=0
fi
rm -f enc.txt res.txt foo.key
return $rv
