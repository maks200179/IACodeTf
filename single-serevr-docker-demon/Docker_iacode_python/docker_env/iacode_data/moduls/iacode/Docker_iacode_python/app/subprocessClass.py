from subprocess import (Popen, PIPE)
from loggingGlobal import loggingGlobal

class subprocessClass():
    def __init__(self):
        super(subprocessClass, self).__init__()
        self.logging = loggingGlobal()

    def cmdCommunicateOS(self, command):
        p = Popen(shlex.split(command), stdin=PIPE, stdout=PIPE, stderr=PIPE)
        (stdout, stderr) = p.communicate()
        if p.returncode != 0 or stderr.decode('utf-8') != '':
            self.logging.writeLogWarning(("""'The command %s exited with error code  %s and error messege is %s '""") %(command,p.returncode,(stderr.decode('utf-8'))))
        return stdout.decode('utf-8')