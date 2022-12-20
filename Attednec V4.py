from selenium import webdriver
from selenium import *
import pandas as pd
import time
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

# Attendence Calcuation
def attendence(Subject ,Classes = '0/0', attendence_limit = 80, Percents = 0):
      count=0
      Classes_list = Classes.split('/')
      classesAttended = int(Classes_list[0])
      classesTaken = int(Classes_list[1])
      print('------------------------------------------------------------------------------------------')
      print('\t\t\t\t',ind,"\t\t\t\t")

      print("Current Percentage: ", Percents)
      print("Current Classes: ", Classes)

      if classesTaken<classesAttended:
            classesTaken,classesAttended=classesAttended,classesTaken

      if (classesAttended/classesTaken*100<attendence_limit):
            while (classesAttended/classesTaken*100<=attendence_limit):
                  count+=1
                  classesAttended+=1
                  classesTaken+=1
            print('Need '+str(count)+' Classes')
      else:                  
            while (classesAttended/classesTaken*100>attendence_limit):
                  count+=1
                  classesTaken+=1
            print('Can Bunk '+str(count)+' Classes')

      print('Min No of Classes to be Attended '+str(classesAttended)+'\nNo of Classes it will take Totally '+str(classesTaken))
      print("Percentage: "+str(round(classesAttended/classesTaken*100,2)))
      # print('------------------------------------------------------------------------------------------')
   




# ++++++++++++++++++++++++++++++++++++++++++++++++Scrapping Part++++++++++++++++++++++++++++++++++++++++++++++++
options = Options()

path_ = os.path.expanduser('~') + "\AppData\\Local\\Google\\Chrome\\User Data\\Default"
options.add_argument(f'user-data-dir={path_}/')
options.add_argument("--start-minimized")
options.page_load_strategy = 'normal'
browser = webdriver.Chrome(executable_path = r"chromedriver_win32\chromedriver.exe", options = options)
browser.minimize_window()


browser.get('https://www.pesuacademy.com/Academy/')

attendeceDelay = 10
btnDelay = 2
menuDelay = 25


browser.minimize_window()




# Submit
time.sleep(btnDelay)
btn = browser.find_element("xpath", '//*[@id="postloginform#/Academy/j_spring_security_check"]').click()

# Attendece Menu
time.sleep(menuDelay)
attedenceScreen = browser.find_element("xpath", '//*[@id="menuTab_660"]/a/span[2]').click()

# Getting Info
time.sleep(btnDelay)
table = browser.find_element("xpath", '//*[@id="subjetInfo"]').text

item = table.split("\n")

print()
# making dataframe
ClassesAndPercentrage = []
row = []
subjectName = []
for i in item:
      split_list = i.split()
      subjectString = ''
      subjectName.append([subjectString + x for x in split_list[1:-2]])
      ClassesAndPercentrage.append(split_list[-2:])

# getting subject name
for i in range(len(subjectName)):
      subjectName[i] = " ".join(subjectName[i])

df = pd.DataFrame(ClassesAndPercentrage,columns=["Classes","Percentage"],index = subjectName)

print()
print(df)
print()

# attendence(Classes = (df.loc[row[0],"Classes"]), attendence_limit = 80)

for ind in df.index:
      attendence(Subject = ind,Classes = df["Classes"][ind], attendence_limit = 80, Percents = df["Percentage"][ind])


browser.close()
# exit()