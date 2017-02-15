from Recalc import *



inputFile = open('20160915.csv', 'r')
rec = inputFile.readline()
task = Recalc()

while rec:
    rec = rec.split(',')
    record = Record(float(rec[0]), float(rec[1]), int(rec[2])/1000-60747.332, int(rec[3]), rec[4], rec[5], rec[6], rec[7],
                    rec[8], float(rec[9]), rec[10], rec[11], 25)

    # record.out()
    task.AddRecord(record)
    # print(rec)
    # print(len(rec))
    rec = inputFile.readline()
inputFile.close()
task.endRecAdding()


field = task.RecalculateField()


outputFile = open('out1.txt', 'w')
for rec in field.out():
    outputFile.write(rec)
outputFile.close()
