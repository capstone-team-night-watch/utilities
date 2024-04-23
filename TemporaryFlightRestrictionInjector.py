#!/usr/bin/env python3

############################################################
# Auth: Ethan Wagner
# Date: 10-26-23  (Due: 10-26-23)
# Course: 2850 (Sec: 850)
# Desc:  Assignment 8, Movie Scraper
#############################################################

import sys
import string
import requests
from operator import itemgetter
from bs4 import BeautifulSoup
from urllib.request import urlopen

url = "https://tfr.faa.gov/tfr2/list.html"
injectUrl = "http://ec2-13-58-87-154.us-east-2.compute.amazonaws.com:6000/notam/tfr"
#injectUrl = "http://localhost:8080/notam/tfr"

#default error if no file is passed in
def argError():
     print(f'Usage: {sys.argv[0]}')    

def main():

    # Array for all values. The key is the current position.
    notams = []

    page = urlopen(url)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")

    allTfrNotams = soup.find_all("u")

    #parses the information out of the table rows
    for notam in allTfrNotams[1:len(allTfrNotams)]: # row 0 is the headings
        notams.append(notam.getText())

    #Now with an array of all current TFR notams, we can pull the notam's raw text to parse later on.
    #The current method to gain this information is at the following link where X_XXXX represents the notam number.
    #https://tfr.faa.gov/save_pages/notam_actual_X_XXXX.html
    
    for notam in notams:
        page = urlopen(f'https://tfr.faa.gov/save_pages/notam_actual_{notam.replace('/', '_')}.html')
        html = page.read().decode("utf-8")
        soup = BeautifulSoup(html, "html.parser")
        notamBodyParse = soup.find_all("td")
        
        notamArry = notamBodyParse[3].getText().strip().split("\n\n\n\r\n\r\n")

        for singleNotam in notamArry:
            print(requests.put(injectUrl, data=singleNotam))




#precheck before actually starting the program. No arguments expected
#argv[0] is the file name
if __name__ == '__main__':
    if (len(sys.argv) == 1): # catches to many or to few arguments
        main()
    else:
        argError()


