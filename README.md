# PES-Atttendence-Checker

> This project has been discontinued and is no longer functional.

This is a Pet Project to learn Data Scraping and GUI in python

It Calculates How Many Classes The User Is Ahead Or Behind Of A Set Attendence Limit By Checking The Attendence From pesuacademy
It Then Shows How Many Classes Required To Get Back To That Limit If Behind or How Many Can Be Missed If Ahead

# Table of Content


| Topic           	| Shortcut                              	|
|-----------------	|---------------------------------------	|
| Features        	|  [Features](#features)               	|
| How it Works    	|  [How it Works](#how-it-works)       	|
| Requirements    	|  [Requirements](#requirements)       	|
| Updates         	|  [Updates](#updates)                 	|
| Planned Updates 	|  [Planned Updates](#planned-updates) 	|


# Features

 - Checks pesuacademy.com to find your Attendence 
 - Calculate how many Classes are Needed on be Above a Limit if Below it or how many Can be Missed if Above the Limit
 - Saves Password if Required
 - Completly GUI Based
 
 
 # How it Works
 

 
  - It Uses the Data Entered in the Login Screen and puts in into the [Pesuacademy Login Page](https://www.pesuacademy.com/Academy/)
  
  
    - If Remember Me is Ticked, it Writes the Data into a Json file if its Blank or Changed
   ![Login](https://user-images.githubusercontent.com/97384467/214359706-ddaccf57-9e14-422a-ac32-44cf46ac0c8d.png)
  
  - It then Navigates to the Attendece Section and Scraps that Data
  - Then the Output is Shown in a Brand New Window


      ![Output-1](https://user-images.githubusercontent.com/97384467/214766064-663b0539-be47-4129-b7ed-2ee45d42c8da.png)
  
     ![Output-2](https://user-images.githubusercontent.com/97384467/213769918-46e540ca-e9c5-4e16-8dd6-1b20373bf41e.png)
 
  
 # Requirements
 
 - Chromedriver is required, This Repo comes with the driver for verision 110.0.5481.178. If you have a newer version of chrome replace the driver with a newer version from the website 
 - You can Find out your chrome version by visiting Chrome Settings -> Help or putting chrome://settings/help in the SearchBar
  >You can download it from here [Download Chrome Driver](https://chromedriver.chromium.org/downloads)  (This is Needed for Selenium to take Data from Chrome)
  ><br>
  >Chrome is Required as this only works for Chrome so far
 
<br>

 -<b> Required Libraries will be Downloaded Automatically, in case they don't </b>
<br>
<br>

  - To Download Dependencies, Run
     ```
     pip install -r requirements.txt
     ```
 - <b>       OR      </b>

 - The Following Libraries are Needed to Run
    > selenium <br>
    > pandas <br>
    > json <br>
    > PySimpleGUI <br>


## Updates

- Fix the Sem 1 Calculation Logic that hasnt been updated yet
 - Add a Icon

## Planned Updates
 - Add Support for other Browsers as well
   > Seems like the chromedriver part has depreciated so gotta go back and fix that
