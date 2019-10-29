#!/usr/bin/python
"""Put this python script into your rFactor2 UserData/Player directory
and run it using the python interpreter (double click should work if
Python is installed correctly).

If everything goes well, you should find a new file called
"career.blt" that you can then upload to rF2 Rank.  In case of
problems, feel free to contact us at isiforums.net (user "hoover").

"""
from __future__ import print_function  # Python 2 compatibility

import glob,os,re,sys
import webbrowser

version="0.127.3t"

import parse_record_files

def create_file(filename="career.blt"):
    """Create a career.blt file from CCH files found in the current directoy"""
    try:
        out = open(filename, "w")
    except:
        print("Could not open career.blt for writing.")
        sys.exit(1)

    files = 0
    stats = 0

    for fname in glob.glob("*.cch"):
        files+=1
        track_stats = parse_record_files.get_trackstats(fname)
        if track_stats:
          stats += track_stats.count('[PLAYERTRACKSTAT]')
          out.write(track_stats)

    out.close()
    print("%s created successfully from %d files (found %d track records)." % (filename, files, stats))

if __name__=="__main__":
    print("create_file.py V%s (c) Uwe Schuerkamp, 2014-2018" % version)
    create_file("career.blt")

    print("Opening the rankings site...")
    url = 'http://rf2.gplrank.info/'
    webbrowser.open(url)

    input("Press ENTER to exit.")

    sys.exit(0)

