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
version="0.26t"

def get_trackstats(file="career.txt"):
    """
    Get all valid trackstat records from a CCH file (argument)
    Has rudimentary error checking
    Returns: Array containing valid PLAYERTRACKSTAT sections
    """

    try:
        fh = open(file, "r")
    except:
        print("couldn't open file %s" % file)
        sys.exit(1)

    data = fh.readlines()
    new_data=[]
    for l in data: # filter new "CRL" Lines
        if l.find("CRL")>=0:
            new_data.append("")
            #next  that messes up the linecount in error reports
        else:
            new_data.append(l)

    result = []
    trackstats = []
    linecount=0
    for l in new_data:
        if l.startswith('[PLAYERTRACKSTAT]'):

            try:
                # get the number of classrecord entries
                count=3 # initial index (ignore TrackName / TrackFile lines)
                while new_data[linecount+count].find("ClassRecord") != -1:
                    count+=1

                # sanity check for keywords TrackName, ClassRecord
                if new_data[linecount+1].find("TrackName") == -1 or new_data[linecount+3].find("ClassRecord") == -1:
                    err_line = linecount
                    print("""
WARNING: Something's wrong with a PLAYERTRACKSTAT entry
in file %s at line %d, please check.
Keywords "TrackName" and / or "ClassRecord" not found
where I expected them:
                    """ % (file, err_line+1))
                    #print lines of current PLAYERTRACKSTAT down to next PLAYERTRACKSTAT line
                    while not new_data[err_line+1].startswith('[PLAYERTRACKSTAT]'):
                      print("%d: %s" % (err_line+1, new_data[err_line]), end='')
                      err_line+=1
                    print("%d: %s" % (err_line+1, new_data[err_line]), end='')
                    err_line+=1
                    print("%d: %s" % (err_line+1, new_data[err_line]))
                    #return [] # or could get the rest of the data...
                    next
            except IndexError:
                print("Aborting: Something's wrong with the record in file %s at line %d, please check." % (file, linecount))
                sys.exit(1)
            trackstats.append(new_data[linecount:linecount+count]) # only if it passed



        linecount+=1


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

