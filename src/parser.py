#!/usr/bin/python
# -*- coding: UTF-8

import re
from bs4 import BeautifulSoup

class HtmlParser:
  def __init__(self, file):
    self.file = file
    self.document = BeautifulSoup(open(file), 'html.parser')

  def insert(self, classname, format):
    tag = self.document.find(class_ = classname)
    tag.append(format.content())

  def content(self):
    return self.document.contents[0]

  def replace_link(self, placeholder, replacement):
    tag = self.document.find('a')
    if tag:
      tag['href'] = tag['href'].replace(placeholder, replacement)

  def replace_text(self, placeholder, replacement):
    tag = self.document.find(text=re.compile(placeholder))
    if tag:
      tag.replace_with(replacement)

  def text(self):
    return str(self.document)
