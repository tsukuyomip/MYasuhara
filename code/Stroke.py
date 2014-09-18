# coding: utf-8
import sys

class Stroke(object):
    def __init__(self, rawData = None):
        """
        rawData = [(time, x, y)...]
        data = [(time, x, y)...]
        rawDataのキャプチャ点で省かれた部分を補完．（data要素数 = totTime になる）
        data内要素のx, yは [0.0 : 1.0] で正規化される．
        """

        if (rawData is None):
            rawData = [(0, 0, 0)]
        self.rawData = rawData
        self.nRawData = len(rawData)
        if(self.nRawData == 0):
            self.outputError("class Stroke.__init__", 
                             "nRawData is 0")

        if(len(rawData[0]) != 3):
            self.outputError("class Stroke.__init__", 
                             "elem of data len isn't 3 (t, x, y)")

        self.totTime = rawData[-1][0]

        (minX, maxX, minY, maxY) = self.getMinMax(rawData)
        self.minX = minX
        self.maxX = maxX
        self.minY = minY
        self.maxY = maxY

        data = self.normalizeRawData(rawData)

    def getMinMax(self, rawData):
        minX = rawData[0][1]
        maxX = rawData[0][1]
        minY = rawData[0][2]
        maxY = rawData[0][2]
        for i in range(1, self.nRawData):
            if(minX > rawData[i][1]):
                minX = rawData[i][1]
            if(maxX < rawData[i][1]):
                maxX = rawData[i][1]
            if(minY > rawData[i][2]):
                minY = rawData[i][2]
            if(maxY < rawData[i][2]):
                maxY = rawData[i][2]

        return (minX, maxX, minY, maxY)


    def normalizeRawData(self, rawData):
        """
        与えられたrawDataのX, Yを[0.0 : 1.0]に正規化．
        各t間を補完し，dataとして補完結果を格納
        """
        xSize = self.maxX - self.minX
        if(xSize <= 0):
            self.outputError("class Stroke.normalizeRawData", 
                             "xSize(%d) <= 0" % (xSize))

        ySize = self.maxY - self.minY
        if(ySize <= 0):
            self.outputError("class Stroke.normalizeRawData", 
                             "ySize(%d) <= 0" % (ySize))

        data = []
        t = 0
        nextIndex = 0

        while(nextIndex < self.nRawData):
            if(rawData[nextIndex][0] > t):
                nmlX = data[-1][1]
                nmlY = data[-1][2]
            else:
                nmlX = float(rawData[nextIndex][1] - self.minX)/float(xSize)
                nmlY = float(rawData[nextIndex][2] - self.minY)/float(ySize)
                nextIndex += 1

            data.append((t, nmlX, nmlY))
            t += 1

        self.data = data

    def outputError(self, errPoint, mes):
        print >> sys.stderr, "Error(%s): %s" % (str(errPoint), str(mes))

if __name__ == "__main__":
    import cPickle
    inputFilename = "testLog.pkl"
    outputFilename = "testStroke.pkl"
    log = cPickle.load(open(inputFilename, "rb"))
    s = Stroke(log)
    cPickle.dump(s, open(outputFilename, "wb"))
