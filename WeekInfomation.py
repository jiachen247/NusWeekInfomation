import requests
from Secret import USERID, PASSWORD
from bs4 import BeautifulSoup

# fix: https://stackoverflow.com/questions/41246976/getting-chunkedencodingerror-connection-broken-incompleteread
from requests_toolbelt.adapters import appengine
appengine.monkeypatch()

LOGIN_URL = "https://ivle.nus.edu.sg/default.aspx"
WORKSPACE_URL = "https://ivle.nus.edu.sg/v1/workspace.aspx"


class WeekInfomation:
    def get(self):
        print("[+] getting week infomation...")
        s = requests.Session()

        viewStateCookie = self.getViewStateCookie(s)
        self.getIvleToken(s, viewStateCookie)
        week = self.getWeekDetails(s)
        print(week)
        return week

    def getViewStateCookie(self, s):
        r = s.get(LOGIN_URL)
        return self.parseViewState(r.text)

    def parseViewState(self, text):
        bs = BeautifulSoup(text, "lxml")
        return bs.find("input", {"id": "__VIEWSTATE"}).attrs['value']

    def getIvleToken(self, s, viewState):
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        s.post(LOGIN_URL, headers=headers,
               data={
                   "__EVENTTARGET": "ctl00$ctl00$ContentPlaceHolder1$btnSignIn",
                   "__VIEWSTATE": viewState,
                   "ctl00$ctl00$ContentPlaceHolder1$userid": USERID,
                   "ctl00$ctl00$ContentPlaceHolder1$password": PASSWORD
               })

    def getWeekDetails(self, s):
        r = s.get(WORKSPACE_URL)
        bs = BeautifulSoup(r.text, "lxml")
        week = bs.find("a", {"id": "ctl00_ctl00_ContentPlaceHolder1_lblAcadTxt"})
        print("[+] ! " + week.text)

        return week.text
