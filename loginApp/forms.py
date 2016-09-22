from django import forms

CHOICES = (
    ("static",("static")),
    ("dhcp",("dhcp"))
)

class NetworkForm(forms.Form):
    address = forms.CharField(label="address",max_length=100,required=False,
                              widget=forms.TextInput(attrs={"class":"choices"}))
    netmask = forms.CharField(label="netmask",max_length=100,required=False)
    gateway = forms.CharField(label="gateway",max_length=100,required=False)
    dns_search = forms.CharField(label="dns-search",max_length=100,required=False)
    dns_nameservers = forms.CharField(label="dns-nameservers",max_length=100,required=False)

    mode = forms.ChoiceField(
        label="Mode", choices=CHOICES, required=False,
        widget=forms.Select(attrs={'class': 'mode'})
    )

    def clean(self):
        mode = self.cleaned_data.get('mode')
        if mode != 'dhcp':
            address = self.cleaned_data.get('address')
            netmask = self.cleaned_data.get('netmask')
            gateway = self.cleaned_data.get('gateway')
            dns_search = self.cleaned_data.get('dns_search')
            dns_nameservers = self.cleaned_data.get('dns_nameservers')
            if not address:
                raise forms.ValidationError({'address': 'address field is required.'})
            elif not netmask:
                raise forms.ValidationError({'netmask': 'netmask field is required.'})
            elif not gateway:
                raise forms.ValidationError({'gateway': 'gateway field is required.'})
            elif not dns_search and not dns_nameservers:
                raise forms.ValidationError({'address': 'You need to fill at least one dns server field.'})

class AwsForm(forms.Form):
    aws_id = forms.CharField(label="aws-id",max_length=200)
    aws_key = forms.CharField(label="aws-key",max_length=200)
    bucket_name = forms.CharField(label="bucket_name",max_length=200)
    
class NtpForm(forms.Form):
    NTP = forms.BooleanField(required=False,initial=True)
    ip1 = forms.CharField(label="ip1",max_length=100)
    ip2 = forms.CharField(label="ip2",max_length=100)
    def __init__(self,*args,**kwargs):
        super(NtpForm,self).__init__(*args,**kwargs)
        self.fields["ip1"].widget.attrs["style"] = "display:none"
        self.fields["ip2"].widget.attrs["style"] = "display:none"
        self.fields["ip1"].widget.attrs["class"] = "user_choice"
        self.fields["ip2"].widget.attrs["class"] = "user_choice"
        self.fields["NTP"].widget.attrs["onclick"] = "javascript:toggleDiv('user_choice');"

class ListBucketsForm(forms.Form):
    aws_id = forms.CharField(label="aws-id",max_length=200)
    aws_key = forms.CharField(label="aws-key",max_length=200)

class S3qlForm(forms.Form):
    aws_id = forms.CharField(label="aws-id",max_length=200)
    aws_key = forms.CharField(label="aws-key",max_length=200)
    bucket_name = forms.CharField(label="bucket_name",max_length=200)
    passphrase = forms.CharField(label="passphrase",max_length=200)


