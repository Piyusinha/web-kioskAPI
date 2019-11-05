from flask import Flask
import urllib
import requests
from bs4 import BeautifulSoup
import sys
from flask import jsonify

app =Flask(__name__)

@app.route('/<string:enrollment>/<string:dob>/<string:pa>')
def webkiosk(enrollment,dob,pa):
    resp = urllib.request.urlopen("https://webkiosk.jiit.ac.in/index.jsp")
    soup = BeautifulSoup(resp,'html.parser')
    captcha=soup.find_all('i')[0].text
    header = resp.info()
    header = header.items()[2][1]
    header, sep, tail = header.partition(';')
    head, sep, jSesId = header.partition('=')

    cookies='JSESSIONID='+jSesId+';switchmenu='
    timeout=10
    headers = {
	'Host': 'webkiosk.jiit.ac.in',
	'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0',
	'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,/;q=0.8',
	'Accept-Language': 'en-US,en;q=0.5',
	'Accept-Encoding': 'gzip, deflate, br',
	'Content-Type': 'application/x-www-form-urlencoded',
	'Cookie':cookies,
	'DNT': '1',
	'Connection': 'keep-alive',
	'Upgrade-Insecure-Requests': '1',
    'Content-length':'248',
    'Referer': 'https://webkiosk.jiit.ac.in/'

    }
    payload = {
   "x":"",
   "txtInst":"Institute",
   "InstCode":"JIIT",
   "txtuType":"Member+Type",
   "UserType101117":"S",
   "txtCode":["Enrollment+No","Enter+Captcha+++++"],"MemberCode":enrollment,
   "DOB":"DOB",
   "DATE1":dob,
   "txtPin":"Password/Pin",
   "Password101117":pa,
   "txtcap":captcha,
   "BTNSubmit":"Submit"
     }
    s=requests.session()
    resp = s.post('https://webkiosk.jiit.ac.in/CommonFiles/UseValid.jsp', data=payload,headers=headers,timeout=timeout)


    resp=requests.get('https://webkiosk.jiit.ac.in/StudentFiles/Academic/ViewDatewiseLecAttendance.jsp?EXAM=2019ODDSEM&CTYPE=R&SC=160037&LTP=LT&mRegConfirmDate=16-07-2019&mRegConfirmDateOrg=16-07-2019&prevTFSTID=&prevLFSTID=&mLFSTID=JIIT1902468&mTFSTID=JIIT1902490',headers=headers)
    soup = BeautifulSoup(resp.text,"html5lib")

    table=soup.find('table',id='table-1')

    trows=table.find_all('tr')
    a=[]
    for tr in trows:
        td=tr.find_all('td')
        row=[i.text for i in td]
        a.append(row)
    return jsonify(a)


app.run(port=5000)
