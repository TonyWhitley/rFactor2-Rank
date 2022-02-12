#!/usr/bin/python
"""Put this python script into your rFactor2 UserData/Player directory
and run it using the python interpreter (double click should work if
Python is installed correctly).

If everything goes well, you should find a new file called
"career.blt" that you can then upload to rF2 Rank.  In case of
problems, feel free to contact us at isiforums.net (user "hoover").

"""
from __future__ import print_function  # Python 2 compatibility

import glob
import sys
import webbrowser

import parse_record_files

VERSION = "0.127.9t"


def create_file(filename="career.blt"):
    """Create a career.blt file from CCH files found in the current directoy"""
    try:
        out = open(filename, "w")
    except BaseException:
        print("Could not open career.blt for writing.")
        sys.exit(1)

    files = 0
    stats = 0

    for fname in glob.glob("*.cch"):
        files += 1
        track_stats = parse_record_files.get_trackstats(fname)
        if track_stats:
            stats += track_stats.count('[PLAYERTRACKSTAT]')
            out.write(track_stats)

    out.close()
    print(
        "%s created successfully from %d files (found %d track records)." %
        (filename, files, stats))


if __name__ == "__main__":
    print("create_file.py V%s (c) Uwe Schuerkamp, 2014-2018" % VERSION)
    print("Updated 2019-20 by https://forum.studio-397.com/index.php?members/seven-smiles.23088/")
    create_file("career.blt")

    print("Opening the rankings site...")
    URL = 'http://rf2.gplrank.de/'
    webbrowser.open(URL)

    input("Press ENTER to exit.")

    sys.exit(0)
