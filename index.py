import csv
import requests
#import xml.etree.ElementTree as ET
from xml.dom import minidom # https://docs.python.org/3/library/xml.dom.minidom.html

#########################################################
# XML source: https://www.treasury.gov/resource-center/data-chart-center/interest-rates/pages/textview.aspx?data=yield
#########################################################
class Treasury:        
    def __init__(self):
        super().__init__()

    def getTreasuryXML(self):
  
        # url of rss feed
       # url = 'https://data.treasury.gov/feed.svc/DailyTreasuryYieldCurveRateData' # all-time, rates SI
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
        tsyGovLink = ""
        mydoc = minidom.parse('treasury.xml')
        items = mydoc.getElementsByTagName('entry')

        for elem in items:            
            if (elem.childNodes[1].tagName == "id"):
                tsyGovLink = elem.childNodes[1].firstChild.data
            if (elem.childNodes[13].tagName == "content"):
                for x in range(1,elem.childNodes[13].childNodes[1].childNodes.length):
                    if (elem.childNodes[13].childNodes[1].childNodes[x].nodeType == elem.ELEMENT_NODE):
                       # print(str(x) + ' ' + elem.childNodes[13].childNodes[1].childNodes[x].tagName)
                        if (elem.childNodes[13].childNodes[1].childNodes[x].tagName == "d:NEW_DATE"):
                            print('date: ' + str(elem.childNodes[13].childNodes[1].childNodes[x].firstChild.data))
                        elif (elem.childNodes[13].childNodes[1].childNodes[x].tagName == "d:BC_1MONTH"):
                            print('  1 mo: ' + str(elem.childNodes[13].childNodes[1].childNodes[x].firstChild.data))
                        elif (elem.childNodes[13].childNodes[1].childNodes[x].tagName == "d:BC_2MONTH"):
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




if __name__ == '__main__':
    myObj = Treasury()
    myObj.getTreasuryXML()
    myObj.parseXML()