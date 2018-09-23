import os
maxErrorLineLength = 60 # Long entries in the cch file spoil the error message appearance


class cchFile:
  records = []
  recordsText = []
  recordResults = []

  class playerTrackStat:
    lines = []
    parsed = None
    error = None

    def __init__(self, playerTrackStatText, cchFileName, lineNumberOfThisRecord):
      wanted_lines = [
        'TrackName',
        'TrackFile',
        'ClassRecord'
        ]
      self.cchFileName = cchFileName
      self.lines = ['[PLAYERTRACKSTAT]']
      self.lines.extend(playerTrackStatText.split('\n')[:-1]) # Lose the blank line at the end
      trackstat = ['[PLAYERTRACKSTAT]']
      for line in self.lines:
        for keyword in wanted_lines:
          if line.startswith(keyword):
            trackstat.append(line)
            break
      if len(trackstat) >= 4:
        if trackstat[1].startswith(wanted_lines[0]) and \
        trackstat[2].startswith(wanted_lines[1]) and \
        trackstat[3].startswith(wanted_lines[2]):
          # parsed OK
          self.parsed = '\n'.join(trackstat)+'\n'
          return
      # else report error and self.parsed is None
      err_line = lineNumberOfThisRecord+1
      self.error = """WARNING: Something's wrong with a PLAYERTRACKSTAT entry
in file %s at line %d, please check.
Keywords "TrackName" and / or "ClassRecord" not found
where I expected them:
""" % (cchFileName, err_line)
      # List lines from start of this block up (not including) to start of next
      for line in self.lines:
        if len(line) > maxErrorLineLength:
          # Long entries in the cch file spoil the error message appearance, trim them
          line = line[:maxErrorLineLength] + '...'
        self.error += "%s:%d: %s\n" % (cchFileName, err_line, line)
        err_line += 1

  def __init__(self, cchFileText, cchFileName):
    self.recordResults = ['all the [CAREER] stuff']
    self.recordsText = cchFileText.split('[PLAYERTRACKSTAT]\n')
    self.records = [self.recordsText[0].split('\n')[:-1]] # Lose the blank line at the end
    lineNumberOfThisRecord = len(self.records[0]) # Lines in Header plus [CAREER] record
    for record in range(1, len(self.recordsText)):
      playerTrackStat_o = self.playerTrackStat(self.recordsText[record],
                                               cchFileName,
                                               lineNumberOfThisRecord)
      lineNumberOfThisRecord += len(playerTrackStat_o.lines)
      self.records.append(playerTrackStat_o.lines)
      self.recordResults.append((playerTrackStat_o.parsed, playerTrackStat_o.error))

  def get_career_blt_contribution(self):
    _career_blt = []
    for result in range(1, len(self.recordResults)):
      if self.recordResults[result][0]:
        _career_blt.append(self.recordResults[result][0])
    _result = ''.join(_career_blt)
    return _result

  def get_errors(self):
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
    Returns: Array containing valid PLAYERTRACKSTAT sections
    """
    if not os.path.exists(cchFileName):
      print("couldn't open file %s" % cchFileName)
      sys.exit(1)
    with open(cchFileName, "r") as fh:
      originalText = fh.read()
      cchFile_o = cchFile(originalText, cchFileName)
      _career_blt = cchFile_o.get_career_blt_contribution()
      _errors = cchFile_o.get_errors()
      print(_errors)
      return _career_blt
    return None #?