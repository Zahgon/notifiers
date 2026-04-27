import email
import re
from datetime import datetime

try:
    import jsonschema
    format_checker = jsonschema.FormatChecker()
except ImportError:
    class _NullChecker:
        checks = lambda self, *a, **kw: lambda f: f
    format_checker = _NullChecker()  # type: ignore[assignment]


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
