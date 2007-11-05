"""ReadifyXML.py: Reformat XML, breaking up long tags to
make it more human-readable"""
from xml.dom.minidom import parseString
import re

triggerLineLength = 60 # Try to reformat lines longer than this

# Amount of indentation to use when reformatting:
indentStep = "  "

def makeXMLReadable(xml):
    xml = xml.toprettyxml("", "\n")
    # Remove trailing whitespace from each line:
    xml = "\n".join(
        [line.rstrip() for line in xml.split("\n")])
    # Remove all empty lines before opening '<':
    while xml.find("\n\n<") != -1:
        xml = xml.replace("\n\n<", "\n<")
    xml = parseString(xml).toprettyxml(indentStep, "")
    # Now all the xml lines are tight,
    # and we can insert spaces and line breaks:
    xml = addBreaks(xml)
    xml = reformatTooLongLines(xml)
    return xml

############# Support functions #############

addBreak = re.compile("\s{0,%d}<[a-zA-Z]" % len(indentStep))
def addBreaks(xml):
    '''Add line breaks to elements with
    zero or one indent level'''
    result = ""
    for line in xml.split("\n"):
        if addBreak.match(line):
            result += "\n"
        result += line + "\n"
    return result

def reformatTooLongLines(xml):
    result = ""
    for line in [line.rstrip() for line in xml.split("\n")]:
        if len(line) < triggerLineLength or not line.lstrip().startswith("<"):
            result += line + "\n"
        else:
            result += reformatLongLine(line) + "\n"
    return result

oneLiner = re.compile("([ ]*)(<\w+)(.*)>")
keyValuePair = re.compile('\w+="[^"]*?"')
def reformatLongLine(line):
    '''Reformat an xml tag to put each key-value
    element on a single indented line, for readability'''
    matchobj = oneLiner.match(line.rstrip())
    baseIndent = matchobj.group(1)
    result = baseIndent + matchobj.group(2) + "\n"
    indent = baseIndent + " " # Match indent level of tag
    for pair in keyValuePair.findall(matchobj.group(3)):
        result += indent + pair + "\n"
    result = result.rstrip() + " />"
    return result
