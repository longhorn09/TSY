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
        url = 'https://data.treasury.gov/feed.svc/DailyTreasuryYieldCurveRateData' # all-time, rates SI
        #url = 'https://data.treasury.gov/feed.svc/DailyTreasuryYieldCurveRateData?$filter=month(NEW_DATE)%20eq%204%20and%20year(NEW_DATE)%20eq%202021'
  
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
                y1 = -99 ; y2 = -99; y3 = -99; y5 = -99; y7 = -99; y10 = -99; y20 = -99; y30 = -99
                m1 = -99; m2 = -99; m3 = -99; m6 = -99
                for x in range(1,elem.childNodes[13].childNodes[1].childNodes.length):
                    if (elem.childNodes[13].childNodes[1].childNodes[x].nodeType == elem.ELEMENT_NODE):
                        mytag = elem.childNodes[13].childNodes[1].childNodes[x].tagName 
                        if (mytag == "d:NEW_DATE"):
                            tsyDate = elem.childNodes[13].childNodes[1].childNodes[x].firstChild.data
                        if (left(mytag,5)=="d:BC_"):    # this is the prefix US Treasury uses for rates
                            if (elem.childNodes[13].childNodes[1].childNodes[x].hasAttribute('m:null') and elem.childNodes[13].childNodes[1].childNodes[x].getAttribute('m:null') == 'true'):
                                assert(True)
                            elif (elem.childNodes[13].childNodes[1].childNodes[x].hasAttribute('m:null')==False):
                                if (mytag == "d:BC_1MONTH"):                                    
                                    m1 = elem.childNodes[13].childNodes[1].childNodes[x].firstChild.data
                                elif (mytag == "d:BC_2MONTH"):                                    
                                    m2 = elem.childNodes[13].childNodes[1].childNodes[x].firstChild.data
                                elif (mytag == "d:BC_3MONTH"):                                    
                                    m3 = elem.childNodes[13].childNodes[1].childNodes[x].firstChild.data
                                elif (mytag == "d:BC_6MONTH"):                                    
                                    m6 = elem.childNodes[13].childNodes[1].childNodes[x].firstChild.data
                                elif (mytag == "d:BC_1YEAR"):                                    
                                    y1 = elem.childNodes[13].childNodes[1].childNodes[x].firstChild.data
                                elif (mytag == "d:BC_2YEAR"):
                                    y2 = elem.childNodes[13].childNodes[1].childNodes[x].firstChild.data
                                elif  (mytag == "d:BC_3YEAR"):
                                    y3 = elem.childNodes[13].childNodes[1].childNodes[x].firstChild.data
                                elif  (mytag == "d:BC_5YEAR"):
                                    y5 = elem.childNodes[13].childNodes[1].childNodes[x].firstChild.data
                                elif  (mytag == "d:BC_7YEAR"):
                                    y7 = elem.childNodes[13].childNodes[1].childNodes[x].firstChild.data
                                elif  (mytag == "d:BC_10YEAR"):
                                    y10 = elem.childNodes[13].childNodes[1].childNodes[x].firstChild.data
                                elif  (mytag == "d:BC_20YEAR"):
                                    y20 = elem.childNodes[13].childNodes[1].childNodes[x].firstChild.data
                                elif  (mytag == "d:BC_30YEAR"):
                                    y30 = elem.childNodes[13].childNodes[1].childNodes[x].firstChild.data

                sql = "INSERT INTO TSY_HISTORICALS(URL,1MO,2MO,3MO,6MO,1Y,2Y,3Y,5Y,7Y,10Y,20Y,30Y)  "
                sql += "VALUES(" + chr(39) + tsyGovLink + chr(39) #+# "," + y1 
                sql += "," + str(m1)
                sql += "," + str(m2)
                sql += "," + str(m3)
                sql += "," + str(m6)
                sql += "," + str(y1)
                sql += "," + str(y2)
                sql += "," + str(y3)
                sql += "," + str(y5)
                sql += "," + str(y7)
                sql += "," + str(y10)
                sql += "," + str(y20)
                sql += "," + str(y30)
                sql += ")"
                #print(sql)
                mycursor.execute(sql)
                mydb.commit()


if __name__ == '__main__':
    myObj = Treasury()
    myObj.getTreasuryXML()
    myObj.parseXML()