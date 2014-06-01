import copy
import sublime_plugin
import urllib2
import sublime

import re

import Tools#for remove_trailing_spaces() and form_indent()

class Code:
  "Manipulations with the C/C++ code."

  def __init__(self, v, e):#v for self.view
    self.view_setting = v#=self.view in FormatCode.py
    self.edit_setting = e#=edit in FormatCode.py
    self.margins = []
    self.broken_line_number = -1
    self.regions = []
    self.strings = []
    self.update_data()
    self.region_warning = []#list of warning areas in Region format
    self.string_warning = []#list of warnign areas in string format
    self.warning_description = []#list of descriptions for each warning

  def align(self):#v <=> self.view, e <=> edit
    s = sublime.load_settings("Convention.sublime-settings")

    margin = 0
    page = ""
    self.broken = False
    number = 1

    for line_str in self.strings:

      if re.match(r'.*{.*', line_str) and not self.broken:
        line_str = Tools.remove_trailing_spaces(line_str)
        for n in range(0, margin):
          page += Tools.form_indent(s.get("indent_size"))
        self.margins.append(margin)
        margin += 1
      elif re.match(r'.*}.*', line_str) and not self.broken:
        if margin > 0:
          margin -= 1
        else:
          self.broken = True
          self.broken_line_number = number
        line_str = Tools.remove_trailing_spaces(line_str)
        for n in range(0, margin):
          page += Tools.form_indent(s.get("indent_size"))
        self.margins.append(margin)
      elif not self.broken:
        line_str = Tools.remove_trailing_spaces(line_str)
        for n in range(0, margin):
          page += Tools.form_indent(s.get("indent_size"))
        self.margins.append(margin)

      page += line_str
      page += "\n"
      number += 1

    self.view_setting.replace(self.edit_setting, sublime.Region(0, self.view_setting.size()), page)

    #clear the strings and put the updated data
    self.update_data()

  def highlight_break(self):#highlight a broken line
    if self.broken and self.broken_line_number != -1:
      f = self.view_setting.find("\}", int(self.regions[self.broken_line_number - 1].a))
      self.view_setting.add_regions("break", [f], "keyword")

  def update_data(self):#extract the current sets of string-regions and strings and put it to the storage
    if self.regions:
      del self.regions[0:len(self.regions)]
    if self.strings:
      del self.strings[0:len(self.strings)]
    for line_region in self.view_setting.lines(sublime.Region(0, self.view_setting.size())):
      self.regions.append(line_region)
      line_str = self.view_setting.substr(line_region)
      self.strings.append(line_str)

  def find_warnings(self):
    s = sublime.load_settings("Convention.sublime-settings")

    #argument definition: no space vs. one space
    if s.get("space_in_arguments_definition") == "one":
      arguments_definition = r'\([^ \n][^\n]+[^ \n]\)'
    elif s.get("space_in_arguments_definition") == "no":
      arguments_definition = r'\( [^\n]+ \)'

    #line length
    if s.get("line_length"):
      long_line = '\n[^\n]{' + str(s.get("line_length")) + ',}\n'

    #condition: no space vs. one space
    if s.get("space_in_condition") == "one":
      condition = r'(if\(|while\(|switch\()'
    elif s.get("space_in_condition") == "no":
      condition = r'(if \(|while \(|switch \()'

    #block statement: one space vs. no space vs. new line
    if s.get("block_statement") == "one":
      block = r'(\)\{|\n[^\n^(else)^(else if)]*\{)'
    elif s.get("block_statement") == "no":
      block = r'(\) \{|\n[^\n^(else)^(else if)]*\{)'
    elif s.get("block_statement") == "newline":
      block = r'(\)\{|\)\ {)'

    combined_regexp = '(' + arguments_definition + '|' + long_line + '|' + condition + '|' + block + ')'
    warnings = self.view_setting.find_all(combined_regexp)
    counter = 0
    warning_strings = []
    
    if self.region_warning:
      del self.region_warning[0:len(self.region_warning)]
    if self.string_warning:
      del self.string_warning[0:len(self.string_warning)]
    
    for el in warnings:
      counter += 1
      warning_strings.append(self.view_setting.substr(el))
      self.region_warning.append(el)
      self.string_warning.append(self.view_setting.substr(el))
      
      if re.match(arguments_definition, self.view_setting.substr(el)):
        if s.get("space_in_arguments_definition") == "one":
          self.warning_description.append("ARGUMENTS: One space before and one space after the arguments definition: ")
        else:
          self.warning_description.append("ARGUMENTS: No space before or after the arguments definition: ")
      
      elif re.match(long_line, self.view_setting.substr(el)):
        self.warning_description.append("LENGTH: Line no longer than " + str(s.get("line_length")) + " characters: ")
      
      elif re.match(condition, self.view_setting.substr(el)):
        if s.get("space_in_condition") == "no":
          self.warning_description.append("CONDITION: No space before semicolon in the condition statement: ")
        else:
          self.warning_description.append("CONDITION: One space before semicolon in the condition statement: ")

      elif re.match(block, self.view_setting.substr(el)):
        if s.get("block_statement") == "no":
          self.warning_description.append("BLOCK: No space between closed and opened brackets: ")
        elif s.get("block_statement") == "one":
          self.warning_description.append("BLOCK: One space between closed and opened brackets: ")
        else:
          self.warning_description.append("BLOCK: Opened bracket on the next line: ")

      listing = [x + y for x, y in zip(self.warning_description, self.string_warning)]
    
      listing = ["CLEAR"] + ["ALIGN"] + listing

    self.view_setting.window().show_quick_panel(listing, self.beautify, sublime.MONOSPACE_FONT)

  def beautify(self, picked):#picked:0,1,2,...
    if picked == 0:
      self.view_setting.add_regions("warn", [sublime.Region(0, 0)], "bookmark", sublime.HIDDEN)
      self.view_setting.add_regions("break", [sublime.Region(0, 0)], "keyword", sublime.HIDDEN)
    elif picked == 1:
      self.align()
      self.highlight_break()
    else:
      self.view_setting.show(self.region_warning[picked - 2].a)
      self.view_setting.add_regions("warn", [self.region_warning[picked - 2]], "bookmark", sublime.DRAW_OUTLINED)