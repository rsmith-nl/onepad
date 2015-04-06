======
Onepad
======
:Author: Roland Smith
:Date: $Date$
:Revision: $Revision$

Introduction
============

The ``onepad.py`` script is a program to use binary `one-time pads`_. This is
a port and simplification of a previous version written in C.

.. _one-time pads: http://en.wikipedia.org/wiki/One-time_pad

How it works
============

The onepad program reads a file and a key and then combines them using the
exclusive-or (xor) operation. The resulting data is written to standard
output.

Key files and encrypted files are stored as base64 encoded text.

Plaintext is compressed with BZ2 before encryption. Cyphertext is likewise
decompressed after decryption.

Security
========

Keep in mind that this program was written as an exercise. In *theory*,
one-time pads offer perfect security if:

  * The used keys are *really* random.
  * Each key is only used only *once*.
  * The keys are only known to the sender and recipient.

In *practice* using e.g. public key cryptography is much more convenient and
probably more secure.

The ``genpad.py`` program gets the random data for the one-time pads from
``os.urandom``.  So wether the keys are usable depends on the underlying
implementation. *If implemented correctly* operating systems gather randomness
from unpredictable events like keystrokes, mouse movements and arriving
network packets. This can be used to (re-)seed a cryptographically secure
pseudorandom number generator. (CSPRNG_) But you should investigate the
quality of the keys before trusting them!

.. _CSPRNG: http://en.wikipedia.org/wiki/Cryptographically_secure_pseudorandom_number_generator

If a key is re-used, the one-time pad is transformed into a `running key
cipher`_, which is *much less* secure. Keys should be destroyed by e.g.
overwrtinging them with zeroes after use.

.. _running key cipher: http://en.wikipedia.org/wiki/Running_key_cipher

Since the keys are as long as the message, transporting them securely is a
problem. You could e.g. generate a lot of keys, burn them on a DVD and courier
that to the recipient. But this is only secure if the keys aren't copied in
transit. So in practice, using public key cryptography is much easier.
