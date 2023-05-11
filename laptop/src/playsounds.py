from playsound import playsound
import threading

class sound_thread(): 
    def __init__(self):
        self.running=False

    def start(self,soundfile,seconds):
        playsound(soundfile,block=False)
        self.running=True
        
        def sctn():  
           self.running=False 
        S = threading.Timer(seconds, sctn)  
        S.start()         
    # soundthread.start()
