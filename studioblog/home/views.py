from django import forms
from django.conf import settings
from django.core.mail import EmailMessage
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import FormView


class ContactForm(forms.Form):
    name = forms.CharField(required=True, label="Your Name")
    from_email = forms.EmailField(required=True, label="Your Email")
    subject = forms.CharField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)

    def send_email(self):
        email = EmailMessage(
            self.cleaned_data["subject"],
            self.cleaned_data["message"],
            None,
            settings.ADMINS,
            reply_to=[
                f"{self.cleaned_data['name']} <{self.cleaned_data['from_email']}>"
            ],
        )
        email.send()


class ContactFormView(FormView):
    template_name = "home/contact.html"
    form_class = ContactForm
    success_url = reverse_lazy("thank-you")

    def form_valid(self, form):
        form.send_email()
        return super().form_valid(form)

    def get_template_names(self):
        if self.request.htmx and not self.request.htmx.boosted:
            return ["home/htmx/contact.html"]
        else:
            return ["home/contact.html"]


def thank_you(request):
    response = None
    if request.htmx and not request.htmx.boosted:
        response = render(request, "home/htmx/thank-you.html")
        response.headers["HX-Push-Url"] = reverse_lazy("thank-you")
    else:
        response = render(request, "home/thank-you.html")
    return response
