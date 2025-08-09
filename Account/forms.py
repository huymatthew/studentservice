from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import StudentProfile

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Email")
    first_name = forms.CharField(max_length=30, required=True, label="Họ")
    last_name = forms.CharField(max_length=30, required=True, label="Tên")

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Thêm CSS classes cho các field
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control',
                'placeholder': field.label
            })

class CustomUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
        labels = {
            'first_name': 'Họ',
            'last_name': 'Tên',
            'email': 'Email'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name == 'avatar':
                field.widget.attrs.update({'class': 'form-control-file'})
            else:
                field.widget.attrs.update({
                    'class': 'form-control',
                    'placeholder': field.label
                })

class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = ('student_id', 'class_name', 'major', 'avatar', 'birth_date', 'gpa', 'credits_earned', 'status')
        labels = {
            'student_id': 'Mã số sinh viên',
            'class_name': 'Lớp',
            'major': 'Ngành học',
            'avatar': 'Ảnh đại diện',
            'birth_date': 'Ngày sinh',
            'gpa': 'Điểm trung bình',
            'credits_earned': 'Số tín chỉ đã tích lũy',
            'status': 'Trạng thái'
        }
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name == 'avatar':
                field.widget.attrs.update({'class': 'form-control-file'})
            else:
                field.widget.attrs.update({
                    'class': 'form-control',
                    'placeholder': field.label
                })
