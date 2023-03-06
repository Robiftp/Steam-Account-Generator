import sys, colr

class Logger():
    def __init__(self, text, resp):
        self.text = text
        self.resp = resp
        
    def log_default(self):
        sys.stdout.write(colr.color(f"[*] {self.text} -> {self.resp}\n",fore='yellow', style='bright'))
        sys.stdout.flush()
        
    def log_success(self):
        sys.stdout.write(colr.color(f"[$] {self.text} -> {self.resp}\n",fore='green', style='bright'))
        sys.stdout.flush()
        
    def log_error(self):
        sys.stdout.write(colr.color(f"[!] {self.text} -> {self.resp}\n",fore='red', style='bright'))
        sys.stdout.flush()