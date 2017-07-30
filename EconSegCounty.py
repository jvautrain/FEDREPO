import FIPS
class EconSegTract:

    def __init__(self, tract, countyname, statename, inYear):
        self.tract=tract
        self.countyName = countyname
        self.stateName = statename
        self.year = inYear
        self.FIPS = ""
        self.band1 = 0
        self.band2 = 0
        self.band3 = 0
        self.band4 = 0
        self.band5 = 0
        self.band6 = 0
        self.band7 = 0
        self.band8 = 0
        self.band9 = 0
        self.band10 = 0

    def set_FIPS(self):
        slist=FIPS.states
        for st in slist:
            # print(self.stateName.upper()+"|"+str(st[1]).upper())
            if self.stateName.upper() == str(st[1]).upper():
                self.stateName=st[0]
        fList=FIPS.counties
        for fip in fList:
            if fip[0]==self.stateName and fip[1].upper()==self.countyName.upper():
                self.FIPS=fip[2]

    def set_band1(self,inVal):
        self.band1=inVal

    def set_band2(self,inVal):
        self.band2=inVal

    def set_band3(self,inVal):
        self.band3=inVal

    def set_band4(self,inVal):
        self.band4=inVal

    def set_band5(self,inVal):
        self.band5=inVal

    def set_band6(self,inVal):
        self.band6=inVal

    def set_band7(self,inVal):
        self.band7=inVal

    def set_band8(self,inVal):
        self.band8=inVal

    def set_band9(self,inVal):
        self.band9=inVal

    def set_band10(self,inVal):
        self.band10=inVal

    def print(self):
        print("tractname: " + self.tract)
        print("countyname: " + self.countyName)
        print("StateName : "+self.stateName)
        print("Year: "+self.year)
        print("FIPS: "+ self.FIPS)
        print("Band: " + str(self.band1) +"|"+ str(self.band2) +"|"+ str(self.band3) +"|"+ str(self.band4) +"|"+ str(self.band5) +"|"+ str( self.band6) +"|"+ str(self.band7) +"|"+ str(self.band8) +"|"+ str(self.band9) +"|"+ str(self.band10))

class EconSegCounty:
    def __init__(self, countyname, statename, inYear):
        self.countyName = countyname
        self.stateName = statename
        self.year = inYear
        self.FIPS = ""
        self.tractcount = float(0)
        self.band1_med = float(0)
        self.band2_med = float(0)
        self.band3_med = float(0)
        self.band4_med = float(0)
        self.band5_med = float(0)
        self.band6_med = float(0)
        self.band7_med = float(0)
        self.band8_med = float(0)
        self.band9_med = float(0)
        self.band10_med = float(0)
        self.band1_diff = float(0)
        self.band2_diff = float(0)
        self.band3_diff = float(0)
        self.band4_diff = float(0)
        self.band5_diff = float(0)
        self.band6_diff = float(0)
        self.band7_diff = float(0)
        self.band8_diff = float(0)
        self.band9_diff = float(0)
        self.band10_diff = float(0)
        self.segregationFactor = float(0)

    def set_tractCount(self,inVal):
        self.tractcount=inVal

    def set_band1_med(self,inVal):
        self.band1_med=inVal

    def set_band2_med(self,inVal):
        self.band2_med=inVal

    def set_band3_med(self,inVal):
        self.band3_med=inVal

    def set_band4_med(self,inVal):
        self.band4_med=inVal

    def set_band5_med(self,inVal):
        self.band5_med=inVal

    def set_band6_med(self,inVal):
        self.band6_med=inVal

    def set_band7_med(self,inVal):
        self.band7_med=inVal

    def set_band8_med(self,inVal):
        self.band8_med=inVal

    def set_band9_med(self,inVal):
        self.band9_med=inVal

    def set_band10_med(self,inVal):
        self.band10_med=inVal

    def calc_diff(self,inVal,median):
        try:
            retval = float(.1) * float(abs(float(median)-float(inVal)))/(float(median)*self.tractcount)
            # print("Median: " + str(median) + " | inVal: " + str(inVal) + " | tract: "+str(self.tractcount)
            #       + " | Return: "+str(retval))
        except:
            retval = float(0)
        return retval

    def set_band1_diff(self,inVal):
        self.band1_diff=float(inVal)

    def set_band2_diff(self,inVal):
        self.band2_diff+=float(inVal)

    def set_band3_diff(self,inVal):
        self.band3_diff+=float(inVal)

    def set_band4_diff(self,inVal):
        self.band4_diff+=float(inVal)

    def set_band5_diff(self,inVal):
        self.band5_diff+=float(inVal)

    def set_band6_diff(self,inVal):
        self.band6_diff+=float(inVal)

    def set_band7_diff(self,inVal):
        self.band7_diff+=float(inVal)

    def set_band8_diff(self,inVal):
        self.band8_diff+=float(inVal)

    def set_band9_diff(self,inVal):
        self.band9_diff+=float(inVal)

    def set_band10_diff(self,inVal):
        self.band10_diff+=float(inVal)

    def set_Segregation(self):
        self.segregationFactor=float(self.band1_diff)+float(self.band2_diff)+float(self.band3_diff)+float(self.band4_diff)+float(self.band5_diff)+float(self.band6_diff)+float(self.band7_diff)+float(self.band8_diff)+float(self.band9_diff) + float(self.band10_diff)

    def print(self):
        print("countyname: " + self.countyName)
        print("StateName : "+self.stateName)
        print("Year: "+self.year)
        print("FIPS: "+ self.FIPS)
        print("Segregation Factor: " + str(self.segregationFactor))
        print("Band: " + str(self.band1_med) +"|"+ str(self.band2_med)
              +"|"+ str(self.band3_med) +"|"+ str(self.band4_med) +"|"
              + str(self.band5_med) +"|"+ str( self.band6_med) +"|"
              + str(self.band7_med) +"|"+ str(self.band8_med) +"|"
              + str(self.band9_med) +"|"+ str(self.band10_med))

    def set_FIPS(self):
        # print(self.stateName+"|"+self.countyName)
        for fipsrow in FIPS.counties:
            if fipsrow[0]==self.stateName and str.strip(fipsrow[1])==str.strip(self.countyName):
                self.FIPS=fipsrow[2]
                # print(self.FIPS)