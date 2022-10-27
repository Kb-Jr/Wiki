from django import forms

class EntryForm(forms.Form):
    entry_name = forms.CharField(label = "Entry name")
    entry_content = forms.CharField(
        label="Entry content",
        widget=forms.Textarea(attrs={'rows':2, 'cols':2})
    )

class EditForm(forms.Form):
    entry_content = forms.CharField(
        label="Entry content",
        widget=forms.Textarea()
    )