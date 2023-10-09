from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from templated_mail.mail import BaseEmailMessage

from djoser import utils
from djoser.conf import settings


class InvitationEmail(BaseEmailMessage):
    template_name = "email/invitation.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        user = context.get("user")
        context["to_user"] = user.first_name
        context["uid"] = utils.encode_uid(user.pk)
        context["token"] = default_token_generator.make_token(user)
        context["url"] = settings.DJSOSER["INVITE_ACTIVATION_URL"].format(**context)

        return context


class ConfirmationEmail(BaseEmailMessage):
    template_name = "email/confirmation.html"