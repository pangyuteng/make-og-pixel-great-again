import sys
import time
import datetime
import warnings
import traceback
import pandas as pd
import json
with open("secret.json",'r') as f:
	secret = json.loads(f.read())
email,password,backup_email = secret["email"],secret["password"],secret["backupemail"]

import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from pathlib import Path

message = f"Get your phone ready to confirm login (via google 2 step verification, gotta have this enabled)! Careful to not mess this up or your account may get locked for a while!!!"

wait = 20
while wait > 0:
    print(message)
    print(f"t-minus {wait} seconds..")
    wait-=1
    time.sleep(1)

driver = uc.Chrome()
driver.get('https://accounts.google.com/')

# add email
time.sleep(2)
driver.find_element(By.XPATH, '//*[@id="identifierId"]').send_keys(email)
driver.find_element(By.XPATH, '//*[@id="identifierNext"]/div/button/span').click()
time.sleep(2)
driver.find_element(By.XPATH, '//*[@id="password"]/div[1]/div/div[1]/input').send_keys(password)
time.sleep(2)
driver.find_element(By.XPATH, '//*[@id="passwordNext"]/div/button/span').click()
time.sleep(10)
driver.get('https://photos.google.com')
time.sleep(2)

df = pd.read_csv('all.csv')
df['tstamp']=df.creationTime.apply(
    lambda x: datetime.datetime.strptime(x,'%Y-%m-%dT%H:%M:%SZ')
)
print(df.shape)

outfile = "space2.csv"
appnd = Path(outfile).is_file()

if appnd:
    rd = pd.read_csv(outfile)
    res = datetime.datetime.strptime(rd.iloc[-1].creationTime,'%Y-%m-%dT%H:%M:%SZ')
else:
    res = datetime.datetime.now()

df = df[df.tstamp<res].reset_index()
print(df.shape)

#mylist = []
firstrow = True
for n,row in df.iterrows():
	try:
		driver.get(row.productUrl)
		driver.implicitly_wait(2)
		time.sleep(2)
		if "Backed up" not in driver.page_source:
			print('click')
			driver.find_element(By.XPATH,'.//*[@aria-label="Open info"]').click()
			driver.implicitly_wait(2)
			time.sleep(2)
		mytext = "This item doesn't take up space in your account storage."
		if mytext in driver.page_source:
			pass
		else:
			mytext = "This item takes up space."
		print(mytext)
		mylist = []
		headr = not(appnd) and firstrow
		myitem = dict(row)
		myitem['observation']=mytext
		mylist.append(myitem)
		newdf = pd.DataFrame([mylist[-1]])
		newdf.to_csv(outfile,index=False,header=headr,mode='a')
		firstrow = False
	except:
		traceback.print_exc()
		time.sleep(2)
driver.quit()
