import DbcAPI.deathbycaptcha as dbc
class DBC():
    def __init__(self):
        self.user = 'lepidoptera'
        self.passwd = 'spdhdnlwm1260'
        
    def resolveFile(self, filepath):
        
        # Put your DBC account username and password here.
        # Use deathbycaptcha.HttpClient for HTTP API.
        client = dbc.HttpClient(self.user, self.passwd)
        try:
            balance = client.get_balance()
    
            # Put your CAPTCHA file name or file-like object, and optional
            # solving timeout (in seconds) here:
            captcha = client.decode(filepath, 20)
            if captcha:
                # The CAPTCHA was solved; captcha["captcha"] item holds its
                # numeric ID, and captcha["text"] item its text.
                print(("CAPTCHA %s solved: %s" % (captcha["captcha"], captcha["text"])))
                return captcha["text"]
                
        except dbc.AccessDeniedException:
            raise  AccessDeniedException("to DBC API denied, check your credentials and/or balance")
        
        
