import logging

class loggingGlobal():
    def __init__(self):
        super(loggingGlobal,self).__init__()

        self.logging = logging
        self.logging.basicConfig(filename='IaC.log', level=logging.DEBUG)

    def writeLogWarning(self,messege):
        self.logging.warning(messege)


    def writeLogCritical(self,messege):
        self.logging.critical(messege)