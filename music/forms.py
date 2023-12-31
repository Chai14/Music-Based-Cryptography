from django import forms

class EncryptionForm(forms.Form):
    text_to_encrypt = forms.CharField(label='Enter Text:', max_length=255, required=False)
    midi_file = forms.FileField(label='Upload MIDI File:', required=False)

class DecryptionForm(forms.Form):
    midi_file = forms.FileField(label='Upload Encrypted MIDI File:', required=False)