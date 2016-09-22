from django.shortcuts import render

# Create your views here.
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.http.response import HttpResponse
from .forms import NetworkForm, AwsForm, NtpForm, ListBucketsForm, S3qlForm
from accessAWS import s3bucket
from s3ql_file import s3ql_access,S3QLActions

import os
import re
import json
import time
import random
import subprocess
import socket

def login_user(request):
    url = request.build_absolute_uri() 
    state = socket.gethostname()
    username = ""
    password = ""
   
    if request.POST:
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username = username,password = password)
        if user is not None:
            if user.is_active:
                login(request,user)
                #state = "You're successfully logged in"
                return HttpResponseRedirect('/home/')
            else:
                state = "Your account is not active"
        else:
            state = "Your username and/or passwors were incorrect"
   
    context = RequestContext(request)
    return render_to_response("auth.html",{'state':state,'username':username,"url":url},context_instance=context)

@login_required(login_url="/login/")
def home(request):
    interfaces = r"/etc/network/interfaces"
    Links = ""
    e = ""
    buckets = None
    if request.method == "POST" and "form1" in request.POST:
        form1 = NetworkForm(request.POST,prefix='form1')
        #form2 = AwsForm(request.POST,prefix="form2")
        
        if form1.is_valid():
            Links = "form1"
            address = request.POST.get("form1-address")
            netmask = request.POST.get("form1-netmask")
            gateway = request.POST.get("form1-gateway")
            dns_search = request.POST.get("form1-dns_search")
            dns_name = request.POST.get("form1-dns_nameservers")

            mode = request.POST.get("form1-mode")
            
            lines = ""
            with open(interfaces,"r") as f:
                for line in f:
                    lines += line
            devices = lines.split("iface")
            interfaces = ""
            iface_prefix = 'iface eth0 inet'

            for i,device in enumerate(devices):
                if i > 0:
                    device = "iface" + device
                    if iface_prefix in device:
                        iface_entry = iface_prefix + mode
                        if mode == "static":
                            device = re.sub("address" + r'.*', "address" + " " + address, device)
                            device = re.sub("netmask" + r'.*', "netmask" + " " + netmask, device)
                            device = re.sub("gateway" + r'.*', "gateway" + " " + gateway, device)
                            device = re.sub("dns-search" + r'.*', "dns-search" + " " + dns_search, device)
                            device = re.sub("dns-nameservers" + r'.*', "dns-nameservers" + " " + dns_name, device)
                        else:
                            device = iface_entry
                interfaces += device
            with open("interfaces","w") as f:
                f.write(interfaces)
            command = "cp interfaces /etc/network/"
            subprocess.check_call(command, shell=True)
            string=address+" "+netmask+" "+gateway+" "+dns_search+" "+dns_name+" "+mode
            Links = string
       
            #os.system("sudo cp interfaces-test /etc/network/")
            #os.system("sudo service network restart")
    else:
        form1 = NetworkForm(prefix="form1")
    if request.method == "POST" and "form2" in request.POST:
        form2 = AwsForm(request.POST,prefix='form2')
        #form2 = AwsForm(request.POST,prefix="form2")
        
        if form2.is_valid():
            #Links = "form2"
            aws_id = request.POST.get("form2-aws_id")
            aws_key = request.POST.get("form2-aws_key")
            bucket = request.POST.get("form2-bucket_name")

            #Links = aws_id + aws_key + bucket
            try:
                object_bucket = s3bucket(aws_id,aws_key)
                object_bucket.Create(bucket)
            except Exception as e:
                e = e
    else:
        form2 = AwsForm(prefix="form2")
    if request.method == "POST" and "form3" in request.POST:
        form3 = NtpForm(request.POST,prefix="form3")
        if form3.is_valid():
            Links = "form3" 
            ip1 = request.POST.get("form3-ip1")
            ip2 = request.POST.get("form3-ip2")
            Links = ip1 + " " + ip2
 
            ntp_file = r"/etc/ntp.conf"
            Content = ""
            with open(ntp_file,"r") as f:
                for line in f:
                    Content += line
            with open("ntp-test.conf","w") as f:
                for line in Content:
                    f.write(line)
                f.write(ip1+"\n")
                f.write(ip2+"\n")
            command1 = "cp ntp-test.conf /etc/"
            subprocess.check_call(command1, shell=True)
            command2 = "sudo service ntp reload"
            subprocess.check_call(command2, shell=True)

    else:
        form3 = NtpForm(prefix="form3")
    if request.method == "POST" and "form4" in request.POST:
        form4 = ListBucketsForm(request.POST,prefix="form4")
        if form4.is_valid():
            #Links = "form4"
            aws_id = request.POST.get("form4-aws_id")
            aws_key = request.POST.get("form4-aws_key")
            #Links = aws_id + " " + aws_key
            
            object_aws = s3bucket(aws_id,aws_key)
            buckets = [str(bucket).replace("<Bucket: ","").replace(">","") for bucket in object_aws.GetBuckets()]
    else:
        form4 = ListBucketsForm(prefix="form4")
    if request.method == "POST" and "form5" in request.POST:
        form5 = S3qlForm(request.POST,prefix='form5')
        #form2 = AwsForm(request.POST,prefix="form2")

        if form5.is_valid():
            #Links = "form5"
            aws_id = request.POST.get("form5-aws_id")
            aws_key = request.POST.get("form5-aws_key")
            bucket_name = request.POST.get("form5-bucket_name")
            passphrase = request.POST.get("form5-passphrase")
            #Links = aws_id+" "+aws_key+" "+bucket_name+" "+passphrase
            s3_object = s3ql_access(aws_id,aws_key,bucket_name,passphrase)
            s3_object.CheckFile()
            mkfs = r"sudo mkfs.s3ql s3://" + str(bucket_name) + "/test"
            mkfs = mkfs.split()
            mount = r"mount.s3ql --allow-other --cachesize 10240000 --compress lzma s3://" + str(bucket_name) + "/test /mnt/s3ql/"
            mount = mount.split()
            password = "mestre"

            object_mkfs = S3QLActions(mkfs,passphrase)
            object_mkfs.any_commands()
            object_mkfs.any_commands()
            object_mount = S3QLActions(mount,password)
            object_mount.any_commands()
            

    else:
        form5 = S3qlForm(prefix="form5")
    return render(request,'home.html',{'Links':Links,'Error':e,
                                       "Form1":form1,"Form2":form2,
                                       "Form3":form3,"Form4":form4,
                                       "Form5":form5,"buckets":buckets})
