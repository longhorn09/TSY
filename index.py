import csv
import requests
import xml.etree.ElementTree as ET

#########################################################
# https://www.treasury.gov/resource-center/data-chart-center/interest-rates/pages/textview.aspx?data=yield
#########################################################
def getTreasury():
  
    # url of rss feed
    url = 'https://data.treasury.gov/feed.svc/DailyTreasuryYieldCurveRateData?$filter=month(NEW_DATE)%20eq%204%20and%20year(NEW_DATE)%20eq%202021'
  
    # creating HTTP response object from given url
    resp = requests.get(url)
  
    # saving the xml file
    #with open('topnewsfeed.xml', 'wb') as f:
    #    f.write(resp.content)


if __name__ == '__main__':
    print("ok")