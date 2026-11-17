from django import forms


class ContactForm(forms.Form):
    nom = forms.CharField(label="Nom")
    email = forms.EmailField(label="Email")
    message = forms.CharField(widget=forms.Textarea, label="Message")

