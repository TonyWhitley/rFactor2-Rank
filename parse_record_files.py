from __future__ import print_function  # Python 2 compatibility

import os
maxErrorLineLength = 60 # Long entries in the cch file spoil the error message appearance

errorText = """WARNING: Something's wrong with a PLAYERTRACKSTAT entry
in file %s at line %d, please check.
Keywords "TrackName" and / or "ClassRecord" not found
where I expected them.  This is the complete entry:
"""

class _playerTrackStat:
  """ Class that takes the text of a [PLAYERTRACKSTAT] section as a single string """
  lines = []    # the lines in the section
  parsed = None # the result text (Stays None if there are errors)
  error = None  # the error text (if there are any)

  def __init__(self, playerTrackStatText, cchFileName, lineNumberOfThisRecord):
    wanted_lines = [  # the entries we want to get
      'TrackName',
      'TrackFile',
      'ClassRecord'
      ]
    self.cchFileName = cchFileName
    self.lines = ['[PLAYERTRACKSTAT]']
    self.lines.extend(playerTrackStatText.split('\n')[:-1]) # Lose the blank line at the end
    _trackstat = ['[PLAYERTRACKSTAT]']
    for line in self.lines:
      for keyword in wanted_lines:
        if line.startswith(keyword):
          _trackstat.append(line)
          break

    # sanity check for keywords TrackName, TrackFile and ClassRecord
    try:
      assert _trackstat[1].startswith(wanted_lines[0])
      assert _trackstat[2].startswith(wanted_lines[1])
      assert _trackstat[3].startswith(wanted_lines[2])
      # parsed OK
      self.parsed = '\n'.join(_trackstat)+'\n'
      return

    except:    
      # else return error and self.parsed is None
      err_line = lineNumberOfThisRecord+1
      self.error = errorText % (cchFileName, err_line)
      # List lines from start of this block up (not including) to start of next
      for line in self.lines:
        if len(line) > maxErrorLineLength:
          # Long entries in the cch file spoil the error message appearance, trim them
          line = line[:maxErrorLineLength] + '...'
        self.error += "%s:%d: %s\n" % (cchFileName, err_line, line)
        err_line += 1

class cchFile:
  """ 
  Class that takes the text of a .cch file as a single string,
  splits it at [PLAYERTRACKSTAT] and processes each section separately.
  """
  recordsText = []    # The .cch file split into [PLAYERTRACKSTAT] sections
  recordResults = []  # The parsed result of each [PLAYERTRACKSTAT] section
  _records = []       # Each section as a list of lines (for unit testing)

  def __init__(self, cchFileText, cchFileName):
    self.recordsText = cchFileText.split('[PLAYERTRACKSTAT]\n')
    self.recordResults = [('all the [CAREER] stuff which we do not care about', 
                           'This is not used')]
    self._records = [self.recordsText[0].split('\n')[:-1]] # -1 to lose the blank line at the end
    lineNumberOfThisRecord = len(self._records[0]) # Lines in Header plus [CAREER] record

    for record in range(1, len(self.recordsText)):
      # Process each section
      playerTrackStat_o = _playerTrackStat(self.recordsText[record],
                                               cchFileName,
                                               lineNumberOfThisRecord)
      lineNumberOfThisRecord += len(playerTrackStat_o.lines)
      self._records.append(playerTrackStat_o.lines)
      self.recordResults.append((playerTrackStat_o.parsed, playerTrackStat_o.error))

  def get_career_blt_contribution(self):
    """ Return a string with all the trackstat records in the file """
    _career_blt = []
    for result in range(1, len(self.recordResults)):
      if self.recordResults[result][0]:
        _career_blt.append(self.recordResults[result][0])
    _result = ''.join(_career_blt)
    return _result

  def get_errors(self):
    """ Return a string with any errors in the file """
    _errors = []
    for result in range(1, len(self.recordResults)):
      if self.recordResults[result][0] == None:
        _errors.append(self.recordResults[result][1])
    _result = ''.join(_errors)
    return _result

def get_trackstats(cchFileName="career.txt"):
    """
    Get all valid trackstat records from a CCH file (argument)
    Has rudimentary error checking
    Returns: String containing valid PLAYERTRACKSTAT sections, e.g.
    """
    """
    [PLAYERTRACKSTAT]
    TrackName=MONTECARLO_1966
    TrackFile=C:\PROGRAM FILES (X86)\STEAM\STEAMAPPS\COMMON\RFACTOR 2\INSTALLED\LOCATIONS\MONTECARLO_1966\2.1\MONTECARLO_1966
    ClassRecord="*",6,95.6254,-1.0000,-1.0000
    ClassRecord="Brabham BT20",6,95.6254,-1.0000,-1.0000
    [PLAYERTRACKSTAT]
    TrackName=ROUEN 1955-70
    TrackFile=C:\PROGRAM FILES (X86)\STEAM\STEAMAPPS\COMMON\RFACTOR 2\INSTALLED\LOCATIONS\VLM_ROUEN-LES-ESSARTS_SJ.DD\0.97\ROUEN 1955-70
    ClassRecord="*",43,124.3666,-1.0000,124.3666
    ClassRecord="Ferrari 312/67 Ferrari 242 3.0 ",37,124.3666,-1.0000,124.3666
    ClassRecord="Brabham BT20",6,128.0244,-1.0000,128.0244
    """
    if not os.path.exists(cchFileName):
      print("couldn't open file %s" % cchFileName)
      sys.exit(1)
    with open(cchFileName, "r") as fh:
      originalText = fh.read() # get the whole file as a string
      cchFile_o = cchFile(originalText, cchFileName)
      _career_blt = cchFile_o.get_career_blt_contribution()
      _errors = cchFile_o.get_errors()
      if _errors != '':
        print(_errors)
      return _career_blt
    return None #?