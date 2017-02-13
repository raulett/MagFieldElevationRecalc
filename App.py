from Recalc import *



inputFile = open('20160915.csv', 'r')
rec = inputFile.readline()
task = Recalc()

while rec:
    rec = rec.split(',')
    record = Record(float(rec[0]), float(rec[1]), int(rec[2]), int(rec[3]), rec[4], rec[5], rec[6], rec[7],
                    rec[8], float(rec[9]), rec[10], rec[11], 25)

    # record.out()
    task.AddRecord(record)
    # print(rec)
    # print(len(rec))
    rec = inputFile.readline()
inputFile.close()
task.endRecAdding()
# task.out()

field = task.RecalculateField()

# print(str(task.Profiles[0].getField(100, 3)))
# field.out()
outputFile = open('out1.txt', 'w')
for rec in field.out():
    outputFile.write(rec)
outputFile.close()
# for profile in task.Profiles:
#     for rec in profile.profile:
#         field = profile.getField(rec.Distance, 1)
#         print(field)