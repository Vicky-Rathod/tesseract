from django import forms

class SingleForm(forms.Form):
    project_id = forms.IntegerField()
    closeout_company_id = forms.IntegerField()