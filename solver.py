import requests, json



class Solver():
    def __init__(self, data_s) -> None:
        self.data_s = data_s
        try:
            with open('config.json', 'r') as f:
                self.api_key = json.loads(f.read())['capmonster']
        except Exception as e:
            self.api_key = 'wtf'

    def ob_task_id(self):
        json = {
            "clientKey": self.api_key,
            "task":
            {
                "type":"RecaptchaV2EnterpriseTask",
                "websiteURL":"https://store.steampowered.com/join",
                "websiteKey":"6LdIFr0ZAAAAAO3vz0O0OQrtAefzdJcWQM2TMYQH",
                "proxyType":"http",
                "proxyAddress":"p.webshare.io",
                "proxyPort":9999,
                "userAgent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.132 Safari/537.36",
                "apiDomain": "www.recaptcha.net",
                "enterprisePayload": {
                    "s": self.data_s
                },
            }
        }
        return requests.post('https://api.capmonster.cloud/createTask', json=json).json()
    
    def solve_captcha(self): 
        task = self.ob_task_id().get("taskId")
        while True:
            captchaData = requests.post(f"https://api.capmonster.cloud/getTaskResult", json={"clientKey": self.api_key, "taskId": task}, timeout=30).json()
            if "processing" in captchaData:
                pass
            else:
                try:
                    return captchaData.get("solution").get("gRecaptchaResponse")
                except Exception:
                    # print("Failed.")
                    continue