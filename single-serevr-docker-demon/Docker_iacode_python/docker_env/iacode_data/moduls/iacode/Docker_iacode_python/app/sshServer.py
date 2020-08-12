import paramiko


class sshCommand():


    def ssh_connect(self,hostname,username,keyfile,command):
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            self.ssh.connect(hostname,username=username,key_filename=keyfile,timeout=5)
            stdin, stdout, stderr = self.ssh.exec_command(command)
        except Exception as err:
            return ('get error "%s" user %s ' % (err, client_name))

        stdoutstr =  '%s %s' %((stdout.read().decode('utf-8').strip("\n")),((stderr.read().decode('utf-8').strip("\n"))))
        self.ssh.close()

        return  stdoutstr