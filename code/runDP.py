# coding: utf-8

if __name__ == "__main__":
    import dp
    import Stroke
    import cPickle

    dataA = "testLog.pkl"
    dataB = "testLog_3.pkl"

    log1 = cPickle.load(open(dataA, "rb"))
    log2 = cPickle.load(open(dataB, "rb"))

    s1 = Stroke.Stroke(log1)
    s2 = Stroke.Stroke(log2)
    mydp = dp.DP(s1, s2)
    mydp.computeSolution()
    mydp.outputWay()
