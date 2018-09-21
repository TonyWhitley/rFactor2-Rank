#!/usr/bin/python
"""Put this python script into your rFactor2 UserData/Player directory
and run it using the python interpreter (double click should work if
Python is installed correctly).

If everything goes well, you should find a new file called
"career.blt" that you can then upload to rF2 Rank.  In case of
problems, feel free to contact us at isiforums.net (user "hoover").

"""
from __future__ import print_function  # Python 2 compatibility

import glob,re,sys
version="0.27t"

maxErrorLineLength = 60 # Long entries in the cch file spoil the error message appearance

def get_trackstats(file="career.txt"):
    """
    Get all valid trackstat records from a CCH file (argument)
    Has rudimentary error checking
    Returns: Array containing valid PLAYERTRACKSTAT sections
    """
    wanted_lines = [
      '[PLAYERTRACKSTAT]',
      'TrackName',
      'TrackFile',
      'ClassRecord'
      ]
    try:
        fh = open(file, "r")
    except:
        print("couldn't open file %s" % file)
        sys.exit(1)

    data = fh.readlines()

    if 0:
      #simple
      trackstats = []
      for linecount, line in enumerate(data):
        for keyword in wanted_lines:
          if line.startswith(keyword):
            trackstats.append(line)
            break
    else:
      # with error checking
      trackstats = []
      trackstatBlocks = []
      for linecount, line in enumerate(data):
          if line.startswith('[PLAYERTRACKSTAT]'):
            trackstatBlocks.append(linecount)
      trackstatBlocks.append(len(data)) # the last one continues to the end of the file
         
      for block in range(len(trackstatBlocks)-1):
        trackstat = []
        for line in data[trackstatBlocks[block]:trackstatBlocks[block+1]]:
          for keyword in wanted_lines:
            if line.startswith(keyword):
              trackstat.append(line)
              break
        # sanity check for keywords TrackName, ClassRecord
        if len(trackstat) >= 4:
          if trackstat[0].startswith(wanted_lines[0]) and \
          trackstat[1].startswith(wanted_lines[1]) and \
          trackstat[2].startswith(wanted_lines[2]):
            #it's good
            trackstats.extend(trackstat)
            continue
        # it's bad
        err_line = trackstatBlocks[block]+1
        print("""
WARNING: Something's wrong with a PLAYERTRACKSTAT entry
in file %s at line %d, please check.
Keywords "TrackName" and / or "ClassRecord" not found
where I expected them:
        """ % (file, err_line))
        for line in data[trackstatBlocks[block]:trackstatBlocks[block+1]]:
          if len(line) > maxErrorLineLength:
            line = line[:maxErrorLineLength] + '...\n'
          print("%s:%d: %s" % (file, err_line, line), end='')
          err_line += 1
        print()

    return trackstats

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
        track_stats = get_trackstats(fname)
        if track_stats:
            for l in track_stats:
                stats+=1
                out.write("".join(l))

    out.close()
    print("%s created successfully from %d files (found %d track records)." % (filename, files, stats))

if __name__=="__main__":
    print("create_file.py V%s (c) Uwe Schuerkamp, 2014-" % version)
    create_file("career.blt")
    input("Press ENTER to exit.")

    sys.exit(0)

