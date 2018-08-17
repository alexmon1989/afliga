from django import forms
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import get_template
from apps.contacts.models import ContactEmail
from captcha.fields import CaptchaField


class ContactForm(forms.Form):
    """Форма контактов."""
    first_name = forms.CharField(label='Имя', max_length=100)
    last_name = forms.CharField(label='Фамилия', max_length=100)
    email = forms.EmailField(label='E-Mail', max_length=100)
    phone = forms.CharField(label='Телефон', max_length=100, required=False)
    message = forms.CharField(label='Сообщение', max_length=1000, widget=forms.Textarea)
    captcha = CaptchaField(label='Решите простой пример')
    hidden = forms.CharField(max_length=32, widget=forms.HiddenInput())
    hidden_changed = forms.BooleanField(widget=forms.HiddenInput())

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(ContactForm, self).__init__(*args, **kwargs)
        self.fields['captcha'].widget.attrs['class'] = 'form-control g-width-auto g-color-black ' \
                                                       'g-bg-white g-bg-white--focus g-brd-primary--focus rounded-3 ' \
                                                       'g-py-13 g-px-15'
        self.fields['captcha'].widget.attrs['style'] = 'display: inline'

    def clean_hidden(self):
        """Антиспам-проверка"""
        data = self.cleaned_data['hidden']

        if data != self.request.session['antispam']:
            raise forms.ValidationError("You're bot!")

        return data

    def send_email(self):
        """Отправляет данные формы на E-Mail."""
        email_template = get_template('contacts/email.html')

        text_content = 'Имя: {}\r\nФамилия: {}\r\nE-Mail: {}\r\nТелефон: {}Сообщение: {}'.format(
            self.cleaned_data['first_name'],
            self.cleaned_data['last_name'],
            self.cleaned_data['email'],
            self.cleaned_data['phone'],
            self.cleaned_data['message']
        )

        recipient_list = ContactEmail.objects.values_list('email', flat=True)

        send_mail(
            subject='Сообщение со страницы контактов',
            message=text_content,
            from_email=getattr(settings, "SERVER_EMAIL", None),
            html_message=email_template.render(self.cleaned_data),
            fail_silently=True,
            recipient_list=recipient_list
        )
