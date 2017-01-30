from datetime import date
from fedwriter import FedWriter
from selenium import webdriver
import zipfile
import requests
import sys
import os
import time
from os import walk
import dbf
import votecounty
from votecounty import VoteCounty
import shutil

########################
# Get arguments
inlocation = sys.argv[3]
inmeasure = sys.argv[2]
inyear = sys.argv[1]
countyvotes = []

#########################################
# for 2014 back to 2010
# for fileitem in votecounty.filelist:
#     print(fileitem)
#
#     ########################
#     # Create Profile for Firefox
#     profile = webdriver.FirefoxProfile()
#     profile.accept_untrusted_certs = True
#     profile.set_preference('browser.download.folderList', 2)  # custom location
#     profile.set_preference('browser.download.manager.', False)
#     profile.set_preference('browser.download.dir', inlocation)
#     profile.set_preference("browser.helperApps.neverAsk.saveToDisk",
#                            "application/zip;application/octet-stream;application/x-zip;application/x-zip-compressed")
#     profile.set_preference("plugin.disable_full_page_plugin_for_types", "application/zip")
#
#     #########################
#     # Open Web driver
#     driver = webdriver.Firefox(profile)
#     driver.get("https://www.eac.gov/research/election_administration_and_voting_survey.aspx")
#     driver.find_element_by_xpath("//*[@*[contains(., '" + fileitem[0] + "')]]").click()
#
#     ########################
#     # Wait for download
#     time.sleep(60)
#     driver.quit()
#
#     #######################
#     # Unzip File
#     zipsuccess=0
#     while zipsuccess == 0:
#         try:
#             zip_ref = zipfile.ZipFile(inlocation + "\\" + fileitem[1], 'r')
#             zip_ref.extractall(inlocation + "\\" + fileitem[2], members=None, pwd=None)
#             zip_ref.close()
#             zipsuccess = 1
#         except:
#             zipsuccess = 0
#     #######################
#     # Remove Zipfile
#     os.remove(inlocation + "\\" + fileitem[1] )
#
#     #######################
#     # Get Data from files
#
#     table = dbf.Table(inlocation + "\\" + fileitem[2] + "\\" + fileitem[3])
#     table.open()
#     print("TABLE RECS-" + str(fileitem[4]) + ":" + len(table).__str__())
#     for rec in table:
#         neednewrecord = True
#         for cv in countyvotes:
#             if str(rec.fipscode[0:5]) == str(cv.fipscode) and str(cv.votedate[0:4]) == str(fileitem[4]):
#                 countyvotes.remove(cv)
#                 cv.addvotes(rec.qf1a)
#                 countyvotes.append(cv)
#                 neednewrecord = False
#                 continue
#         if neednewrecord:
#             votec = VoteCounty()
#             votec.setcountyname(rec.jurisdicti)
#             votec.setfipscode(rec.fipscode[0:5])
#             votec.setdate(votecounty.getvotedate(fileitem[4]))
#             votec.addvotes(rec.qf1a)
#             countyvotes.append(votec)
#     table.close()
#
#     #######################
#     # Remove folder
#     shutil.rmtree(inlocation + "\\" + fileitem[2])
#
#     print("VOTES:" + len(countyvotes).__str__())
#################################################################
# 2008 code
########################
# Create Profile for Firefox
profile = webdriver.FirefoxProfile()
profile.accept_untrusted_certs = True
profile.set_preference('browser.download.folderList', 2)  # custom location
profile.set_preference('browser.download.manager.', False)
profile.set_preference('browser.download.dir', inlocation)
profile.set_preference("browser.helperApps.neverAsk.saveToDisk",
                       "application/zip;application/octet-stream;application/x-zip;application/x-zip-compressed")
profile.set_preference("plugin.disable_full_page_plugin_for_types", "application/zip")

#########################
# Open Web driver
driver = webdriver.Firefox(profile)
driver.get("https://www.eac.gov/research/election_administration_and_voting_survey.aspx")
driver.find_element_by_xpath("//*[@*[contains(., '2008 eavs dbf august 11 2010.zip')]]").click()

########################
# Wait for download
time.sleep(60)
driver.quit()

#######################
# Unzip File
zipsuccess=0
while zipsuccess == 0:
    try:
        zip_ref = zipfile.ZipFile(inlocation + "\\2008 eavs dbf august 11 2010.zip", 'r')
        zip_ref.extractall(inlocation + "\\2008 eavs dbf august 11 2010", members=None, pwd=None)
        zip_ref.close()
        zipsuccess = 1
    except:
        zipsuccess = 0
#######################
# Remove Zipfile
os.remove(inlocation + "\\2008 eavs dbf august 11 2010.zip")

#######################
# Get Data from files

table = dbf.Table(inlocation + "\\2008 eavs dbf august 11 2010\\County_DBF\\combined_sectionf.dbf")
table.open()
print("TABLE RECS-2008:" + len(table).__str__())
for rec in table:
    neednewrecord = True
    testrec=[str(rec[0])s3,[str(rec[1])],[str(rec[4])]]
    print(testrec)
    for cv in countyvotes:
        if str(rec[0][0:5]) == str(cv.fipscode) and str(cv.votedate[0:4]) == "2008":
            countyvotes.remove(cv)
            cv.addvotes(int(rec[4]))
            countyvotes.append(cv)
            neednewrecord = False
            continue
    if neednewrecord:
        votec = VoteCounty()
        votec.setcountyname(rec[1])
        votec.setfipscode(rec[0][0:5])
        votec.setdate(votecounty.getvotedate("2008"))
        votec.addvotes(int(rec[4]) if rec[4] is not None else 0)
        countyvotes.append(votec)
table.close()

#######################
# Remove folder
shutil.rmtree(inlocation + "\\2008 eavs dbf august 11 2010")

print("VOTES:" + len(countyvotes).__str__())
# driver.find_element_by_name("action-I Agree").click()
# time.sleep(5)
# driver.find_element_by_xpath("//select[@name='B_1']//option[text()='Year']").click()
# driver.find_element_by_xpath("//select[@name='B_2']//option[text()='County']").click()
# driver.find_element_by_xpath("//select[@name='V_D132.V1']//option[contains(.,'1999')]").click()
# driver.find_element_by_xpath("//select[@name='V_D132.V1']//option[contains(.,'All Years')]").click()
# driver.find_element_by_xpath("//select[@name='F_D132.V9']//option[contains(.,'Alabama')]").click()
# driver.find_element_by_xpath("//select[@name='F_D132.V9']//option[contains(.,'All')]").click()
# driver.find_element_by_name("action-Send").click()
# test = 0
# resultlist = []
# objlist = []
# while test == 0:
#     time.sleep(20)
#     try:
#         result = driver.find_element_by_class_name("response-form")
#         test = 1
#         print("Driver Captured")
#     except BaseException as e:
#         print(str(e))
#         test = 0
# for row in result.find_elements_by_tag_name('tr'):
#     headers = row.find_elements_by_tag_name('th')
#     tempresult = []
#     for header in headers:
#         tempresult.extend([header.text])
#     fields = row.find_elements_by_tag_name('td')
#     for field in fields:
#         tempresult.extend([str(field.text)])
#     resultlist.extend([tempresult])
# for rec in resultlist:
#     if str(rec[1]).find("(") > 0:
#         deathYear = DeathYear(rec[0])
#         deathYear.setcountystr(rec[1])
#         deathYear.setdeathcount(rec[2])
#         deathYear.setpopcount(rec[3])
#         deathYear.setcountycode()
#         deathYear.setdate()
#         objlist.append(deathYear)
#
# # x = 0
# # for rec in objlist:
# #     print(str(x)+": " + rec.print())
# #     x += 1

#
# inlocation = "C:\\Users\\joshu\\Documents\\WorkProjects\\fedmeasures"
# inmeasure = 'Banana'
# writer = FedWriter(inmeasure, inlocation)
#
# for obj in objlist:
#     writer.add(obj.measureDate, obj.deathCount, obj.countyCode)
# writer.output_msr_file()
#
# #for row in result.find_element_by_name('tbody'):
#     # cells = row.xpath('.//td/text()')
#     #print(cells[0])
#
#
# # datex = date(2016, 1, 15)
# # writer = FedWriter(inmeasure, inlocation)
# # writer.add(datex, 1324)
# # writer.add(datex, 1115)
# # writer.output()
