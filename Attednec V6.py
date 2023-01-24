# V6
# - Remember Me Functionality Added
# - Fixed the TryElement Function
# - Fixed Fonts
# - Fixed the Loading Window
# - Added Default Username and Password
# - Added json file to store the username and password
# - Added Error Handling for Wrong Username and Password
# - Added Error Handling for Internet Connection
# - Added Timeout Limit for the Webpage to Load


from selenium import webdriver
from selenium import *
import pandas as pd
import time
import os
from selenium.webdriver.chrome.options import Options
import PySimpleGUI as sg
import json



def buildGUI():
    '''
    ------------------------------------------------------
    Function to build Login GUI
    ------------------------------------------------------
    '''

    # read secrets.json file
    print('Reading Files....')

    if os.path.exists('secrets.json'):
        with open('secrets.json') as f:
            data = json.load(f)
            DefaultUsername = data['Username'].strip()
            DefaultPassword= data['Password'].strip()
    else:
        with open('secrets.json','w') as f:
            data = {'Username':'','Password':''}
            json.dump(data,f)
            DefaultUsername = ''
            DefaultPassword = ''
    
    print('Reading Files....Done')


    # sg.theme('Black')   # Add a touch of color
    sg.theme('DarkBrown2')
    # make a window which takes username and password as input
    layout = [[sg.Text('Enter the Username:',font=("Cascadia Code",12) ),sg.Input(key='-USERNAME-',background_color='white',default_text = DefaultUsername)],
                [sg.Text('Enter the Password:',font=("Cascadia Code",12)),sg.Input(key='-PASSWORD-',password_char='*',background_color='white',default_text= DefaultPassword)],
                [sg.Text('Enter the Attendence Limit:',font=("Cascadia Code",12)),sg.Input(key='-ATTENDENCE-',default_text='80',background_color='white')],
                [sg.Button('Submit',font=("Cascadia Code",12),focus= True),sg.Button('Cancel',font=("Cascadia Code",12)),sg.Checkbox('Remember Me',font=("Cascadia Code",12),default= True,key='-REMEMBER-')]]
    window = sg.Window('Attendence Calculator',layout = layout,grab_anywhere=True)
    event, values = window.read()

    print('Waiting for the User to Enter the Credentials....')

    if event == 'Submit':
        print('Credentials Entered....')
        if (values['-REMEMBER-'] and values['-USERNAME-'] != '' or values['-PASSWORD-'] != '' ):
            data['Username'] = values['-USERNAME-']
            data['Password'] = values['-PASSWORD-']
            with open('secrets.json','w') as f:
                json.dump(data,f)
        
        window.close()        
        main(username = values['-USERNAME-'],password = values['-PASSWORD-'])
    
    elif event == 'Cancel' or event == sg.WIN_CLOSED:
            print('Cancelled')
            window.close()
            browser.close()
            exit()

    window.close()


def OpenBrowser():
    '''
    ------------------------------------------------------
    Function to open the browser and Webpage
    ------------------------------------------------------

    Returns:
        browser: [webdriver]
    '''
    # ++++++++++++++++++++++++++++++++++++++++++++++++Scrapping Part++++++++++++++++++++++++++++++++++++++++++++++++
    global browser
    options = Options()

    options.add_argument("--start-minimized")
    browser = webdriver.Chrome(executable_path = r"chromedriver_win32\chromedriver.exe", options = options)
    browser.minimize_window()

    browser.get('https://www.pesuacademy.com/Academy/')

    return browser

def TryElement(browser,elementType,element,action = None, Timeout = 120):
    '''
    ------------------------------------------------------
    Function to click the element once it is present in the webpage
    ------------------------------------------------------

    @param
    browser: [webdriver]
    elementType: [str]
    element: [str]
    action: [str] (click,text,None) [default = None]
    Timeout: [int] [default = 120 seconds]

    Returns:
        Element: [webdriver element]
    '''
    checking = True
    while checking:
        Timeout -= 1

        if Timeout == 0 and action != 'Input':
            # make a popup window for timeout error
            LoadingWindow.close()
            sg.popup('Timeout Error','Please Check your Internet Connection and Try Again',title='Error',font=("Cascadia Code",12))
            print('Timeout Error')
            exit()
        elif Timeout == 0 and action == 'Input':
            # make a popup window for timeout error
            LoadingWindow.close()
            sg.popup('Timeout Error','Wrong Username or Password',title='Error',font=("Cascadia Code",12))
            print('Wrong Username or Password')
            exit()
        try:
            if action == 'Input':
                Element = browser.find_element(elementType, element)
            elif action == 'click':
                Element = browser.find_element(elementType, element).click()
            elif action == 'text':
                Element = browser.find_element(elementType, element).text
        except:
            time.sleep(1)
            print('Waiting for the Page to Load')
        else:
            checking = False
    return Element
def Scraping(browser,username,password):
    '''
    ------------------------------------------------------
    Function to scrap the data from the webpage
    ------------------------------------------------------

    @param
    browser: [webdriver]
    username: [str]
    password: [str]

    Returns:
        df: [pandas dataframe]
    '''

    # Login
    
    # TODO: Fix the TryElement function
    print('Logging In....')
    user = TryElement(browser,"xpath", '//*[@id= "j_scriptusername" ]',action= "Input")
    pwd = TryElement(browser,"xpath", '/html/body/div[2]/div[1]/div/div[2]/form/fieldset/div[2]/input',action= "Input")
    
    user.send_keys(username)
    pwd.send_keys(password)

    # Submit Button
    TryElement(browser,"xpath", '//*[@id="postloginform#/Academy/j_spring_security_check"]',action= 'click')

    print('Logged In')

    print('Getting the Data....')
    # Attendece Menu
    TryElement(browser,"xpath", '//*[@id="menuTab_660"]/a/span[2]',action= 'click')

    # Getting Info
    table = TryElement(browser,"xpath", '//*[@id="subjetInfo"]',action= 'text')
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
    df.index.name = "Subject"

    print('Data Scraped')
    return df

# Attendence Calcuation
def attendence(Subject ,Classes = '0/0', attendence_limit = 80, Percents = 0):
    '''
    ------------------------------------------------------
    Function to calculate the attendence
    ------------------------------------------------------

    @param
    Subject: Subject Name [str]
    Classes: Classes Attended and Total Classes [str]
    attendence_limit: Attendence Limit [int]
    Percents: Current Percentage [int]

    Returns:
        stringItem: [str]   
    '''
    print('Calculating Attendence....')

    if type(attendence_limit) == str:
        attendence_limit = 80
    attendence_limit = int(attendence_limit)
    count=0
    Classes_list = Classes.split('/')
    classesAttended = int(Classes_list[0])
    classesTaken = int(Classes_list[1])
    stringItem = ''
    
    stringItem+='----------------------------------------------------------------------------------------------------\n'
    
    stringItem += f"\t\t\t\t{Subject}\t\t\t\t\n"

    stringItem += f"Current Percentage: {Percents}\n"

    stringItem += f"Current Classes: {Classes}\n"

    if classesTaken<classesAttended:
            classesTaken,classesAttended=classesAttended,classesTaken

    if (classesAttended/classesTaken*100<attendence_limit):
            while (classesAttended/classesTaken*100<=attendence_limit):
                count+=1
                classesAttended+=1
                classesTaken+=1
            stringItem += f"Need {count} Classes\n"
    else:                  
            while (classesAttended/classesTaken*100>attendence_limit):
                count+=1
                classesTaken+=1
            stringItem += f"Can Miss {count} Classes\n"

    stringItem += f"Min No of Classes to be Attended {classesAttended}\nNo of Classes it will take Totally {classesTaken}\n"
    
    stringItem += f"Percentage: {round(classesAttended/classesTaken*100,2)}\n"

    print('Attendence Calculated')
    return stringItem

def ShowData(df,TotalData,LoadingWindow,browser):
    '''
    ------------------------------------------------------
    Function to show the data in a new window
    ------------------------------------------------------

    @param
    df: [pandas dataframe]
    TotalData: [str]
    LoadingWindow: [sg.Window]
    browser: [webdriver]

    Returns:
        None
    '''
    browser.close()

    print('Closing the Browser....')

    print('Showing the Data....')
    print('Building the Window....')

    out = df.to_markdown(tablefmt='pipe', colalign=['center']*len(df.columns))
    
    col = [sg.Column([[sg.Text(out,font=('Courier'))],[sg.Text(TotalData,font=('Courier'))],[sg.Button('Ok',auto_size_button=True,font= ('Courier'))]],scrollable=True, element_justification='center',vertical_scroll_only=True)]
    layout = [col]
    
    newWindow = sg.Window('Data',layout=layout,resizable=True)
    LoadingWindow.close()
    event, values = newWindow.read()
    
    print('Window Built')

    print('Data Shown')

    if event == 'Ok' or event == sg.WIN_CLOSED:
        newWindow.close()
        print('Exiting....')
        print('Exited')
        print('Thank You')
        exit()

def main(username,password,attnLimit = 80):
    '''
    ------------------------------------------------------
    Main Function
    ------------------------------------------------------

    @param
    username: [str]
    password: [str]
    attnLimit: [int]

    Returns:
        None
    '''
    global LoadingWindow
    
    print("Loading....")

    LoadingWindow = sg.Window('Loading',[[sg.Text('Loading....',font=("Casadia Code",15))]])
    LoadingWindow.read(timeout=0)

    print("Opening Browser")
    browser = OpenBrowser()


    df = Scraping(browser=browser,username=username,password=password)

    # attendence(Classes = (df.loc[row[0],"Classes"]), attendence_limit = 80)
    TotalData = ""
    for ind in df.index:
            text = attendence(Subject = ind,Classes = df["Classes"][ind], attendence_limit = attnLimit, Percents = df["Percentage"][ind])
            TotalData += text

    ShowData(df,TotalData,LoadingWindow,browser)

if __name__ == "__main__":
    print('Starting....')
    print('Building GUI')
    buildGUI()
