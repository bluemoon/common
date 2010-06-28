#!/usr/bin/env python
# encoding: utf-8
"""
deterministic_random.py

Created by Bradford A Toney on 2010-06-28.
Copyright (c) 2010 __MyCompanyName__. All rights reserved.
"""

import sys
import common.mm_hash

# We expect the hash to be 4 bytes long
HASH_BYTES = 4
MAX_HASH_VALUE = 2**(8*HASH_BYTES)

_hasher = mm_hash.mumurHash
## If murmur2_neutral_32 and murmur2_32 give identical results for 1000
## numbers, then we'll assume they are interchangeable, and use murmur2_32
## which is faster.
#if [pyhash.murmur2_32()(`i`) for i in range(1000)] == [pyhash.murmur2_neutral_32()(`i`) for i in range(1000)]:
#    print >> sys.stderr, "Using pyhash.murmur2_32() optimization, since pyhash.murmur2_32 == pyhash.murmur2_neutral_32"
#    _hasher = pyhash.murmur2_32()
#else:
#    print >> sys.stderr, "UH-OH. Using pyhash.murmur2_neutral_32() to be safe, since pyhash.murmur2_32 != pyhash.murmur2_neutral_32"
#    _hasher = pyhash.murmur2_neutral_32()

def deterministicrandom(x):
    """
    Convert x (any Python value) to a deterministic uniform random number
    in [0, 1), with 32-bits of precision.

    TODO: Construct float value from 64-bits, not 32-bits.
    """

    i = hash_value(x)

    r = 1.0 * i / MAX_HASH_VALUE
    return r

def hash_value(x):
    """
    TODO: Make sure that we get a 4-byte value!!!
    """
    i = _hasher(`x`)
#    assert sys.sizeof(i) == HASH_BYTES
    assert i >= 0 and i < MAX_HASH_VALUE
    return i

assert [hash_value(i) for i in range(10)] == [1111412596, 1228156847, 772897149, 2292183779, 873905602, 1598865363, 1503201697, 3657602018, 194571672, 2418971295]
print >> sys.stderr, "Simple sanity check passed"

if __name__ == "__main__":
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("-s", "--stream", action="store_true", default=False, dest="stream", help="stream random numbers to stdout")
    (options, args) = parser.parse_args()
    assert len(args) == 0

    import os
    import struct
    # Make sure that packing to a struct of type L (standard unsigned long) is
    # 4 bytes, which is the length of the murmurhash output. (Actually,
    # we don't sanity check murmurhash length :( .)
    assert len(struct.unpack("cccc", struct.pack("=L", hash_value(0)))) == HASH_BYTES

    if not options.stream:
        array = [deterministicrandom(i) for i in range(1000)]
        import numpy
        print "mean (should be 0.5) = ", numpy.mean(array)

        print >> sys.stderr, "Writing 500000 bytes of random output to randomoutput.bin"
        f = open("randomoutput.bin", "wb")
        for i in range(1250000):
            f.write(struct.pack("=L", hash_value(i)))
        os.system("ent randomoutput.bin")
    else:
        i = 0
        import common.stats
        while 1:
            sys.stdout.write(struct.pack("=L", hash_value(i)))
            i += 1
#            if i % 1000000 == 0: print >> sys.stderr, i, common.stats.stats()

