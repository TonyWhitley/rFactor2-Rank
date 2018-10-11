from collections import OrderedDict
from configparser import RawConfigParser

class MultiOrderedDict(OrderedDict):
    _unique = 0   # class variable
    def __setitem__(self, key, value):
        """  
        # Causes "RuntimeError: OrderedDict mutated during iteration"
        # De-dupe [PLAYERTRACKSTAT] keys in text beforehand instead.
        if key in self:
          self._unique += 1
          key += str(self._unique)
        """
        if isinstance(value, list) and key in self:
            self[key].extend(value)
        else:
            OrderedDict.__setitem__(self, key, value)

class cchFile:
  """ 
  Class that takes the text of a .cch file as a single string,
  splits it at [PLAYERTRACKSTAT] and processes each section separately.
  """
  recordsText = []    # The .cch file split into [PLAYERTRACKSTAT] sections
  recordResults = []  # The parsed result of each [PLAYERTRACKSTAT] section
  _records = []       # Each section as a list of lines (for unit testing)
  _career_blt = []

  def __init__(self, cchFileText, cchFileName):
    # de-dupe the [PLAYERTRACKSTAT] keys by numbering them
    trackstatsCount = cchFileText.count('[PLAYERTRACKSTAT]')
    for i in range(trackstatsCount):
      cchFileText = cchFileText.replace('[PLAYERTRACKSTAT]', '[PLAYERTRACKSTAT_%d]' % i, 1)

    self.config = RawConfigParser(dict_type=MultiOrderedDict, comment_prefixes=('//'), strict=False, empty_lines_in_values=False)
    self.config.read_string(cchFileText, cchFileName)

    for section in self.config.sections():
      if section.startswith('PLAYERTRACKSTAT'):
        _trackstat = ['[PLAYERTRACKSTAT]']

        # sanity check for keywords TrackName, TrackFile and ClassRecord
        try:
          _trackstat.append('TrackName=%s' % self.config[section]['TrackName'])
          _trackstat.append('TrackFile=%s' % self.config[section]['TrackFile'])
          for record in self.config[section]['ClassRecord'].split('\n'):
            _trackstat.append('ClassRecord=%s' % record)
          # parsed OK
          self._career_blt.append('\n'.join(_trackstat)+'\n')


        except:    
          # else return error and self.parsed is None
          pass
          """
          err_line = lineNumberOfThisRecord+1
          self.error = errorText % (cchFileName, err_line)
          # List lines from start of this block up (not including) to start of next
          for line in self.lines:
            if len(line) > maxErrorLineLength:
              # Long entries in the cch file spoil the error message appearance, trim them
              line = line[:maxErrorLineLength] + '...'
            self.error += "%s:%d: %s\n" % (cchFileName, err_line, line)
            err_line += 1
          """

  def get_career_blt_contribution(self):
    """ Return a string with all the trackstat records in the file """
    return ''.join(self._career_blt)

if __name__=="__main__":
  pass
