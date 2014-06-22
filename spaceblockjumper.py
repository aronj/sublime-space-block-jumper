# -*- coding: utf-8 -*-

from sublime import *
from sublime_plugin import *
import re

SETTINGS = "Base File.sublime-settings"

class SpaceBlockJumper(TextCommand):

    def __init__(self, view):

        super(View).__init__()
        self.view = view
        self.skipClosestEdge = load_settings(SETTINGS).get("Skip Closest Edge", True)
        self.jumpToBlockSeparator = load_settings(SETTINGS).get("Jump To Block Separator", False)
        self.ShowCursorAtCenter = load_settings(SETTINGS).get("Show Cursor At Center", True)

        self.mode = 0

    @classmethod
    def updateContext(self, fun):
        def wrapper(self, *args, **kwargs):
            self.selection = self.view.sel()[0]
            self.startCursorPoint = self.selection.b
            self.startCursorRow, self.startCursorCol = self.rowcol(self.startCursorPoint)
            return fun(self, *args, **kwargs)
        return wrapper

    def jump(self, direction, select):

        newLine = self.getNewLine(self.startCursorRow, direction)
        if select:
            newRegion = self.getLineRegion(newLine)
            if direction -1:
                self.view.sel().add(self.selection.cover(newRegion))
            else:
                self.view.sel().add(newRegion.cover(self.selection))

        else:
            self.view.sel().clear()
            rightCheck = min(self.getLineRegion(newLine, full=True).size(), self.startCursorCol)
            leftCheck = max(self.getLineStart(newLine), rightCheck)
            newRegion = Region(self.point(newLine, leftCheck ))
            self.view.sel().add(newRegion)

        if self.ShowCursorAtCenter:
            self.view.show_at_center(newRegion)
        else:
            self.view.show(newRegion)

    def selectBlock(self):

        topLine = self.getNewLine(self.startCursorRow, -1, stayInBlock=True)
        bottomLine = self.getNewLine(self.startCursorRow, 1, stayInBlock=True)

        newRegionList = []

        # modes: "minimum", "expanded", "multiline-minimum", "multiline-expanded"
        if self.mode in [0, 2]:
            r1 = self.getLineRegion(topLine)
            r2 = self.getLineRegion(bottomLine)
        elif self.mode in [1, 3]:
            r1 = self.getLineRegion(topLine, full=True)
            r2 = self.getLineRegion(bottomLine, full=True)
        newRegion = r1.cover(r2)
        if self.mode in [2, 3]:
            newRegionList = self.view.split_by_newlines(newRegion)
            if self.mode == 2:
                tmpList = []
                for lineRegion in list(newRegionList):
                    tmpList.append(self.getLineRegion(self.rowcol(lineRegion.a)[0]))
                newRegionList = tmpList

        if re.sub('[\t\s\n]', '', self.view.substr(newRegion)) == "":
            self.view.sel().add(newRegion)
        elif (newRegion == self.view.sel()[0] or newRegionList == self.view.sel()):
            self.mode =  (self.mode+1)%4
            self.selectBlock()
        else:
            self.view.sel().clear()
            if len(newRegionList) > 0:
                self.view.sel().add_all(newRegionList)
                self.view.show(newRegionList[0].cover(newRegionList[-1]))
            else:
                self.view.sel().add(newRegion)
                self.view.show(newRegion)


    def getNewLine(self, currLine, direction, stayInBlock=False):
        nextLine = currLine + direction

        if not self.isInBounds(nextLine):
            return currLine

        if self.jumpToBlockSeparator:
            currLine += direction
            while self.isInBounds(currLine+direction) and self.isEmptyLine(currLine) == self.isEmptyLine(currLine+direction):
                currLine += direction
            return currLine+(direction if not self.isEmptyLine(currLine) else 0)

        # moving in emptiness
        if (self.isEmptyLine(currLine) and self.isEmptyLine(nextLine)):
            currLine += direction
            while self.isInBounds(currLine+direction) and self.isEmptyLine(currLine+direction):
                currLine += direction
            if not stayInBlock:
                currLine += direction

        # moving inside a block
        elif not self.isEmptyLine(currLine) and not self.isEmptyLine(nextLine):
            currLine += direction
            while self.isInBounds(currLine+direction) and not self.isEmptyLine(currLine+direction):
                currLine += direction

        # moving from an edge of a block
        elif not self.isEmptyLine(currLine) and self.isEmptyLine(nextLine) and not stayInBlock:
            currLine += direction
            if self.skipClosestEdge:
                while self.isInBounds(currLine+direction) and not (not self.isEmptyLine(currLine) and self.isEmptyLine(currLine+direction)):
                    currLine += direction
            else:
                while self.isInBounds(currLine+direction) and self.isEmptyLine(currLine):
                    currLine += direction

        # moving to an edge of a block
        elif self.isEmptyLine(currLine) and not self.isEmptyLine(nextLine) and not stayInBlock:
            currLine += direction
        return currLine

    def isInBounds(self, line):
        bufferRegion = Region(0,self.view.size())
        return True if line >= 0 and line < len(self.view.lines(bufferRegion)) else False

    def isEmptyLine(self, line):
        linestr = self.view.substr(self.getLineRegion(line))
        return True if linestr == "" else False

    def getLineRegion(self, line, full=False):
        if full:
            lineRegion = self.view.line(self.point(line, 0))
        else:
            wordStartCol = self.getLineStart(line)
            wordStartPoint = self.point(line, wordStartCol)
            lineRegion = Region(wordStartPoint, self.view.line(wordStartPoint).end())
        return lineRegion

    def getLineStart(self, line):
        n = 0
        p = self.point(line, n)
        while(self.view.substr(p) == " " or self.view.substr(p) == "\t"):
            n += 1
            p = self.point(line, n)
        return n

    def getCurrentRowCol(self, whichEnd):
        if whichEnd == "begin":
            return self.view.rowcol(self.view.sel()[0].begin())
        elif whichEnd == "end":
            return self.view.rowcol(self.view.sel()[0].end())

    def rowcol(self, point):
        return self.view.rowcol(point)
    def point(self, row, col):
        return self.view.text_point(row, col)

class SpaceBlockJumpCommand(SpaceBlockJumper):
    @SpaceBlockJumper.updateContext
    def run(self, edit, direction, select=False):
        self.jump(direction, select)

class SpaceBlockSelectBlockCommand(SpaceBlockJumper):
    @SpaceBlockJumper.updateContext
    def run(self, edit):
        self.selectBlock()
