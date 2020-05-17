from django import forms

MONTH_CHOICES = ((1, 'January'), (2, 'February'), (3, 'March'), (4, 'April'), (5, 'May'), (6, 'June'), (7, 'July'), (8, 'August'), (9, 'September'), (10, 'October'), (11, 'November'), (12, 'December'))

class Register_Form(forms.Form):
    username                = forms.CharField(label = 'Username', required = True)
    password                = forms.CharField(label = 'Password', required = True, widget=forms.PasswordInput)
    password2               = forms.CharField(label = 'Type Password Again', required = True, widget=forms.PasswordInput)
    email                   = forms.EmailField(label = 'E-Mail', required = True)
    first_name              = forms.CharField(label = 'First Name', required = True)
    last_name               = forms.CharField(label = 'Last Name', required = True)
    date_of_birth           = forms.DateField(label = 'Date Of Birth', input_formats = '%Y-%m-%d', widget = forms.DateInput, required = True)


    
