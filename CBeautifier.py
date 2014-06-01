import sublime_plugin
import urllib2
import sublime
import re

from Code import Code

import Tools

class CBeautifierCommand(sublime_plugin.TextCommand):

  def has_bracket(self, line):
    result = False
    for c in line:
      if c == '{' or c == '}':
        result =  True
        break
    return result

  def run(self, edit):
    c = Code(self.view, edit)
    c.find_warnings()
