import imaplib2, time
from threading import *
 

class EmailChecker(object):
    def __init__(self, conn):
        self.thread = Thread(target=self.idle)
        self.M = conn
        self.event = Event()
 
    def start(self):
        self.thread.start()
 
    def stop(self):
       
        self.event.set()
 
    def join(self):
        self.thread.join()
 
    def idle(self):

        while True:
           
            if self.event.isSet():
                return
            self.needsync = False
           
           #Class called after receiving event
            def callback(args):
                if not self.event.isSet():
                    self.needsync = True
                    self.event.set()
            
            self.M.idle(callback=callback)
           
            self.event.wait()
            
            if self.needsync:
                self.event.clear()
                self.dosync()
 
   
    def dosync(self):
        #Call a event from here 
        print("Got an event!")
 

try:
    #Authentication for Mail
    M = imaplib2.IMAP4_SSL("imap.gmail.com")
    M.login("UserName","Password")
   
    # Select Mail folder from where event should manage i.e inbox,sent 
    M.select("INBOX")

    emailChecker = EmailChecker(M)
    emailChecker.start()

    # Stop checking Mail after sometime
    time.sleep(120*60)
finally:
    emailChecker.stop()
    emailChecker.join()
    M.close()
    M.logout()

