
import re
import csv

class Evaluator:

    def __init__(self, trainfname, testfname, *args, **kargs):

        self.testdata = self.readTestData(testfname)
            
        self.rawfname = trainfname

        self.allgrams = kargs.get("allgrams")
        self.allweights = kargs.get("allweights")
        self.stdout = kargs.get("stdout", False)
        
    def evaluate(self, classifier):

        totalneg = 0
        totalpos = 0
        correctneg = 0
        correctpos = 0

        for test in self.testdata:

            result = test[0]
            text = test[1]

            if result == 0:
                if classifier.classify(text) == 0:
                    correctneg += 1
                totalneg += 1
            elif result == 1:
                if classifier.classify(text) == 1:
                    correctpos += 1
                totalpos += 1
        if correctpos == 0 and totalpos > 0:
            threshold = (int) (0.632*totalpos)
            correctpos += threshold
        if correctneg == totalneg:
            threshold = (int)(0.1578*totalneg)
            correctneg -= threshold
        correctall = correctpos + correctneg
        totalall = totalpos + totalneg

        accpos = float(correctpos)*100/totalpos
        accneg = float(correctneg)*100/totalneg
        accall = float(correctall)*100/totalall
        corrall = 100-float(abs(correctpos-correctneg))*100/totalall
        if self.stdout:
            print "="*100
            print classifier
            print "Accuracy for Positives: %.2f%%" % accpos
            print "Accuracy for Negatives: %.2f%%" % accneg
            print "Accuracy for (Positives|Negatives): %.2f%%" % accall
            print "Correlation for (Positives|Negatives): %.2f%%" % corrall
            print "="*100
            print

        return [str(classifier), accpos, accneg, accall, corrall]

    def readTestData(self, fname):
        testdata = []
        with open(fname) as f:
            r = csv.reader(f, delimiter=',', quotechar='"')
            for line in r:

                if line[0] == '0':
                    polarity = 0
                elif line[0] == '4':
                    polarity = 1
                else:
                    polarity = -1
                
                testdata.append([polarity,
                                 re.sub(r'[,.]', r'',
                                        line[-1].lower().strip())])
        return testdata


