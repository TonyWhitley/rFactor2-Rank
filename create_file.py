#!/usr/bin/python
"""Put this python script into your rFactor2 UserData/Player directory
and run it using the python interpreter (double click should work if
Python is installed correctly).

If everything goes well, you should find a new file called
"career.blt" that you can then upload to rF2 Rank.  In case of
problems, feel free to contact us at isiforums.net (user "hoover").

"""

import glob,re,sys
version="0.26"

def get_trackstats(file="career.txt"):
    """
    Get all valid trackstat records from a CCH file (argument)
    Has rudimentary error checking
    Returns: Array containing valid PLAYERTRACKSTAT sections
    """

    try:
        fh = open(file, "r")
    except:
        print "couldn't open file %s" % file
        sys.exit(1)

    data = fh.readlines()
    new_data=[]
    for l in data: # filter new "CRL" Lines
        if l.find("CRL")>=0:
            next
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

                trackstats.append(new_data[linecount:linecount+count])
                # sanity check for keywords TrackName, ClassRecord
                if new_data[linecount+1].find("TrackName") == -1 or new_data[linecount+3].find("ClassRecord") == -1:
                    print """
WARNING: Something's wrong with a PLAYERTRACKSTAT entry
in file %s at line %d, please check.
Error: Keywords "TrackName" and / or "ClassRecord" not found
where I expected them.
                    """ % (file, linecount)
                    return []
            except IndexError:
                print "Aborting: Something's wrong with the record in file %s at line %d, please check." % (file, linecount)
                sys.exit(1)



        linecount+=1


    return trackstats

def create_file(filename="career.blt"):
    """Create a career.blt file from CCH files found in the current directoy"""
    try:
        out = open(filename, "w")
    except:
        print "Could not open career.blt for writing."
        sys.exit(1)

    files = 0
    stats = 0

    for fname in glob.glob("*.cch"):
        files+=1
        track_stats = get_trackstats(fname)
        if track_stats:
            for l in track_stats:
                stats+=1
                print >>out, "".join(l)

    out.close()
    print "%s created successfully from %d files (found %d track records)." % (filename, files, stats)

if __name__=="__main__":
    print "create_file.py V%s (c) Uwe Schuerkamp, 2014-" % version
    create_file("career.blt")
    raw_input("Press ENTER to exit.")

    sys.exit(0)


