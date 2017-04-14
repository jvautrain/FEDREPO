from datetime import date


class FedWriter:  # Creates and manage writing of files in Federal Reserve common format


    def __init__(self, measure, location):
        # defines list to write
        # measureList  is name vslue pair for each county
        self.measureName = measure
        self.measureList = []
        self.fileLocation = location

    def print(self):
        print(self.fileLocation)
        print(self.measureName)
        print(self.measureList)

    def leadingzero(self,num):
        returnvalue = ''
        if num < 10:
            returnvalue = '0'+str(num)
        else:
            returnvalue = str(num)
        return returnvalue

    def add(self, indate, inmeasure, incounty):
        measuredate = str(indate)
        measure = Measure()
        measure.setdate(indate)
        measure.setvalue(inmeasure)
        measure.setcounty(incounty)
        self.measureList.append(measure)

    def output_msr_county(self):
        amt = len(self.measureList)
        if amt>0:
            firstline = "DATE\t"+self.measureName+"\r"
            location = self.fileLocation+"\\"+self.measureName+".txt"
            file = open(location, 'w')
            file.write(firstline)

            counter = 0
            while counter <= amt-1:
                file.write(self.measureList[counter][0]+"\t"+str(self.measureList[counter][1])+"\r")
                counter += 1
            file.close()

    def output_msr_file(self):
        datelist=[]
        countylist =[]
        for rec in self.measureList:
            if str(rec.date) not in datelist:
                datelist.append(str(rec.date))

        for rec in self.measureList:
            if str(rec.county) not in countylist:
                countylist.append(str(rec.county))
        datelist.sort()
        countylist.sort()
        firstline = "COUNTY"

        for dateevent in datelist:
            firstline = firstline + "\t" + dateevent

        firstline = firstline + "\r"
        location = self.fileLocation+"\\"+self.measureName+".txt"
        file = open(location, 'w')
        file.write(firstline)
        for currcounty in countylist:
            linestr = currcounty
            for currdate in datelist:
                valuepts = [measure for measure in self.measureList if (measure.county == currcounty and str(measure.date) == str(currdate))]
                for valpt in valuepts:
                    linestr = linestr + "\t" + str(valpt.value)
            linestr = linestr + "\r"
            file.write(linestr)
        file.close()

class Measure:
    def __init__(self):
        self.date = ""
        self.value = float(0)
        self.county = ""

    def setdate(self, indate):
        self.date = indate

    def setvalue(self, invalue):
        self.value = float(invalue)

    def setcounty(self,incounty):
        self.county = incounty

