from string import punctuation, digits, ascii_letters as letters

from django import forms
from django.utils import timezone

from .models import (Profile, Workshop, Comment, department_choices, title, source, states, WorkshopType,
                     AttachmentFile)

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .send_mails import generate_activation_key

UNAME_CHARS = letters + "._" + digits
PWD_CHARS = letters + punctuation + digits


def _add_form_control(fields):
    """Add Bootstrap form-control class to all visible widgets."""
    for name, field in fields.items():
        widget = field.widget
        cls = widget.__class__.__name__
        if cls in ('Select', 'NullBooleanSelect'):
            widget.attrs.setdefault('class', 'form-control custom-select')
        elif cls == 'CheckboxInput':
            widget.attrs.setdefault('class', 'form-check-input')
        elif cls == 'Textarea':
            widget.attrs.setdefault('class', 'form-control')
            widget.attrs.setdefault('rows', '4')
        elif cls not in ('HiddenInput', 'MultipleHiddenInput'):
            widget.attrs.setdefault('class', 'form-control')


class UserRegistrationForm(forms.Form):
    """A Class to create new form for User's Registration."""
    required_css_class = 'required'
    errorlist_css_class = 'errorlist'

    username = forms.CharField(
        max_length=32,
        help_text='Letters, digits, period and underscore only.',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g. john_doe',
            'autocomplete': 'username',
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'you@example.com',
            'autocomplete': 'email',
        })
    )
    password = forms.CharField(
        max_length=32,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Choose a strong password',
            'autocomplete': 'new-password',
        })
    )
    confirm_password = forms.CharField(
        max_length=32,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Repeat your password',
            'autocomplete': 'new-password',
        })
    )
    title = forms.ChoiceField(
        choices=title,
        widget=forms.Select(attrs={'class': 'form-control custom-select'})
    )
    first_name = forms.CharField(
        max_length=32,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'First name',
            'autocomplete': 'given-name',
        })
    )
    last_name = forms.CharField(
        max_length=32,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Last name',
            'autocomplete': 'family-name',
        })
    )
    phone_number = forms.RegexField(
        regex=r'^.{10}$',
        error_messages={'invalid': "Phone number must be 10 digits, e.g. 9876543210."},
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '9876543210',
            'inputmode': 'numeric',
            'autocomplete': 'tel-national',
            'maxlength': '10',
        })
    )
    institute = forms.CharField(
        max_length=128,
        help_text='Please write the full name of your Institute or Organisation.',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g. IIT Bombay',
            'autocomplete': 'organization',
        })
    )
    department = forms.ChoiceField(
        help_text='Department you work/study in.',
        choices=department_choices,
        widget=forms.Select(attrs={'class': 'form-control custom-select'})
    )
    location = forms.CharField(
        max_length=255,
        help_text='City or place.',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g. Mumbai',
            'autocomplete': 'address-level2',
        })
    )
    state = forms.ChoiceField(
        choices=states,
        widget=forms.Select(attrs={'class': 'form-control custom-select'})
    )
    how_did_you_hear_about_us = forms.ChoiceField(
        choices=source,
        widget=forms.Select(attrs={'class': 'form-control custom-select'})
    )

    def clean_username(self):
        u_name = self.cleaned_data["username"]
        if u_name.strip(UNAME_CHARS):
            raise forms.ValidationError(
                "Only letters, digits, period and underscore are allowed in username."
            )
        try:
            User.objects.get(username__exact=u_name)
            raise forms.ValidationError("Username already exists.")
        except User.DoesNotExist:
            return u_name

    def clean_password(self):
        pwd = self.cleaned_data['password']
        if pwd.strip(PWD_CHARS):
            raise forms.ValidationError(
                "Only letters, digits and punctuation are allowed in password."
            )
        return pwd

    def clean_confirm_password(self):
        c_pwd = self.cleaned_data['confirm_password']
        pwd = self.data['password']
        if c_pwd != pwd:
            raise forms.ValidationError("Passwords do not match.")
        return c_pwd

    def clean_email(self):
        user_email = self.cleaned_data['email']
        if User.objects.filter(email=user_email).exists():
            raise forms.ValidationError("An account with this email already exists.")
        return user_email

    def save(self):
        u_name = self.cleaned_data["username"].lower()
        pwd = self.cleaned_data["password"]
        email = self.cleaned_data["email"]
        new_user = User.objects.create_user(u_name, email, pwd)
        new_user.first_name = self.cleaned_data["first_name"]
        new_user.last_name = self.cleaned_data["last_name"]
        new_user.save()

        cleaned_data = self.cleaned_data
        new_profile = Profile(user=new_user)
        new_profile.institute = cleaned_data["institute"]
        new_profile.department = cleaned_data["department"]
        new_profile.phone_number = cleaned_data["phone_number"]
        new_profile.location = cleaned_data["location"]
        new_profile.title = cleaned_data["title"]
        new_profile.state = cleaned_data["state"]
        new_profile.how_did_you_hear_about_us = cleaned_data["how_did_you_hear_about_us"]
        new_profile.activation_key = generate_activation_key(new_user.username)
        new_profile.key_expiry_time = timezone.now() + timezone.timedelta(days=1)
        new_profile.save()
        return u_name, pwd, new_profile.activation_key


class UserLoginForm(forms.Form):
    """Login form."""
    username = forms.CharField(
        max_length=32,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Username',
            'autocomplete': 'username',
            'autofocus': True,
        })
    )
    password = forms.CharField(
        max_length=32,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password',
            'autocomplete': 'current-password',
        })
    )

    def clean(self):
        super(UserLoginForm, self).clean()
        try:
            u_name = self.cleaned_data["username"]
            pwd = self.cleaned_data["password"]
            user = authenticate(username=u_name, password=pwd)
        except Exception:
            raise forms.ValidationError("Please enter both username and password.")
        if not user:
            raise forms.ValidationError("Invalid username or password.")
        return user


class WorkshopForm(forms.ModelForm):
    """Coordinators propose a workshop and date."""
    errorlist_css_class = 'errorlist'

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(WorkshopForm, self).__init__(*args, **kwargs)
        self.fields['tnc_accepted'].label = ""
        self.fields['tnc_accepted'].required = True
        self.fields['workshop_type'].label = "Workshop type"
        self.fields['date'].label = "Preferred date"

    class Meta:
        model = Workshop
        exclude = ['status', 'instructor', 'coordinator']
        widgets = {
            'date': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control',
                },
                format='%Y-%m-%d'
            ),
            'workshop_type': forms.Select(attrs={'class': 'form-control custom-select'}),
            'tnc_accepted': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class CommentsForm(forms.ModelForm):
    """Users post comments on workshops."""

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(CommentsForm, self).__init__(*args, **kwargs)
        self.fields['comment'].required = True
        self.fields['public'].label = "Public"

    class Meta:
        model = Comment
        exclude = ['author', 'created_date', 'workshop']
        widgets = {
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': '4',
                'placeholder': 'Write your comment here…',
            }),
            'public': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class WorkshopTypeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(WorkshopTypeForm, self).__init__(*args, **kwargs)
        for field in self.visible_fields():
            cls = field.field.widget.__class__.__name__
            if cls == 'Textarea':
                field.field.widget.attrs.update({'class': 'form-control', 'rows': '5'})
            elif cls not in ('CheckboxInput',):
                field.field.widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = WorkshopType
        exclude = []


class AttachmentFileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AttachmentFileForm, self).__init__(*args, **kwargs)
        _add_form_control(self.fields)

    class Meta:
        model = AttachmentFile
        exclude = ['workshop_type']


class ProfileForm(forms.ModelForm):
    """Profile form for coordinators and instructors."""

    first_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'First name',
            'autocomplete': 'given-name',
        })
    )
    last_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Last name',
            'autocomplete': 'family-name',
        })
    )

    class Meta:
        model = Profile
        exclude = ["user", "is_email_verified", "activation_key",
                   "key_expiry_time", "how_did_you_hear_about_us"]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(ProfileForm, self).__init__(*args, **kwargs)

        if user:
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name

        widget_map = {
            'institute':    ('form-control', 'Institute'),
            'phone_number': ('form-control', 'Phone number'),
            'position':     ('form-control', None),
            'location':     ('form-control', 'City / Location'),
        }
        for field_name, (css, placeholder) in widget_map.items():
            if field_name in self.fields:
                self.fields[field_name].widget.attrs.update({'class': css})
                if placeholder:
                    self.fields[field_name].widget.attrs.update({'placeholder': placeholder})

        for field_name in ('department', 'title', 'state'):
            if field_name in self.fields:
                self.fields[field_name].widget.attrs.update(
                    {'class': 'form-control custom-select'}
                )
