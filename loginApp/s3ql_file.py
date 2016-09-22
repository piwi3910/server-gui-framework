import os, re, subprocess

class s3ql_access:
    def __init__(self,aws_id,aws_secret,bucket,phrase):
        self.aws_id = aws_id
        self.aws_secret = aws_secret
        self.bucket = bucket
        self.phrase = phrase
        self.filename = r"/home/david/.s3ql/authinfo2"
        self.content = ""
    def FindFileSystem(self,text):
        regex = "fs(.+?)]\nstorage"
        pattern = re.compile(regex)
        find = re.findall(pattern,text)
        if find:
            return find[-1]
    def CheckIfExists(self):
        return os.path.isfile(self.filename) 
    def CreateFile(self,count):
        with open(self.filename,"a") as f:
            f.write("[fs" + str(count) + "]"+"\n")
            f.write("storage-url: s3://" + str(self.bucket) + "\n")
            f.write("backend-login:" + str(self.aws_id) + "\n")
            f.write("backend-password:" + str(self.aws_secret) + "\n")
            f.write("fs-passphrase:" + str(self.phrase) + "\n\n")
    def CheckFile(self):
        count = 1
        if not self.CheckIfExists():
            try:
                os.makedirs(os.path.dirname(self.filename))
            except Exception as e:
                pass
            self.CreateFile(count)
        else:
            with open(self.filename,"r") as f:
                for line in f:
                    self.content += line
            
            count = int(self.FindFileSystem(self.content)) + 1
            self.CreateFile(count)
            
class S3QLActions:
    def __init__(self,cmd1,cmd2):
        self.cmd1=cmd1
        self.cmd2=cmd2
    def console(self):
        return subprocess.Popen(["sudo","-S"] + self.cmd1, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    def any_commands(self):
        return self.console().communicate(self.cmd2)
