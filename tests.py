# -*- coding: UTF-8 -*-
from django.test import TestCase
from django_tagcapsule.models import *


class TagCapsuleTest(TestCase):
    fixtures = ['test_data.json']
    
    def setUp(self):
        self.tags = Tag.objects.all().order_by('id')
        self.html_sample = '<html><head></head><body></body></html>'
            
    def test_insert_in_html(self):
        self.assertEqual(self.tags[0].insert_in_html(self.html_sample), '<html><head><!--"This comment appears on every page"--></head><body></body></html>')
        self.assertEqual(self.tags[5].insert_in_html(self.html_sample), '<html><head></head><body><!--\r\n1\r\n2\r\n3\r\n--></body></html>')
