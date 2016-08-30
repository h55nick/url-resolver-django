from django.test import TestCase
from django.core.urlresolvers import reverse

from .models import UrlMapper
import unittest
import json

class UrlResolverViewTests(TestCase):
    def test_router_with_no_domain(self):
        """
        #create missing domain shows 500 with error message
        """
        response = self.client.post(reverse('url_resolver:router', args={}))
        self.assertEqual(response.status_code, 500)

    def test_router_with_domain(self):
        """
        #create with proper args 200
        """
        test_body = {
            'desktop_url': 'google.com'
        }
        test_json = json.dumps(test_body)
        response = self.client.post(reverse('url_resolver:router'), data=test_json, content_type="application/json")
        desktop_url = json.loads(response.json())[0]['fields']['desktop_url']

        self.assertEqual(response.status_code, 200)
        self.assertEqual(desktop_url, 'google.com')

    def test_show_with_setup(self):
        """
        #show properly redirects
        """
        test_url_map = UrlMapper(desktop_url='nblanchet.com', slug='1234567890')
        test_url_map.save()
        path = reverse('url_resolver:show', args=[test_url_map.slug])
        response = self.client.get(path)
        self.assertEqual(response.get('Location'), 'http:///nblanchet.com')

    def test_index_with_setup(self):
        """
        #index properly renders
        """
        UrlMapper(desktop_url='nblanchet.com', slug='1234567890').save()
        UrlMapper(desktop_url='fake.com', slug='1234567891').save()
        path = reverse('url_resolver:router')
        response = self.client.get(path) # get router => index
        desktop_url_one = json.loads(response.json())[0]['fields']['desktop_url']
        desktop_url_two = json.loads(response.json())[1]['fields']['desktop_url']
        self.assertEqual(desktop_url_one, 'nblanchet.com')
        self.assertEqual(desktop_url_two, 'fake.com')
