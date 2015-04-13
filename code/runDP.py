# coding: utf-8
import sys
from subprocess import PIPE, Popen

if __name__ == "__main__":
    import dp
    import Stroke
    import cPickle

    argvs = sys.argv
    if(len(argvs) == 1):
        # 読み込み・保存ファイル名に関する定義
        directory = "result/"
        dataA = "ru1"
        dataB = "ru1"
    elif(len(argvs) == 4):
        directory = argvs[1]
        if directory[-1] != "/":
            directory += "/"
        dataA = argvs[2]
        dataB = argvs[3]
    else:
        print >> sys.stderr, \
            "usage:\n"+\
            "\tpython %s [<DIR_NAME> <FILE1> <FILE2>]\n" % (argvs[0])
        quit()

    # 時間＋座標データ読み込み
    log1 = cPickle.load(open(directory + dataA + ".pkl", "rb"))
    log2 = cPickle.load(open(directory + dataB + ".pkl", "rb"))

    # (10msごとの)ストロークに変換
    s1 = Stroke.Stroke(log1)
    s2 = Stroke.Stroke(log2)

    # 動的計画法でTimeWarpingFunctionを求める
    mydp = dp.DP(s1, s2)
    mydp.computeSolution()
    outputName = directory + \
                 dataA + "-" + dataB + \
                 "-dist" + str(mydp.wayDist) + ".dat"
    mydp.outputWay(outputName)
    print>>sys.stderr, "wayDist:" + str(mydp.wayDist)
    print>>sys.stderr, "output:", outputName

    plotquery = 'plot "%s" w l' % outputName
    print>>sys.stderr, plotquery

    plot = Popen(['gnuplot'], stdin=PIPE)
    plot.communicate(plotquery)
