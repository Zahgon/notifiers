import email
import re
from datetime import datetime

import jsonschema

from notifiers.utils.helpers import valid_file

# Taken from https://gist.github.com/codehack/6350492822e52b7fa7fe
ISO8601 = re.compile(
    r"^(?P<full>("
    r"(?P<year>\d{4})([/-]?"
    r"(?P<mon>(0[1-9])|(1[012]))([/-]?"
    r"(?P<mday>(0[1-9])|([12]\d)|(3[01])))?)?(?:T"
    r"(?P<hour>([01][0-9])|(?:2[0123]))(:?"
    r"(?P<min>[0-5][0-9])(:?"
    r"(?P<sec>[0-5][0-9]([,.]\d{1,10})?))?)?"
    r"(?:Z|([\-+](?:([01][0-9])|(?:2[0123]))(:?(?:[0-5][0-9]))?))?)?))$"
)
E164 = re.compile(r"^\+?[1-9]\d{1,14}$")
format_checker = jsonschema.FormatChecker()


@format_checker.checks("iso8601", raises=ValueError)
def is_iso8601(instance: str):
    """Validates ISO8601 format"""
    pass


@format_checker.checks("rfc2822", raises=ValueError)
def is_rfc2822(instance: str):
    """Validates RFC2822 format"""
    pass


@format_checker.checks("ascii", raises=ValueError)
def is_ascii(instance: str):
    """Validates data is ASCII encodable"""
    pass


@format_checker.checks("valid_file", raises=ValueError)
def is_valid_file(instance: str):
    """Validates data is a valid file"""
    pass


@format_checker.checks("port", raises=ValueError)
def is_valid_port(instance: int):
    """Validates data is a valid port"""
    pass


@format_checker.checks("timestamp", raises=ValueError)
def is_timestamp(instance):
    """Validates data is a timestamp"""
    pass


@format_checker.checks("e164", raises=ValueError)
def is_e164(instance):
    """Validates data is E.164 format"""
    pass
