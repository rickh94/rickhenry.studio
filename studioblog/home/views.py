import http.client
import json
from typing import Any

from django import forms
from django.conf import settings
from django.core.mail import EmailMessage
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import FormView


class ContactForm(forms.Form):
    """
    A simple contact form that emails me. Spam protection using botpoison and a
    honeypot field called 'information'.
    """

    name = forms.CharField(required=True, label="Your Name")
    from_email = forms.EmailField(required=True, label="Your Email")
    subject = forms.CharField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)
    information = forms.CharField(
        required=False, widget=forms.HiddenInput
    )  # this field is a honeypot for botspam
    botpoison = forms.CharField(required=True, widget=forms.HiddenInput)

    def clean(self) -> dict[str, Any] | None:
        cleaned_data = super().clean()
        if not cleaned_data:
            return None
        # if it filled out the honeypot, stop now
        if cleaned_data.get("information"):
            raise forms.ValidationError("You’re a bot, go away.")
        # get the botpoison solution from the form and use the rest api to verify it.
        if bp_solution := cleaned_data.get("botpoison"):
            data = json.dumps(
                {
                    "secretKey": settings.BOTPOISON_SECRET_KEY,
                    "solution": bp_solution,
                }
            )
            conn = http.client.HTTPSConnection("api.botpoison.com")
            conn.request(
                "POST",
                "/verify",
                body=data,
                headers={
                    "Content-Type": "application/json",
                    "Accept": "application/json",
                },
            )
            response = conn.getresponse()
            response_data = json.loads(response.read())
            if response.status != 200 or not response_data.get("ok"):
                self.add_error("botpoison", "You’re a bot, go away.")
            conn.close()
        else:
            self.add_error("botpoison", "You’re a bot, go away.")

        return cleaned_data

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
