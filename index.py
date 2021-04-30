import csv
import requests
import xml.etree.ElementTree as ET

#########################################################
# XML source: https://www.treasury.gov/resource-center/data-chart-center/interest-rates/pages/textview.aspx?data=yield
# help reference: https://www.geeksforgeeks.org/xml-parsing-python/
#########################################################
class Treasury:        
    def __init__(self):
        super().__init__()

    def getTreasuryXML(self):
  
        # url of rss feed
        url = 'https://data.treasury.gov/feed.svc/DailyTreasuryYieldCurveRateData?$filter=month(NEW_DATE)%20eq%204%20and%20year(NEW_DATE)%20eq%202021'
  
        # creating HTTP response object from given url
        resp = requests.get(url)
  
        # saving the xml file
        with open('treasury.xml', 'wb') as f:
            f.write(resp.content)

    def parseXML(self):
        tree = ET.parse('treasury.xml')
        root = tree.getroot()
        #for item in root.findall('./entry'):


if __name__ == '__main__':
    myObj = Treasury()
    myObj.getTreasuryXML()
