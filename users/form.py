from django import forms

class SignupForm(forms.Form):
    username = forms.CharField(max_length=200)
    password = forms.CharField(label="密码", max_length=255)
    confirm_password = forms.CharField(label="确认密码", max_length=255)

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError(u'两次输入密码不一致')
        return password