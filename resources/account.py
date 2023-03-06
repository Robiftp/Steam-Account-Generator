from solver import Solver
from bs4 import BeautifulSoup
import time, requests, secrets, imaplib, email, time, random
from utils.logger import Logger


class Account():
    def __init__(self, proxy, mail, password):
        self.proxy = proxy
        self.accountmail = mail
        self.accountpassword = password
        self.session = requests.Session()
        self.session.proxies = {'http': proxy, 'https': proxy}
        self.sessionid = None
        self.imap = imaplib.IMAP4_SSL("outlook.office365.com")

    def register_account(self):
        r = self.session.get('https://store.steampowered.com/join/refreshcaptcha')
        start = time.time()
        captcha_key = Solver(r.json()['s']).solve_captcha()
        took = int(time.time() - start) * 1000
        
        Logger(f'Solved Captcha', f'({took}ms) {captcha_key[:50]}...').log_success()

        data = {
            'email': self.accountmail,
            'captchagid' : r.json()['gid'],
            'captcha_text' : captcha_key,
            'elang' : 0
        }
        r = self.session.post('https://store.steampowered.com/join/ajaxverifyemail', data=data)
        if r.json().get('sessionid') is None or r.json().get('sessionid') == '':
            return self.register_account()
        return r.json().get('sessionid')

    def create_account(self):
            self.sessionid = self.register_account()
            Logger('Session ID', f'{self.sessionid}').log_default()
            self.imap.login(self.accountmail, self.accountpassword)
            while not self.verify_email():
                time.sleep(0.5)
            username, password = f"AfricanGen{secrets.token_hex(6)}", secrets.token_hex(12)
            data = {
                "accountname": username,
                "password": password,
                "count": 0,
                "lt": 0,
                "creation_sessionid": self.sessionid,
                "embedded_appid": 0,
            }
            r = self.session.post('https://store.steampowered.com/join/createaccount', data=data, headers={'Content-Type': 'application/x-www-form-urlencoded'})
            return username, password
            # return self.sessionid, r.cookies

    def verify_email(self):
        try:
            self.imap.select("inbox")
            status, messages = self.imap.search(
                None, 'UNSEEN', 'SUBJECT "New Steam Account Email Verification"')
            if status == "OK":
                messages = messages[0].split()

            emails = []
            for message in messages:
                status, data = self.imap.fetch(message, "(RFC822)")
                if status == "OK":
                    emails.append(email.message_from_bytes(data[0][1]))

            emails.sort(key=lambda x: x["Date"], reverse=True)

            for part in emails[0].walk():
                if part.get_content_type() == "text/html":
                    html = part.get_payload(decode=True)
                    link = BeautifulSoup(html, "html.parser").find("a", class_="link c-grey4")
                    if not link: return False
                    self.session.get(link["href"]).raise_for_status()
                    Logger("Verified account", f"{self.accountmail}:{self.accountpassword}").log_success()
                    return True
            return False
        except IndexError:
            pass
        except Exception as e:
            Logger('Failed to verify email', e).log_error()