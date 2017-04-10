from fedwriter import FedWriter
from selenium import webdriver
import sys
import csv
from businessstarts import BlsCount
from businessstarts import BusStarts
import businessdata
import os.path
import time

########################
# Get arguments

inlocation = sys.argv[2]
inmeasure = sys.argv[1]
measurelist=[]


print(inlocation)
print(inmeasure)
# print(inyear)
#########################################
# Looping through States
for url in businessdata.states:
    print(url)
    blslist = []
    for set in businessdata.quarters:
        print(set)
        ########################
        # Create Profile for Firefox
        profile = webdriver.FirefoxProfile()
        profile.accept_untrusted_certs = True
        profile.set_preference('browser.download.folderList', 2)  # custom location
        profile.set_preference('browser.download.manager.showWhenStarting', False)
        profile.set_preference('browser.download.dir', inlocation)
        profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "'text/plain, application/vnd.ms-excel, text/csv, text/comma-separated-values, application/octet-stream, application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        profile.set_preference("plugin.disable_full_page_plugin_for_types", "'text/plain, application/vnd.ms-excel, text/csv, text/comma-separated-values, application/octet-stream, application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        #########################
        # Open Web driver
        driver = webdriver.Firefox(profile)

        driver.get(url[2])
        driver.find_element_by_xpath("//select[@name='period']//option[contains(.,'" + set[0] + "')]").click()
        driver.find_element_by_name("Update").click()
        linknotthere=True
        while linknotthere:
            time.sleep(1)
            try:
                driver.find_element_by_link_text('CSV Data Feed').click()
                linknotthere=False
            except:
                linknotthere=True
        test=True
        path=inlocation + '\\bls_qcew_maps.csv'
        while test:
            time.sleep(1)
            if os.path.isfile(path):
                test=False
        with open(path) as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            print('CSV OPEN')

            counter=1
            for row in reader:
                print('csvrow:'+str(counter))
                if counter>1 and len(row[0])>1:
                    blsCount=BlsCount()
                    print(row)
                    blsCount.set_yearquarter(row[1])
                    blsCount.set_businesscount(row[2])
                    blsCount.set_FIPS(row[8])
                    blsCount.set_state(row[9])
                    blslist.append(blsCount)
                    blsCount.print()
                counter+=1
        driver.quit()
        test=True
        while test:
            time.sleep(1)
            try:

                test=False
                os.remove(path)
            except:
                test=False
    counter=0
    for set in businessdata.quarters:
        if counter>1:
            for rec in blslist:
                if (str(rec.get_quarter())+" "+str(rec.get_year()))==set[0]:
                    #print("into loop")
                    for rec2 in blslist:
                        # print(str(rec2.get_quarter()) + " " + str(rec2.get_year()))
                        # print(set[1])
                        # print(rec.get_FIPS()+"|"+rec2.get_FIPS())
                        if (str(rec2.get_quarter()) + " " + str(rec2.get_year())) == set[1] and rec.get_FIPS()==rec2.get_FIPS():
                            result=(int(rec.get_businesscount())-int(rec2.get_businesscount()))
                            bussstart = BusStarts()
                            bussstart.set_FIPS(rec.get_FIPS())
                            bussstart.set_measure(result)
                            bussstart.set_date(rec.get_date())
                            measurelist.append(bussstart)
                            break
        counter+=1
counter=0
#################################
# create writing object
writer = FedWriter(inmeasure, inlocation)

#################################
# push list into writer and write
for obj in measurelist:
    writer.add(obj.get_date(), obj.get_measure(), obj.get_FIPS())
    print(obj.get_date()+str(obj.get_measure())+obj.get_FIPS())
writer.output_msr_file()
