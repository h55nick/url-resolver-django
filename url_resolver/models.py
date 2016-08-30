from __future__ import unicode_literals

from django.db import models

import re as regex
import urlparse

# Define constants
MAX_URL_LENGTH = 200
# SLUG Length note:
# increasing this decreases collision chance but
# increases people on twitter being angry about longer urls
# although I think twitter now shortens them anyway?
MAX_SLUG_LENGTH = 10

# Notes: incredible basic implementation of referrer parsing

TABLET_REGEX = r'iPad'
MOBILE_REGEX = r'iPhone'

def is_tablet(user_agent):
    return regex.search(TABLET_REGEX, user_agent)
def is_mobile(user_agent):
    return regex.search(MOBILE_REGEX, user_agent)

def ensure_url(potential_url):
    return urlparse.urlparse(potential_url, 'http').geturl()

# Create your models here.
class UrlMapper(models.Model):
    """
    helps in the resolving of 'slugs' with desktop, mobile, and tablet urls.
    """
    desktop_url = models.CharField(max_length=MAX_URL_LENGTH, unique=True)
    # Notes: mobile & tablet urls will fallback to desktop
    # however this will happen at read so changing the logic is easy and
    # we reduce db size/don't duplicate information.
    mobile_url = models.CharField(max_length=MAX_URL_LENGTH, null=True, blank=True)
    tablet_url = models.CharField(max_length=MAX_URL_LENGTH, null=True, blank=True)

    # Notes: redirect_count
    redirect_count = models.IntegerField(default=0)

    # Notes: created_at, updated_at are used for trouble shooting and have
    # no direct business implications.
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Notes: slug is the shortcode for the url
    slug = models.CharField(max_length=MAX_SLUG_LENGTH)

    def resolved_url(self, user_agent):
        if is_tablet(user_agent) and self.tablet_url != '':
            return ensure_url(self.tablet_url)
        elif is_mobile(user_agent) and self.mobile_url != '':
            return ensure_url(self.mobile_url)
        else:
            return ensure_url(self.desktop_url)
