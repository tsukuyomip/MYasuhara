#coding: utf-8

import Stroke
import math

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

        # field[data1][data2] = [[(MOVE_DST, totCost) ...] ...]
        self.field = [[(self.MOVE_UNDEF, -1)]*(data2.totTime + 1)]*(data1.totTime + 1)

        self.makeField(data1, data2)

    def makeField(self, data1, data2):
        # (i, 0)を計算
        for i in range(data1.totTime + 1):
            cost = self.computeDistance(data1.data[i], data2.data[0])
            self.field[i][0] = (self.MOVE_UNDEF, cost)

        # (0, j)を計算
        for j in range(data2.totTime + 1):
            cost = self.computeDistance(data1.data[0], data2.data[j])
            self.field[0][j] = (self.MOVE_UNDEF, cost)

        # (i, j)を計算
        for i in range(1, data1.totTime + 1):
            for j in range(1, data2.totTime + 1):
                cost = self.computeDistance(data1.data[i], data2.data[j])

                # 左を一番小さいとし，順に左下，下を調べる
                min = self.field[i - 1][j][1]
                direction = self.MOVE_R
                if min > self.field[i - 1][j - 1][1]:
                    min = self.field[i - 1][j - 1][1]
                    direction = self.MOVE_UR
                if min > self.field[i][j - 1][1]:
                    min = self.field[i][j - 1][1]
                    direction = self.MOVE_U
                self.field[i][j] = (direction, min + cost)

    def computeDistance(self, elem1, elem2):
        """
        elem1, elem2 は共に Stroke.data
        elem1 と elem2 のユークリッド距離を返す
        """
        distX = elem1[1] - elem2[1]
        distY = elem1[2] - elem2[2]

        return math.sqrt(distX*distX + distY*distY)

    def computeSolution(self):
        way = []
        # 右上からスタート
        pos = [self.data1.totTime, self.data2.totTime]
        way.append((pos[0], pos[1]))

        while(pos[0] > 0 or pos[0] > 0):
            if(pos[0] < 0):
                self.outputError("DP.computeSolution", "pos[0] < 0")
            if(pos[1] < 0):
                self.outputError("DP.computeSolution", "pos[1] < 0")

            dx = 0
            dy = 0
            if   (self.field[pos[0]][pos[1]][0] == self.MOVE_R):
                dx = -1
            elif (self.field[pos[0]][pos[1]][0] == self.MOVE_UR):
                dx = -1
                dy = -1
            elif (self.field[pos[0]][pos[1]][0] == self.MOVE_U):
                dy = -1

            pos[0] += dx
            pos[1] += dy

            way.append((pos[0], pos[1]))

        self.way = way

    def outputError(self, errPoint, mes):
        print >> sys.stderr, "Error(%s): %s" % (str(errPoint), str(mes))
