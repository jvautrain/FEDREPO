from fedwriter import FedWriter
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
import sys
import os
import zipfile
import csv
import FIPS
import shutil
import time
import statistics
from EconSegCounty import EconSegTract
from EconSegCounty import EconSegCounty

########################
# Get arguments
inyear = sys.argv[1]
inmeasure = sys.argv[2]
inlocation = sys.argv[3]
instate = sys.argv[4]

#########################################
# Print Arguments
print(inyear)
print(inmeasure)
print(inlocation)
print(instate)
state = instate

#########################################
# Set Variables
url="https://factfinder.census.gov/bkmk/table/1.0/en/ACS/15_5YR/S1901/0100000US"
year=inyear
measurelist = []

#########################################
# Get Files
options = webdriver.ChromeOptions()
prefs = {"download.default_directory": inlocation}
chromedriver = inlocation + "/chromedriver.exe"
options.add_experimental_option("prefs", prefs)

print("Opening Web Driver")
########################
# Open Web driver
driver = webdriver.Chrome(executable_path=chromedriver, chrome_options=options)
driver.get(url)

########################
# Clicking  Year
time.sleep(5)
driver.find_element_by_partial_link_text(year).click()
print('Clicked year:'+year)

########################
# Going To Geograpy
clickfail=True
while clickfail:
    try:
        driver.find_element_by_id('addRemoveGeo_btn').click()
        clickfail=False
    except:
        clickfail=True
print("Going geography Button")

########################
# Waiting for Alert Window
alertnotopen=True
while alertnotopen:
    if EC.alert_is_present:
        driver.switch_to.alert
        alertnotopen=False
    else:
        alertnotopen=True
print("Gone to alert")

########################
# Selecting County
summaryclickfail=True
while summaryclickfail:
    try:
        driver.find_element_by_id('summaryLevel').click()
        driver.find_element_by_xpath("//select[@id='summaryLevel']//option[contains(.,'140')]").click()
        summaryclickfail=False
    except:
        summaryclickfail=True
print("selected county")

########################
# Picking State
stateclickfail=True
while stateclickfail:
    try:
        driver.find_element_by_xpath("//select[@id='state']//option[contains(.,'" + state + "')]").click()
        stateclickfail=False
    except:
        stateclickfail=True
print("Select state")

########################
# Confirming Geography
selectclickfail=True
while selectclickfail:
    try:
        driver.find_element_by_xpath("//select[@id='geoAssistList']//option[contains(.,'All Census Tracts within')]").click()
        selectclickfail = False
    except:
        selectclickfail=True
print("Select all tracts in state: "+state)

########################
# Setting Geography
addselectclickfail=True
while addselectclickfail:
    try:
        driver.find_element_by_id('addtoyourselections').click()
        addselectclickfail=False
    except:
        addselectclickfail=True
print("add to your selections")
time.sleep(5)

########################
# Show Table
showtableclickfail=True
while showtableclickfail:
    try:
        driver.find_element_by_id("showTableBtn").click()
        showtableclickfail = False
    except:
        showtableclickfail = True
print("Show Table: Waiting 10")
time.sleep(10)
print("show table")

########################
# Start Table Modify
clickfail = True
while clickfail:
    try:
        driver.find_element_by_id('modify_btn').click()
        clickfail = False
    except:
        clickfail = True
print("Hit modify button")

########################
# Transposing Rows
clickfail = True
while clickfail:
    try:
        driver.find_element_by_link_text('Transpose Rows/Columns').click()
        clickfail = False
    except:
        clickfail = True
print("transpose rows,columns")
print('sleeping for 5')
time.sleep(5)

########################
# Clicking Download
clickfail = True
while clickfail:
    try:
        driver.find_element_by_id('dnld_btn').click()
        clickfail = False
    except:
        clickfail = True
print("clicking download")
print('sleeping for 10')
time.sleep(5)

########################
# Waiting for Alert Window
alertnotopen=True
while alertnotopen:
    if EC.alert_is_present:
        driver.switch_to.alert
        alertnotopen=False
    else:
        alertnotopen=True
print("Gone to alert")

########################
# Choosing FIle Type
clickfail = True
while clickfail:
    try:
        driver.find_element_by_id('dnld_decision_use').click()
        clickfail = False
    except:
        clickfail = True
print("select use")

########################
# Launching File Compiler
clickfail = True
while clickfail:
    try:
        print("attempt")
        driver.find_element_by_id("yui-gen1-button").click()
        clickfail = False
    except:
        print("fail")
        clickfail = True
print("Click OK")
print('sleeping for 10')
time.sleep(10)

########################
# Launching File Compiler
clickfail = True
while clickfail:
    try:
        driver.find_element_by_id("yui-gen3-button").click()
        clickfail = False
    except:
        clickfail = True
print("clicked download button")
print("waiting 10 seconds")
time.sleep(10)
driver.quit()
#*********************************************************************

year=inyear[2:4]
filename="ACS_"+ year+"_5YR_S1901"
tractList=[]
countyList=[]
#######################
# Unzip File
zipsuccess = 0
while zipsuccess == 0:
    try:
        zip_ref = zipfile.ZipFile(inlocation + "\\" + filename+".zip", 'r')
        zip_ref.extractall(inlocation + "\\" + filename, members=None, pwd=None)
        zip_ref.close()
        zipsuccess = 1
    except:
        zipsuccess = 0

#######################
# Remove Zipfile
os.remove(inlocation + "\\" + filename+".zip")

#################################
# extract csv
CSVFile = inlocation + "\\" +filename+"\\"+ filename+"_with_ann.csv"
with open(CSVFile) as CSVData:
    reader = csv.reader(CSVData, delimiter=',', quotechar='"')
    counter=0
    for row in reader:
        counter += 1
        if counter>3:
            tractfull=row[2]
            firstcomma = tractfull.find(",")
            countyfull=tractfull[firstcomma+2:len(tractfull)]
            secondcomma=countyfull.find(",")
            state = countyfull[secondcomma + 2:len(countyfull)]
            tract=tractfull[0:firstcomma]
            county=countyfull[0:secondcomma]
            econSegTract = EconSegTract(tract,county, state, inyear)
            econSegTract.set_band1(row[11])
            econSegTract.set_band2(row[19])
            econSegTract.set_band3(row[27])
            econSegTract.set_band4(row[35])
            econSegTract.set_band5(row[43])
            econSegTract.set_band6(row[51])
            econSegTract.set_band7(row[59])
            econSegTract.set_band8(row[67])
            econSegTract.set_band9(row[75])
            econSegTract.set_band10(row[83])
            econSegTract.set_FIPS()
            # econSegTract.print()
            tractList.append(econSegTract)
print(len(tractList))
CSVData.close()

#################################
# create county list
print("Startign County List")
for tract in tractList:
    matched=False
    for countyRow in countyList:
        if countyRow.countyName==tract.countyName:
            matched=True
    if not(matched):
        econSegCounty = EconSegCounty(tract.countyName, tract.stateName, tract.year)
        countyList.append(econSegCounty)
print("COunty List Created")
print(str(len(countyList)))

#################################
# collecting tract daa by county
for countyRow in countyList:
    countyRow.set_FIPS()
    tractcount=0
    band1=[]
    band2=[]
    band3=[]
    band4=[]
    band5=[]
    band6=[]
    band7=[]
    band8=[]
    band9=[]
    band10=[]
    for tract in tractList:
        if tract.countyName==countyRow.countyName:
            tractcount+=1
            try:
                band1.append(float(tract.band1))
                band2.append(float(tract.band2))
                band3.append(float(tract.band3))
                band4.append(float(tract.band4))
                band5.append(float(tract.band5))
                band6.append(float(tract.band6))
                band7.append(float(tract.band7))
                band8.append(float(tract.band8))
                band9.append(float(tract.band9))
                band10.append(float(tract.band10))
            except:
                tractcount-=1
    countyRow.set_band1_med(statistics.median(band1))
    countyRow.set_band2_med(statistics.median(band2))
    countyRow.set_band3_med(statistics.median(band3))
    countyRow.set_band4_med(statistics.median(band4))
    countyRow.set_band5_med(statistics.median(band5))
    countyRow.set_band6_med(statistics.median(band6))
    countyRow.set_band7_med(statistics.median(band7))
    countyRow.set_band8_med(statistics.median(band8))
    countyRow.set_band9_med(statistics.median(band9))
    countyRow.set_band10_med(statistics.median(band10))
    countyRow.set_tractCount(tractcount)

#################################
# calculate differences to median
for countyRow in countyList:
    print(countyRow.countyName)
    for tract in tractList:
        if tract.countyName == countyRow.countyName:
            countyRow.set_band1_diff(countyRow.calc_diff(tract.band1,countyRow.band1_med))
            countyRow.set_band2_diff(countyRow.calc_diff(tract.band2, countyRow.band2_med))
            countyRow.set_band3_diff(countyRow.calc_diff(tract.band3, countyRow.band3_med))
            countyRow.set_band4_diff(countyRow.calc_diff(tract.band4, countyRow.band4_med))
            countyRow.set_band5_diff(countyRow.calc_diff(tract.band5, countyRow.band5_med))
            countyRow.set_band6_diff(countyRow.calc_diff(tract.band6, countyRow.band6_med))
            countyRow.set_band7_diff(countyRow.calc_diff(tract.band7, countyRow.band7_med))
            countyRow.set_band8_diff(countyRow.calc_diff(tract.band8, countyRow.band8_med))
            countyRow.set_band9_diff(countyRow.calc_diff(tract.band9, countyRow.band9_med))
            countyRow.set_band10_diff(countyRow.calc_diff(tract.band10, countyRow.band10_med))
    countyRow.set_Segregation()

#################################
# remove directory

shutil.rmtree(inlocation + "\\" +filename+"\\")

#################################
# create writing object
writer = FedWriter(inmeasure, inlocation)

#################################
# push list into writer and write
for county in countyList:
    writer.add(county.year+"-01-01", county.segregationFactor, county.FIPS)
    # print(obj.Date+"|"+ str(obj.count) + "|" + obj.FIPS)
    writer.output_msr_file()
