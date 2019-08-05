from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import pandas as pd
browser=webdriver.Chrome()
browser.maximize_window()
browser.get('https://doris.delhigovt.nic.in/login.aspx')
button=browser.find_element_by_link_text('Complete Search (Without Reg. Year)')
button.click()
time.sleep(60)
def get_data(source,main_df):
    soup=BeautifulSoup(source,'lxml')
    tables=soup.find_all('table',{'id':'ctl00_ContentPlaceHolder1_gv_search'})
    rows=tables[0].find_all('tr',{'align':'left'})
    regno=[]
    regdate=[]
    party_1=[]
    party_2=[]
    address=[]
    area=[]
    deed_type=[]
    property_type=[]
    for row in rows:
        array=row.text.split('\n')
        regno.append(array[2])
        regdate.append(array[4])
        party_1.append(array[9])
        party_2.append(array[40])
        if array[68]!='':
            address.append(array[68])
            area.append(array[70])
            deed_type.append(array[72])
            property_type.append(array[74])
        else:
            address.append(array[76])
            area.append(array[78])
            deed_type.append(array[80])
            property_type.append(array[82])
    
    df=pd.DataFrame({'regno':regno,'regdate':regdate,'party_1':party_1,'party_2':party_2,'address':address,'area':area,'deed_type':deed_type,'property_type':property_type})
    if main_df.empty:
        main_df=df
    else:
        main_df=pd.concat([main_df,df])
    return main_df
try:
    main_df=pd.DataFrame()
    count=0
    for j in range(1,int(BeautifulSoup(browser.page_source,'lxml').find_all('span',{'id':'ctl00_ContentPlaceHolder1_gv_search_ctl13_lblTotalNumberOfPages'})[0].text)+1):
        time.sleep(2)
        count+=1
        main_df=get_data(browser.page_source,main_df)
        bttn=browser.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_gv_search_ctl13_txtGoToPage"]')
        for i in range(3):    
            bttn.send_keys(Keys.BACKSPACE)
        bttn.send_keys(j)
        bttn.submit()
except:
    print(count,' pages were scraped from DORIS')
print(main_df.head())
print(main_df.tail())
print('shape',main_df.shape)
import datetime as dt
name=f'{dt.datetime.now().year}-{dt.datetime.now().month}-{dt.datetime.now().day}-DORIS.csv'
main_df.to_csv(name)