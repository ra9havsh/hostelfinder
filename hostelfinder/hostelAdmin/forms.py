from django.forms import  ModelForm
from django import forms
from hostelAdmin.models import Hostel, Room, Fee,Image

class HostelForm(ModelForm):
    class Meta:
        model=Hostel
        fields = ['hostel_name','hostel_type','hostel_phone','hostel_mobile','location','latitude','longitude','additional_location']
        widgets = {
            'hostel_name': forms.TextInput(attrs={'style': 'width:100%;'}),
            'hostel_type': forms.Select(attrs={'style': 'width:150px'}),
            'hostel_phone': forms.TextInput(attrs={'style': 'width:200px'}),
            'hostel_mobile': forms.TextInput(attrs={'style': 'width:200px'}),
            'location': forms.Select(attrs={'style': 'width:350px'}),
            'latitude': forms.TextInput(attrs={'style': 'width:150px'}),
            'longitude': forms.TextInput(attrs={'style': 'width:150px'}),
            'additional_location': forms.TextInput(attrs={'style': 'width:250px'}),
        }

class RoomForm(ModelForm):
    def __init__(self, *args, **kwargs):
        # first call parent's constructor
        super(RoomForm, self).__init__(*args, **kwargs)
        # there's a `fields` property now
        self.fields['room_price'].required = False

    class Meta:
        model = Room
        fields = ['seater_type','quantity','room_price','available']
        widgets = {
            'seater_type': forms.NumberInput(attrs={'id': 'seater_type'}),
            'quantity': forms.NumberInput(attrs={'id': 'quantity'}),
            'room_price': forms.TextInput(attrs={'id': 'room_price'}),
            'available': forms.NumberInput(attrs={'id': 'available'}),
        }

class FeeForm(ModelForm):
    class Meta:
        model = Fee
        fields = ['admission_fee','refundable_fee','security_fee']

class ImageForm(ModelForm):
    class Meta:
        model = Image
        fields = ['profile_image','hostel_image','room','kitchen']


class RoomDetailForm(forms.Form):
        room_detail = forms.CharField(label='',required=False,widget=forms.Textarea(attrs={'id': 'room_json','style':'display:none;'}))
        class Meta:
            fields = ['room_detail']





