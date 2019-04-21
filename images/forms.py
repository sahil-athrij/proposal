from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import person

class PersonForm(forms.ModelForm):
    class Meta:
        model = person
        fields = ('name', 'photo', )

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'imageForm'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit',onclick="showprogress()"))
        self.helper.form_tag =False
