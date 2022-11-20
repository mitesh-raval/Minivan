#!/usr/bin/env python3

import argparse

'''
    RemoveCommentsAndMisc(inList):
    Removes all lines making up multiline comments and puts extra space 
    before '+' if the line starts with '+'
'''
def RemoveCommentsAndMisc(inList):
    tempList = []
    dropLines = False
    for line in inList:
        if dropLines:
            if not line.endswith('*/'):
                continue
            else:
                dropLines = False
                continue
        if line.startswith('+'):
            line = ''.join([' ', line])
        if line.startswith('/*') and line.endswith('*/') or line.startswith('//'):
            continue
        elif line.startswith('/*') and not line.endswith('*/'):
            dropLines = True
        else:
            tempList.append(line)

    return tempList

'''
    RemoveInlineCommentsAndMisc(inStr) :
    Removes all inline comments and ignores any code lines with a url string in it. 
    Also, fixes one line else statements without curly braces to have an extra space.
    e.g. some code // comment     ==>  some code
         some code /* comment */  ==>  some code
         urlStr = 'http[s]://blah'   // comment ==> unchanged
         urlStr = 'http[s]://blah'   /* comment */ ==> unchanged
         else
            statement;      ==>  else statement;  
'''
def RemoveInlineCommentsAndMisc(inStr):
    if 'http://' in inStr or 'https://' in inStr:
        return inStr
    retStr = inStr
    if '//' in inStr :
        retStr = ''
        strTuples = inStr.partition('/')
        # loop till // is found and not just the first / 
        while not strTuples[2].startswith('/') :
            retStr = ''.join([retStr, strTuples[0], strTuples[1]])
            strTuples = strTuples[2].partition('/')
        retStr = ''.join([retStr, strTuples[0]])
    elif '/*' in inStr:
        retStr = ''
        strTuples = inStr.partition('/')
        # loop till /* is found and not just the first /
        while not strTuples[2].startswith('*') :
            retStr = ''.join([retStr, strTuples[0], strTuples[1]])
            strTuples = strTuples[2].partition('/')
        preCommentStr = ''.join([retStr, strTuples[0]])
        # now partition from right to remove the comment
        postCommentStr = strTuples[2].rpartition('/')[2]
        retStr = ''.join([preCommentStr, postCommentStr])

    ''' Account for one line else statements that do not have curly braces
        by adding an extra space after spaces were stripped in a previous step  
    '''
    if 'else' in retStr and '{' not in retStr:
        retStr = ''.join([retStr, ' '])

    return retStr

def main():
    parser = argparse.ArgumentParser(description='Minify .js or .css file')
    parser.add_argument('source', help='(Relative) Path to source file e.g. script.js')
    parser.add_argument('dest', help='(Relative) new location/file name \
        e.g. script.min.js.')
    args = parser.parse_args()
    src = args.source
    dest = args.dest

    with open(src, 'r') as f:
        content = f.read()

    ''' splitlines to remove all linebreaks before stripping whitespace and tabs ''' 
    linesList = list(map(str.strip,iter(content.splitlines())))
    linesList = RemoveCommentsAndMisc(linesList)
    linesList = list(map(RemoveInlineCommentsAndMisc,iter(linesList)))
    minContent = ''.join(linesList)
    
    with open(dest, 'w') as f:
        f.write(minContent)
        f.flush

main()