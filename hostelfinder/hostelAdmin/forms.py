from django.forms import  ModelForm
from django import forms
from hostelAdmin.models import Geography, Hostel, Room, Fee,Image

class HostelForm(ModelForm):
    class Meta:
        model=Hostel
        fields = ['hostel_name','hostel_type','hostel_phone','hostel_mobile']
        widgets = {
            'hostel_name': forms.TextInput(attrs={'style': 'width:100%;'}),
            'hostel_type': forms.Select(attrs={'style': 'width:150px'}),
            'hostel_phone': forms.TextInput(attrs={'style': 'width:200px'}),
            'hostel_mobile': forms.TextInput(attrs={'style': 'width:200px'}),
        }

class GeographyForm(ModelForm):
    class Meta:
        model = Geography
        fields = ['location','latitude','longitude','additional']
        widgets = {
            'location': forms.Select(attrs={'style': 'width:350px'}),
            'latitude': forms.TextInput(attrs={'style': 'width:150px'}),
            'longitude': forms.TextInput(attrs={'style': 'width:150px'}),
            'additional': forms.TextInput(attrs={'style': 'width:250px'}),
        }

class RoomForm(ModelForm):
    def __init__(self, *args, **kwargs):
        # first call parent's constructor
        super(RoomForm, self).__init__(*args, **kwargs)
        # there's a `fields` property now
        self.fields['room_price'].required = False

    class Meta:
        model = Room
        fields = ['seater_type','quantity','room_price']
        widgets = {
            'seater_type': forms.NumberInput(attrs={'id': 'seater_type'}),
            'quantity': forms.NumberInput(attrs={'id': 'quantity'}),
            'room_price': forms.TextInput(attrs={'id': 'room_price'}),
        }

class FeeForm(ModelForm):
    class Meta:
        model = Fee
        fields = ['admission_fee','refundable_fee','security_fee']

class ImageForm(ModelForm):
    class Meta:
        model = Image
        fields = ['profile_image','image1','image2','image3','image4','image5']


class RoomDetailForm(forms.Form):
        room_detail = forms.CharField(label='',widget=forms.Textarea(attrs={'id': 'room_json','style':'display:none'}))
        class Meta:
            fields = ['room_detail']





