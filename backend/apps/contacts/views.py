from django.views.generic.edit import FormView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from apps.contacts.forms import ContactForm
from apps.contacts.models import Contact
import random
import string


class ContactView(SuccessMessageMixin, FormView):
    """Отображает страницу контактов."""
    template_name = 'contacts/contacts.html'
    form_class = ContactForm
    success_url = reverse_lazy('contacts')
    success_message = 'Спасибо, ваше сообщение было успешно отправлено. Мы ответим на него в ближайшее время.'

    def form_valid(self, form):
        form.send_email()
        return super(ContactView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ContactView, self).get_context_data(**kwargs)
        context['contacts'] = Contact.objects.first()
        return context

    def get_initial(self):
        initial = super(ContactView, self).get_initial()

        # Антиспам
        if self.request.method != 'POST':
            random_string = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(32))
            initial['hidden'] = random_string
            self.request.session['antispam'] = random_string[::-1]

        return initial

    def get_form_kwargs(self):
        kwargs = super(ContactView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs
