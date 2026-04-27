from . import email


class Gmail(email.SMTP):
    """Send email via Gmail"""

    site_url = "https://www.google.com/gmail/about/"
    base_url = "smtp.gmail.com"
    name = "gmail"

    @property
    def defaults(self) -> dict:
        pass
