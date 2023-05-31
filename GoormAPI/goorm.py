# -*- coding: utf-8 -*-



from requests import Session
from random import choice
from enum import Enum, auto



class GoormType(Enum):
    def __repr__(self):
        return f"GoormType.{self}"



class GoormResponse(GoormType):
    EmptyEmail = auto()
    EmptyPassword = auto()
    InvalidEmail = auto()
    InvalidPassword = auto()
    InvalidResponse = auto()
    Success = auto()



class AUTHENTICATION:
    def __init__(self, email, password):
        self.EMAIL = email
        self.PASSWORD = password



class GoormIDE:
    def __init__(self, email, password):
        self.session = Session()
        self.useragent = self.__useragent__()
        self.AUTHENTICATION = AUTHENTICATION(email, password)

    def __useragent__(self):
        return (choice([
            "Mozilla/5.0 (Linux; Android 12; M2101K6G) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 9; 5024A) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 11; SM-A202F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.0.0 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 12; CPH2211 Build/SP1A.210812.016; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/104.0.5112.110 Mobile Safari/537.36 [FB_IAB/FB4A;FBAV;]",
            "Mozilla/5.0 (Linux; Android 11; SM-A217F Build/RP1A.200720.012; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/98.0.4758.101 Mobile Safari/537.36 [FB_IAB/FB4A;FBAV;]",
            "Mozilla/5.0 (Linux; Android 7.0; AGS-W09) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.152 Safari/537.36"
        ]))

    def Login(self):
        try:
            res = self.session.post(
                url="https://accounts.goorm.io/api/login",
                headers={
                          "Host": "accounts.goorm.io",
                          "User-Agent": self.useragent,
                          "Accept": "application/json, text/plain, */*",
                          "Accept-Language": "en-US,en;q=0.5",
                          "Content-Type": "application/json;charset=utf-8",
                          "Origin": "https://accounts.goorm.io",
                          "Connection": "keep-alive",
                          "Referer": "https://accounts.goorm.io/login",
                          "Sec-Fetch-Dest": "empty",
                          "Sec-Fetch-Mode": "cors",
                          "Sec-Fetch-Site": "same-origin"
                },
                json={
                       "email": self.AUTHENTICATION.EMAIL,
                       "pw": self.AUTHENTICATION.PASSWORD,
                       "return_url": "https://ide.goorm.io/my/dashboard?redirect=1",
                       "signupLanguage": "en-US",
                       "keepLogin": True
                }
            )
            if (res.status_code) == 200:
                res = res.json()
                if (res["result"]) == True:
                    return GoormResponse.Success
                elif (res["result"]) == False:
                    if (res["code"]) == 1:
                        return GoormResponse.EmptyEmail
                    elif (res["code"]) == 2:
                        return GoormResponse.EmptyPassword
                    elif (res["code"]) == 5:
                        return GoormResponse.InvalidEmail
                    elif (res["code"]) == 8:
                        return GoormResponse.InvalidPassword
        except Exception:
            pass
        return GoormResponse.InvalidResponse

    def GetContainerList(self):
        try:
            res = self.session.get(
                url="https://ide.goorm.io/api/users/my/containers/all",
                headers={
                          "Host": "ide.goorm.io",
                          "User-Agent": self.useragent,
                          "Accept": "application/json, text/plain, */*",
                          "Accept-Language": "en-US,en;q=0.5",
                          "X-Requested-With": "XMLHttpRequest",
                          "Connection": "keep-alive",
                          "Referer": "https://ide.goorm.io/my/dashboard",
                          "Sec-Fetch-Dest": "empty",
                          "Sec-Fetch-Mode": "cors",
                          "Sec-Fetch-Site": "same-origin"
                }
            )
            if (res.status_code) == 200:
                res = res.json()
                return [{"ProjectName":(i["name"]), "ProjectUID":(i["uid"]), "Status":(eval(((i["status"]).replace("on","True").replace("off", "False"))))} for i in res]
        except Exception:
            pass
        return GoormResponse.InvalidResponse

    def RunContainer(self, container_uid):
        try:
            res = self.session.post(
                url="https://ide-run.goorm.io/container/run",
                headers={
                          "Host": "ide-run.goorm.io",
                          "User-Agent": self.useragent,
                          "Accept": "*/*",
                          "Accept-Language": "en-US,en;q=0.5",
                          "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                          "X-Requested-With": "XMLHttpRequest",
                          "Origin": "https://ide-run.goorm.io",
                          "Connection": "keep-alive",
                          "Referer": f"https://ide-run.goorm.io/workspace/{container_uid}",
                          "Sec-Fetch-Dest": "empty",
                          "Sec-Fetch-Mode": "cors",
                          "Sec-Fetch-Site": "same-origin"
                },
                data={
                    "docker_id": container_uid,
                    "project_path": container_uid
                }
            )
            if (res.status_code) == 200:
                res = res.json()
                if res == True or (res["running"]) == True:
                    return GoormResponse.Success
        except Exception:
            pass
        return GoormResponse.InvalidResponse

