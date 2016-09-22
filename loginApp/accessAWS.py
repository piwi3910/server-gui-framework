import boto
from boto.s3.connection import S3Connection
from boto.s3.key import Key

class s3bucket:
    def __init__(self,key,secret):
        self.ACCESS_KEY = key  
        self.SECRET_KEY = secret
        self.conn = S3Connection(self.ACCESS_KEY,self.SECRET_KEY)
    def Create(self,name):
        self.conn.create_bucket(name)
    def GetBuckets(self):
        return [bucket for bucket in self.conn.get_all_buckets()]
