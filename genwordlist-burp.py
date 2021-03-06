#!/usr/bin/python
#
# Simple script to generate a sorted unique wordlist from a burp sitemap
# Input file can be b64 encoded or plain
# Usage: $ ./genwordlist.py <inputfile> [outfile]
# Saves output to wordlist.txt
#
import base64
import re
import sys
try:    # Use faster C implementation if we can
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

wordlist = set()

for event, elem in ET.iterparse(sys.argv[1]):
    if event == 'end':
        if elem.tag == 'response':
            if elem.attrib["base64"] == "true":
                response = str(base64.b64decode(elem.text))
            else:
                response = str(elem.text)
            words = re.findall("[a-zA-Z0-9\-]+", response)
            for word in words:
                wordlist.add(word)
    elem.clear() # Discard the element to free memory


wordlist = sorted(wordlist, key=lambda s: s.lower())    # Case insensitive sort

try:
    outfile = sys.argv[2]
except IndexError:
    outfile = "wordlist.txt"
f = open(outfile, "w")
for word in wordlist:
    f.write(word + "\n")
print("Wrote " + str(len(wordlist)) + " words to " + outfile)
