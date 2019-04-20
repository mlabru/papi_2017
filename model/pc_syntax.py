#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
pc_syntax

revision 0.1  2017/abr  mlabru
initial release (Linux/Python)
---------------------------------------------------------------------------------------------------
"""
__version__ = "$revision: 0.1$"
__author__ = "Milton Abrunhosa"
__date__ = "2017/04"

# < imports >--------------------------------------------------------------------------------------

# python library
import sys

# PyQt4
from PyQt4 import QtCore
from PyQt4 import QtGui

# -------------------------------------------------------------------------------------------------
def format(color, style=''):
    """
    return a QTextCharFormat with the given attributes
    """
    _color = QtGui.QColor()
    _color.setNamedColor(color)

    _format = QtGui.QTextCharFormat()
    _format.setForeground(_color)

    if "bold" in style:
        _format.setFontWeight(QtGui.QFont.Bold)

    if "italic" in style:
        _format.setFontItalic(True)

    return _format

# -------------------------------------------------------------------------------------------------
# syntax styles that can be shared by all languages
STYLES = {"keyword": format("cyan"),
          "operator": format("red"),
          "brace": format("lightGray"),
          "defclass": format("lightYellow", "bold"),
          "string": format("magenta"),
          "string2": format("lightPink"),
          "comment": format("lightGreen", "italic"),
          "self": format("lightYellow", "italic"),
          "numbers": format("sandyBrown"), }

# < CConfigHighlighter >---------------------------------------------------------------------------

class CConfigHighlighter(QtGui.QSyntaxHighlighter):
    """
    syntax highlighter for the config parameters
    """
    # python keywords
    keywords = ["and", "ser", "break", "class", "tim", "net",
                "dir", "elif", "else", "except", "exec", "finally",
                "for", "from", "glb", "if", "import", "in",
                "is", "lambda", "not", "or", "pass", "print",
                "raise", "return", "try", "while", "yield",
                "None", "True", "False", ]

    # python operators
    operators = ["=",
                 # comparison
                 "==", "!=", "<", "<=", ">", ">=",
                 # arithmetic
                 "\+", "-", "\*", "/", "//", "\%", "\*\*",
                 # in-place
                 "\+=", "-=", "\*=", "/=", "\%=",
                 # bitwise
                 "\^", "\|", "\&", "\~", ">>", "<<",]

    # python braces
    braces = ["\{", "\}", "\(", "\)", "\[", "\]", ]

    # ---------------------------------------------------------------------------------------------
    def __init__(self, document):
        """
        constructor
        """
        # init super class
        # QtGui.QSyntaxHighlighter.__init__(self, document)
        super(CConfigHighlighter, self).__init__(document)

        # multi-line strings (expression, flag, style)
        # FIXME: The triple-quotes in these two lines will mess up the
        # syntax highlighting from this point onward
        self.tri_single = (QtCore.QRegExp("'''"), 1, STYLES['string2'])
        self.tri_double = (QtCore.QRegExp('"""'), 2, STYLES['string2'])

        rules = []

        # keyword, operator, and brace rules
        rules += [(r'\b%s\b' % w, 0, STYLES['keyword']) for w in CConfigHighlighter.keywords]
        rules += [(r'%s' % o, 0, STYLES['operator']) for o in CConfigHighlighter.operators]
        rules += [(r'%s' % b, 0, STYLES['brace']) for b in CConfigHighlighter.braces]

        # all other rules
        rules += [
            # 'self'
            (r'\bself\b', 0, STYLES['self']),

            # double-quoted string, possibly containing escape sequences
            (r'"[^"\\]*(\\.[^"\\]*)*"', 0, STYLES['string']),
            # single-quoted string, possibly containing escape sequences
            (r"'[^'\\]*(\\.[^'\\]*)*'", 0, STYLES['string']),

            # 'def' followed by an identifier
            (r'\bdef\b\s*(\w+)', 1, STYLES['defclass']),
            # 'class' followed by an identifier
            (r'\bclass\b\s*(\w+)', 1, STYLES['defclass']),

            # from '#' until a newline
            (r'#[^\n]*', 0, STYLES['comment']),

            # numeric literals
            (r'\b[+-]?[0-9]+[lL]?\b', 0, STYLES['numbers']),
            (r'\b[+-]?0[xX][0-9A-Fa-f]+[lL]?\b', 0, STYLES['numbers']),
            (r'\b[+-]?[0-9]+(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?\b', 0, STYLES['numbers']),
        ]

        # build a QRegExp for each pattern
        self.rules = [(QtCore.QRegExp(pat), index, fmt) for (pat, index, fmt) in rules]

    # ---------------------------------------------------------------------------------------------
    def highlightBlock(self, text):
        """
        apply syntax highlighting to the given block of text
        """
        # do other syntax formatting
        for expression, nth, format in self.rules:
            index = expression.indexIn(text, 0)

            while index >= 0:
                # we actually want the index of the nth match
                index = expression.pos(nth)
                length = expression.cap(nth).length()
                self.setFormat(index, length, format)
                index = expression.indexIn(text, index + length)

        self.setCurrentBlockState(0)

        # do multi-line strings
        in_multiline = self.match_multiline(text, *self.tri_single)
        if not in_multiline:
            in_multiline = self.match_multiline(text, *self.tri_double)

    # ---------------------------------------------------------------------------------------------
    def match_multiline(self, text, delimiter, in_state, style):
        """
        do highlighting of multi-line strings. ``delimiter`` should be a
        ``QRegExp`` for triple-single-quotes or triple-double-quotes, and
        ``in_state`` should be a unique integer to represent the corresponding
        state changes when inside those strings. Returns True if we're still
        inside a multi-line string when this function is finished
        """
        # If inside triple-single quotes, start at 0
        if self.previousBlockState() == in_state:
            start = 0
            add = 0
        # otherwise, look for the delimiter on this line
        else:
            start = delimiter.indexIn(text)
            # Move past this match
            add = delimiter.matchedLength()

        # as long as there's a delimiter match on this line...
        while start >= 0:
            # look for the ending delimiter
            end = delimiter.indexIn(text, start + add)
            # ending delimiter on this line?
            if end >= add:
                length = end - start + add + delimiter.matchedLength()
                self.setCurrentBlockState(0)
            # no; multi-line string
            else:
                self.setCurrentBlockState(in_state)
                length = text.length() - start + add
            # apply formatting
            self.setFormat(start, length, style)
            # look for the next match
            start = delimiter.indexIn(text, start + length)

        # return True if still inside a multi-line string, False otherwise
        return self.currentBlockState() == in_state

# < the end >--------------------------------------------------------------------------------------
