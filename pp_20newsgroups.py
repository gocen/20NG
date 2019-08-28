#-*- coding: utf-8 -*-
"""
Preprocess Script for 20Newsgroups Dataset
This script removes headers,footers and quotes
and changes extra points at sentences to commas to split sentences correctly.
Before running this script all files are converted to txt format
"""

import glob
import re

#This 3 function is taken from scikit-learn twenty_newsgroups.py 
def strip_newsgroup_header(text):
    """
    Given text in "news" format, strip the headers, by removing everything
    before the first blank line.
    """
    _before, _blankline, after = text.partition('\n\n')
    return after


_QUOTE_RE = re.compile(r'(writes in|writes:|wrote:|says:|said:'
                       r'|^In article|^Quoted from|^\||^>)')

def strip_newsgroup_quoting(text):
    """
    Given text in "news" format, strip lines beginning with the quote
    characters > or |, plus lines that often introduce a quoted section
    (for example, because they contain the string 'writes:'.)
    """
    good_lines = [line for line in text.split('\n')
                  if not _QUOTE_RE.search(line)]
    return '\n'.join(good_lines)

def strip_newsgroup_footer(text):
    """
    Given text in "news" format, attempt to remove a signature block.

    As a rough heuristic, we assume that signatures are set apart by either
    a blank line or a line made of hyphens, and that it is the last such line
    in the file (disregarding blank lines at the end).
    """
    lines = text.strip().split('\n')
    for line_num in range(len(lines) - 1, -1, -1):
        line = lines[line_num]
        if line.strip().strip('-') == '':
            break

    if line_num > 0:
        return '\n'.join(lines[:line_num])
    else:
        return text


path = '.../20news-bydate/*/*/*.txt'

#list files
files=glob.glob(path)

#open files
for file in files:     
    f=open(file, 'r')  
    text = f.read()
    text = strip_newsgroup_header(text)
    text = strip_newsgroup_quoting(text)
    text = strip_newsgroup_footer(text)

    text = re.sub(r'(\d*)\.(\d+)', r'\1,\2', text) # Change extra points at sentences to commas for split sentences correctly.
    f.close()

    f=open(file, 'w')
    f.write(text)
    f.close()
