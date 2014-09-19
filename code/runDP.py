# coding: utf-8

if __name__ == "__main__":
    import dp
    import Stroke
    import cPickle

    directory = "result/"
    dataA = "ru1"
    dataB = "ru2"

    outputName = directory + dataA + "-" + dataB + ".dat"

    log1 = cPickle.load(open(directory + dataA + ".pkl", "rb"))
    log2 = cPickle.load(open(directory + dataB + ".pkl", "rb"))

    s1 = Stroke.Stroke(log1)
    s2 = Stroke.Stroke(log2)
    mydp = dp.DP(s1, s2)
    mydp.computeSolution()
    mydp.outputWay(outputName)
