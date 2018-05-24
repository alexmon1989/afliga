from django import forms
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import get_template
from apps.contacts.models import ContactEmail


class ContactForm(forms.Form):
    """Форма контактов."""
    first_name = forms.CharField(label='Имя', max_length=100)
    last_name = forms.CharField(label='Фамилия', max_length=100)
    email = forms.EmailField(label='E-Mail', max_length=100)
    phone = forms.CharField(label='Телефон', max_length=100)
    message = forms.CharField(label='Сообщение', max_length=1000, widget=forms.Textarea)

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
