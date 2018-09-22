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
version="0.27t (generator)"

maxErrorLineLength = 60 # Long entries in the cch file spoil the error message appearance

#iterator (not working, replaced with generator)
class IplayerTrackStat:
  def __init__(self, trackstats):
    self.trackstats = iter(trackstats)
  def __iter__(self):
    self._next = next(self.trackstats)
    return self
  def next(self):
    if self._next[1] == '[PLAYERTRACKSTAT]':
      _trackstat = self._next
      self._next = next(self.trackstats)
      while self._next != '[PLAYERTRACKSTAT]':
        _trackstat.append(self._next)
        self._next = next(self.trackstats)
      yield _trackstat

def playerTrackStat(trackstats):
  """ generator that gives one complete PLAYERTRACKSTAT """
  def getOneTrackstat(_trackstats, _first):
    _trackstat = [_first] # [linenum, '[PLAYERTRACKSTAT]']
    _next = next(_trackstats)
    try:
      while not _next[1].startswith('[PLAYERTRACKSTAT]'):
        _trackstat.append(_next)
        _next = next(_trackstats)
    except StopIteration:
      pass
    return _trackstat, _next

  _trackstats = iter(trackstats)
  _first = next(_trackstats)
  _trackstat, _first = getOneTrackstat(_trackstats, _first)
  while True:
    yield _trackstat
    _trackstat,_first = getOneTrackstat(_trackstats, _first)
  yield _trackstat

def get_trackstats(file="career.txt"):
    """
    Get all valid trackstat records from a CCH file (argument)
    Has rudimentary error checking
    Returns: Array containing valid PLAYERTRACKSTAT sections
    """
    def error(file, trackstat, originalFile):
      pass

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

    originalFile = []
    _trackstats = []
    for linecount, line in enumerate(fh):
      originalFile.append(line)
      for keyword in wanted_lines:
        if line.startswith(keyword):
          _trackstats.append((linecount, line))
          break # (keyword matched, no need to keep searching)

    results = []
    # Error checking
    z = playerTrackStat(_trackstats)
    _trackstatsList = list(z)
    for trackstat in _trackstatsList:
        # sanity check for keywords TrackName, TrackFile, ClassRecord
        if len(trackstat) >= 4:
          if trackstat[0][1].startswith(wanted_lines[0]) and \
          trackstat[1][1].startswith(wanted_lines[1]) and \
          trackstat[2][1].startswith(wanted_lines[2]):
            #it's good
            for line in trackstat:
              results.append(line[1])
            continue
        # it's bad
        err_line = trackstat[0][0]+1
        print("""
WARNING: Something's wrong with a PLAYERTRACKSTAT entry
in file %s at line %d, please check.
Keywords "TrackName" and / or "ClassRecord" not found
where I expected them:
        """ % (file, err_line))
        _lastline = trackstat[-1][0]+1 # the linenum of the last line in this trackstat
        for line in originalFile[trackstat[0][0]:_lastline]:
          if len(line) > maxErrorLineLength:
            line = line[:maxErrorLineLength] + '...\n'
          print("%s:%d: %s" % (file, err_line, line), end='')
          err_line += 1
        print()

    return results

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

