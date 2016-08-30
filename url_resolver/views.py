from django.shortcuts import render, redirect
from django.http import JsonResponse

import json
import hashlib
from .models import UrlMapper
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist

# should be moved to global const folder
POST_KEY = 'POST'

# Notes: Helper Methods
def render_json_error(error):
    errors = { 'error': error }
    return JsonResponse(errors, status=500)

def router(request):
    """
    routes post/get for /u/
    """
    if(request.method == POST_KEY):
        return create(request)
    else:
        return index(request)

# Notes: Controller Implementation
def index(request):
    """
    index
    """
    all_url_maps = UrlMapper.objects.all()
    response_json = serializers.serialize('json', all_url_maps)
    return JsonResponse(response_json, safe=False)

def show(request, slug=None):
    """
    this is the redirect method to handle slugs
    """

    user_agent = request.META.get('HTTP_USER_AGENT', 'desktop')

    try:
        url_map = UrlMapper.objects.get(slug=slug)
    except ObjectDoesNotExist, _e:
        return JsonResponse({ 'error': 'redirect failed.'}, status=404)

    # Notes: increase redirect_count
    # - as we do not ensure success this is more redirect_attempt_count :-/
    url_map.redirect_count += 1
    url_map.save()

    redirect_url = url_map.resolved_url(user_agent)
    return redirect(redirect_url)

def create(request):
    """create"""
    try:
        body_unicode = request.body.decode('utf-8')
        json_body = json.loads(body_unicode)
    except ValueError:
        return render_json_error('Body could not be parsed. Please send a valid json body.')

    desktop_url = json_body.get('desktop_url', None)
    # Validate desktop url.
    # FIXME: Most likely a more django way of doing this.
    if desktop_url == None:
        return render_json_error('desktop_url is a required field.')

    # Notes: default is MD5 of the reverse of the desktop-url.
    # Reversing will decrease collision risk.
    # the best way to decrease collision risk however would be to increase the allowed length.
    default_slug = hashlib.md5(desktop_url[::-1]).hexdigest()[0:10]
    slug = json_body.get('slug', default_slug)

    # Notes: Saving UrlMapper
    try:
        r = UrlMapper(
            desktop_url= desktop_url,
            mobile_url= json_body.get('mobile_url', ''),
            tablet_url= json_body.get('tablet_url', ''),
            slug= slug
        )
        r.save()
        response_json = serializers.serialize('json', [r])
        return JsonResponse(response_json, safe=False)
    except Exception, e:
        return render_json_error(str(e))
