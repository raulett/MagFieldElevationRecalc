# -*- coding: utf-8 -*-
import copy


class Record:
    def __init__(self, X, Y, TField, qmc, st, date, time, lat, lon, elev, date_1, t, RecalcH):
        self.X = X
        self.Y = Y
        self.TField = TField
        self.RecalcH = RecalcH
        self.Distance = 0
        self.Date = date
        self.Time = time
        self.lat = lat
        self.lon = lon
        self.elev = elev

    def out(self):
        return str(self.X) + ' ' + str(self.Y) + ' ' + str(self.TField) + ' ' + str(self.Distance)


class Profile:
    def __init__(self):
        self.functions = []
        self.profile = []
        self.defaultField = 0

    def createFunc(self):
        for recNum in range(1, len(self.profile)):
            start = self.profile[recNum - 1].Distance
            end = self.profile[recNum].Distance
            k = (self.profile[recNum].TField - self.profile[recNum - 1].TField) \
                / (self.profile[recNum].Distance - self.profile[recNum - 1].Distance)
            b = self.profile[recNum].TField - k * self.profile[recNum].Distance
            # (self.profile[recNum].TField*self.profile[recNum-1].Distance)-\
            # (self.profile[recNum-1].TField*self.profile[recNum].Distance)/\
            # (self.profile[recNum-1].Distance-self.profile[recNum].Distance)
            self.functions.append((start, end, k, b))

    # Функция возвращает значение поле в конкретной точке
    def getField(self, distance, index):
        maxIndex = len(self.functions)

        while ((index > 0) and (index < maxIndex)):
            if (distance < self.functions[index][0]):
                index = index - 1
            elif (distance > self.functions[index][1]):
                index = index + 1
            else:
                return self.functions[index][2] * distance + self.functions[index][3]

        return self.defaultField


class Recalc:
    def __init__(self):
        self.A = [7.303, -2.326, -0.568, -0.193, -0.018, -0.041, -0.003]
        self.Profile = Profile()
        self.Profiles = []
        self.firstRec = 1
        self.prevX = 0
        self.prevY = 0
        self.prevDistance = 0
        self.prevRec = 0
        self.profileDistance = 40

    def RecalculateField(self):
        field = Recalc()
        for profile in self.Profiles:
            for i in range(len(profile.profile)):
                dist = profile.profile[i].Distance
                recalcH = profile.profile[i].RecalcH
                fieldT = self.A[0] * profile.profile[i].TField + \
                         self.A[1] * ((profile.profile[i].TField +
                                       profile.getField(dist - recalcH, i)) / 2 +
                                      (profile.profile[i].TField +
                                       profile.getField(dist + recalcH, i)) / 2) + \
                         self.A[2] * (profile.getField(dist - recalcH, i) +
                                      profile.getField(dist + recalcH, i)) + \
                         self.A[3] * (profile.getField(dist - 2 * recalcH, i) +
                                      profile.getField(dist + 2 * recalcH, i)) + \
                         self.A[4] * (profile.getField(dist - 3 * recalcH, i) +
                                      profile.getField(dist + 3 * recalcH, i)) + \
                         self.A[5] * (profile.getField(dist - 6 * recalcH, i) +
                                      profile.getField(dist + 6 * recalcH, i)) + \
                         self.A[6] * (profile.getField(dist - 8 * recalcH, i) +
                                      profile.getField(dist + 8 * recalcH, i))
                # print(str(self.A[0]*profile.profile[i].TField) + str(' ') +
                #       str(self.A[1]*((profile.profile[i].TField + profile.getField(dist - recalcH, i))/2 +
                #                      (profile.profile[i].TField + profile.getField(dist + recalcH, i))/2)) + str(' ') +
                #       str(self.A[2]*(profile.getField(dist - recalcH, i) +
                #                      profile.getField(dist + recalcH, i))) + str(' ') +
                #       str(self.A[3]*(profile.getField(dist - 2*recalcH, i) +
                #                     profile.getField(dist + 2*recalcH, i))) + str(' ') +
                #       str(self.A[4]*(profile.getField(dist - 3*recalcH, i) +
                #                     profile.getField(dist + 3*recalcH, i))) + str(' ') +
                #       str(self.A[5]*(profile.getField(dist - 6*recalcH, i) +
                #                     profile.getField(dist + 6*recalcH, i))) + str(' ') +
                #       str(self.A[6]*(profile.getField(dist - 8*recalcH, i) +
                #                     profile.getField(dist + 8*recalcH, i)))+ '\n')
                # print(str(profile.profile[i].TField) + str(' ') +
                #       str(((profile.profile[i].TField + profile.getField(dist - recalcH, i)) / 2 +
                #                        (profile.profile[i].TField + profile.getField(dist + recalcH, i)) / 2)) + str(' ') +
                #       str((profile.getField(dist - recalcH, i) +
                #                        profile.getField(dist + recalcH, i))) + str(' ') +
                #       str((profile.getField(dist - 2 * recalcH, i) +
                #                        profile.getField(dist + 2 * recalcH, i))) + str(' ') +
                #       str((profile.getField(dist - 3 * recalcH, i) +
                #                        profile.getField(dist + 3 * recalcH, i))) + str(' ') +
                #       str((profile.getField(dist - 6 * recalcH, i) +
                #                        profile.getField(dist + 6 * recalcH, i))) + str(' ') +
                #       str((profile.getField(dist - 8 * recalcH, i) +
                #                        profile.getField(dist + 8 * recalcH, i))) + '\n')
                # print(str(profile.profile[i].TField) + str(' ') +
                #       str((profile.getField(dist - recalcH, i))) + str(' ') +
                #           str((profile.getField(dist + recalcH, i))) + str(' ') +
                #       str(profile.getField(dist - recalcH, i)) + str(' ') +
                #            str(profile.getField(dist + recalcH, i)) + str(' ') +
                #       str(profile.getField(dist - 2 * recalcH, i)) + str(' ') +
                #            str(profile.getField(dist + 2 * recalcH, i)) + str(' ') +
                #       str(profile.getField(dist - 3 * recalcH, i)) + str(' ') +
                #            str(profile.getField(dist + 3 * recalcH, i)) + str(' ') +
                #       str((profile.getField(dist - 6 * recalcH, i) +
                #                        profile.getField(dist + 6 * recalcH, i))) + str(' ') +
                #       str((profile.getField(dist - 8 * recalcH, i) +
                #                        profile.getField(dist + 8 * recalcH, i))) + '\n')

                record = Record(profile.profile[i].X, profile.profile[i].Y, fieldT, 0, 0, profile.profile[i].Date,
                                profile.profile[i].Time, profile.profile[i].lat, profile.profile[i].lon,
                                profile.profile[i].elev - recalcH, 0, 0, 0)
                field.AddRecord(record)

        field.endRecAdding()
        return field

    def AddRecord(self, record):
        rec = record
        # print("Add rec")
        # rec.out()
        # record.out()

        if (self.firstRec == 1):
            rec.Distance = 0
            self.firstRec = 0
        else:
            dist = self.CalculateDistance(self.prevRec.X, self.prevRec.Y, rec.X, rec.Y)
            if (dist < self.profileDistance):
                rec.Distance = self.prevRec.Distance + dist
            else:
                self.Profiles.append(self.Profile)
                self.Profile = Profile()
                rec.Distance = 0
        self.Profile.profile.append(rec)
        self.prevRec = rec

    def endRecAdding(self):
        self.Profiles.append(self.Profile)
        for profile in self.Profiles:
            profile.createFunc()

    def out(self):
        lines = []
        for profile in self.Profiles:
            for record in profile.profile:
                lines.append(str(record.out()) + '\n')
        return lines

    def CalculateDistance(self, X1, Y1, X2, Y2):
        return ((X1 - X2) ** 2 + (Y1 - Y2) ** 2) ** 0.5

        # def RecalcField(self):
