import threading

class Thread(threading.Thread):
    def __init__(self, threadID, threadName, defrun):
        threading.Thread.__init__(self)
        self.ID = threadID
        self.name = threadName
        self.defToRun = defrun
    
    def run(self):
        print (self.name, "started")
        self.defToRun()



