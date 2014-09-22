#coding: utf-8

import Stroke
import math
import sys

class DP(object):
    MOVE_UNDEF = -1
    MOVE_R = 0
    MOVE_U = 1
    MOVE_RU = 2
    MOVE_UR = 2

    def __init__(self, data1 = None, data2 = None):
        """
        data1, data2 共にStrokeのインスタンス
        class Stroke
          rawData: [(t, x, y) ...]
          nRawData: ( = len(rawData) )
          totTime: int
          minX(Y): int
          maxX(Y): int
          data: [(t, x, y) ...] completemented and normalized
        """
        if(data1 is None):
            self.outputError("DP.__init__", "data1 is None")
        if(data2 is None):
            self.outputError("DP.__init__", "data2 is None")

        self.data1 = data1
        self.data2 = data2

        self.makeField(data1, data2)

    def makeField(self, data1, data2):
        # field[data1][data2] = [[(MOVE_DST, totCost) ...] ...]
        self.field = []
        for i in range(data1.totTime + 1):
            self.field.append([(self.MOVE_UNDEF, 0)]*(data2.totTime + 1))

        # (0, 0)を計算
        cost = self.computeDistance(data1.data[0], data2.data[0])
        self.field[0][0] = (self.MOVE_UNDEF, cost)

        # (i, 0)を計算
        for i in range(1, data1.totTime + 1):
            cost = self.computeDistance(data1.data[i], data2.data[0])
            prevCost = self.field[i-1][0][1]
            self.field[i][0] = (self.MOVE_R, prevCost + cost)

        # (0, j)を計算
        for j in range(1, data2.totTime + 1):
            cost = self.computeDistance(data1.data[0], data2.data[j])
            prevCost = self.field[0][j-1][1]
            self.field[0][j] = (self.MOVE_U, prevCost + cost)

        # (i, j)を計算
        for i in range(1, data1.totTime + 1):
            for j in range(1, data2.totTime + 1):
                # 左下を一番小さいとし，順に左，下を調べる
                min = self.field[i - 1][j - 1][1]
                direction = self.MOVE_UR

                tmp = self.field[i - 1][j][1]
                if tmp < min:
                    min = tmp
                    direction = self.MOVE_UR

                tmp = self.field[i][j - 1][1]
                if tmp < min:
                    min = tmp
                    direction = self.MOVE_U

                cost = self.computeDistance(data1.data[i], data2.data[j])

                self.field[i][j] = (direction, min + cost)
                if(i == 0):
                    print "warning!!!!"

    def computeDistance(self, elem1, elem2):
        """
        elem1, elem2 は共に Stroke.data
        elem1 と elem2 のユークリッド距離を返す
        """
        distX = float(elem1[1]) - float(elem2[1])
        distY = float(elem1[2]) - float(elem2[2])

        return math.sqrt(distX*distX + distY*distY)

    def computeSolution(self):
        self.way = []
        # 右上からスタート
        xPos = self.data1.totTime
        yPos = self.data2.totTime
        self.way.append((xPos, yPos))

        while(xPos >= 0 and yPos >= 0):
            if (xPos == 0 and yPos == 0):
                break
            if(xPos < 0):
                self.outputError("DP.computeSolution", "xPos(%d) < 0" % xPos)
            if(yPos < 0):
                self.outputError("DP.computeSolution", "yPos(%d) < 0" % yPos)

            dx = 0
            dy = 0
            if   (self.field[xPos][yPos][0] == self.MOVE_R):
                dx = -1
            elif (self.field[xPos][yPos][0] == self.MOVE_U):
                dy = -1
            elif (self.field[xPos][yPos][0] == self.MOVE_UR):
                dx = -1
                dy = -1
            else:
                self.outputError("DP.computeSolution", "(%d, %d) MOVE_UNDEF?" % (xPos, yPos))

            xPos += dx
            yPos += dy

            self.way.append((xPos, yPos))

        #self.way = way

        # DP結果と距離の計算・出力
        self.computeWayDistance()
        #print self.wayDist


    def outputWay(self, filename = "result.dat"):
        fp = open(filename, "w")

        for i in range(len(self.way)):
            print "%d\t%d" % (self.way[i][0], self.way[i][1])
            fp.write("%d\t%d" % (self.way[i][0], self.way[i][1]))
            fp.write("\n")

        print ""
        fp.write("\n")

        # 完全マッチ時の直線の描画

        print "0\t0"
        fp.write("0\t0")
        fp.write("\n")

        print "%d\t%d" % (self.data1.totTime, self.data2.totTime)
        fp.write("%d\t%d" % (self.data1.totTime, self.data2.totTime))
        fp.write("\n")

        fp.close()


    def computeWayDistance(self):
        dist = 0.0
        a = float(self.data2.totTime)/float(self.data1.totTime)
        for p in self.way:
            dist += math.sqrt((p[1] - a*p[0])*(p[1] - a*p[0]))
        self.wayDist = dist / float(len(self.way))


    def outputError(self, errPoint, mes):
        print >> sys.stderr, "Error(%s): %s" % (str(errPoint), str(mes))
