import csv
import requests
import json # used for reading config.json for db authentication credentials
from xml.dom import minidom # https://docs.python.org/3/library/xml.dom.minidom.html
import mysql.connector as mysql #import sqlite3  

#########################################################
# https://stackoverflow.com/questions/22586286/python-is-there-an-equivalent-of-mid-right-and-left-from-basic
#########################################################
def left(s, amount):    
    return s[:amount]
#########################################################
# XML source: https://www.treasury.gov/resource-center/data-chart-center/interest-rates/pages/textview.aspx?data=yield
#########################################################
class Treasury:        
    def __init__(self):
        super().__init__()

    def getTreasuryXML(self):
  
        # url of rss feed
  #      url = 'https://data.treasury.gov/feed.svc/DailyTreasuryYieldCurveRateData' # all-time, rates SI
        url = 'https://data.treasury.gov/feed.svc/DailyTreasuryYieldCurveRateData?$filter=month(NEW_DATE)%20eq%204%20and%20year(NEW_DATE)%20eq%202021'
  
        # creating HTTP response object from given url
        resp = requests.get(url)
  
        # saving the xml file
        with open('treasury.xml', 'wb') as f:
            f.write(resp.content)
    

    ######################################################################### 
    # does the main parsing of the Treasury XML using Python minidom class
    # help reference: https://www.oreilly.com/library/view/python-xml/0596001282/ch04s04.html
    #########################################################################
    def parseXML(self):

        with open('config.json') as fp:
            configData = json.load(fp)

        # https://www.thepythoncode.com/article/connect-to-a-remote-mysql-server-in-python
        mydb = mysql.connect(host=configData['host'], database=configData['database'], user=configData['username'], password=configData['password'])
        print("Connected to:", mydb.get_server_info())
        mycursor = mydb.cursor()

        tsyGovLink = ""
        mydoc = minidom.parse('treasury.xml')
        items = mydoc.getElementsByTagName('entry')


        
        for elem in items:            
            if (elem.childNodes[1].tagName == "id"):
                tsyGovLink = elem.childNodes[1].firstChild.data #gets the hyperlink to the treasury gov website
            if (elem.childNodes[13].tagName == "content"):
                for x in range(1,elem.childNodes[13].childNodes[1].childNodes.length):
                    if (elem.childNodes[13].childNodes[1].childNodes[x].nodeType == elem.ELEMENT_NODE):
                        mytag = elem.childNodes[13].childNodes[1].childNodes[x].tagName 
                        if (mytag == "d:NEW_DATE"):
                            tsyDate = elem.childNodes[13].childNodes[1].childNodes[x].firstChild.data

                        if (left(mytag,5)=="d:BC_"):    # this is the prefix US Treasury uses for rates
                            if (elem.childNodes[13].childNodes[1].childNodes[x].hasAttribute('m:null') and elem.childNodes[13].childNodes[1].childNodes[x].getAttribute('m:null') == 'true'):
                                assert(true)
                            elif (elem.childNodes[13].childNodes[1].childNodes[x].hasAttribute('m:null')==False):
                                if (mytag == "d:BC_1YEAR"):
                                    
                                    y1 = elem.childNodes[13].childNodes[1].childNodes[x].firstChild.data

                                    sql = "INSERT INTO TSY_HISTORICALS(URL, 1Y)  "
                                    sql += "VALUES(" + chr(39) + tsyGovLink + chr(39) + "," + y1 + ")"

                                    mycursor.execute(sql)
                                    mydb.commit()
                        """
                        elif (mytag == "d:BC_1MONTH"):
                            print('  1 mo: ' + str(elem.childNodes[13].childNodes[1].childNodes[x].firstChild.data))
                        elif (mytag == "d:BC_2MONTH"):
                            print('  2 mo: ' + str(elem.childNodes[13].childNodes[1].childNodes[x].firstChild.data))
                        elif (elem.childNodes[13].childNodes[1].childNodes[x].tagName == "d:BC_3MONTH"):
                            print('  3 mo: ' + str(elem.childNodes[13].childNodes[1].childNodes[x].firstChild.data))
                        elif (elem.childNodes[13].childNodes[1].childNodes[x].tagName == "d:BC_6MONTH"):
                            print('  6 mo: ' + str(elem.childNodes[13].childNodes[1].childNodes[x].firstChild.data))
                        elif (elem.childNodes[13].childNodes[1].childNodes[x].tagName == "d:BC_1YEAR"):
                            print('  1Y: ' + str(elem.childNodes[13].childNodes[1].childNodes[x].firstChild.data))
                        elif (elem.childNodes[13].childNodes[1].childNodes[x].tagName == "d:BC_2YEAR"):
                            print('  2Y: ' + str(elem.childNodes[13].childNodes[1].childNodes[x].firstChild.data))
                        elif (elem.childNodes[13].childNodes[1].childNodes[x].tagName == "d:BC_3YEAR"):
                            print('  3Y: ' + str(elem.childNodes[13].childNodes[1].childNodes[x].firstChild.data))
                        elif (elem.childNodes[13].childNodes[1].childNodes[x].tagName == "d:BC_5YEAR"):
                            print('  5Y: ' + str(elem.childNodes[13].childNodes[1].childNodes[x].firstChild.data))
                        elif (elem.childNodes[13].childNodes[1].childNodes[x].tagName == "d:BC_7YEAR"):
                            print('  7Y: ' + str(elem.childNodes[13].childNodes[1].childNodes[x].firstChild.data))
                        elif (elem.childNodes[13].childNodes[1].childNodes[x].tagName == "d:BC_10YEAR"):
                            print('  10Y: ' + str(elem.childNodes[13].childNodes[1].childNodes[x].firstChild.data))
                        elif (elem.childNodes[13].childNodes[1].childNodes[x].tagName == "d:BC_20YEAR"):
                            print('  20Y: ' + str(elem.childNodes[13].childNodes[1].childNodes[x].firstChild.data))
                        elif (elem.childNodes[13].childNodes[1].childNodes[x].tagName == "d:BC_30YEAR"):
                            print('  30Y: ' + str(elem.childNodes[13].childNodes[1].childNodes[x].firstChild.data))
                        """



if __name__ == '__main__':
    myObj = Treasury()
    myObj.getTreasuryXML()
    myObj.parseXML()