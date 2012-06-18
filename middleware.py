# -*- coding: UTF-8 -*-
from django.conf import settings

from django_tagcapsule.models import *
import re

class TagCapsuleMiddleware(object):

    def process_response(self, request, response):
        """
        This method is fired each time Django has executed a view and renderes a templats
        and is about to serve the httpresponse to client.
        Here we check all the active tags and insert them at the correct place if they
        match every condition (url patterns and parameters).
        """
        content_with_tags = response.content.decode('utf-8')
        tags = Tag.objects.filter(active=True).select_related("tag_template")

        for tag in tags:
            if self.check_url_patterns(request, tag.url_patterns.all()) and self.check_url_parameters(request, tag.parameter_conditions.all()):
                content_with_tags = tag.insert_in_html(content_with_tags)
        
        content_with_tags = re.sub(r'<!--tagcapsule_values=(.*)-->', '', content_with_tags)
        response.content = content_with_tags
        return response

    def check_url_patterns(self, request, patterns):
        """
        Checks if requested URL matches one of the requested URL patterns.
        @param request
        @param patterns
        @return boolean
        """
        for pattern in patterns:
            pattern_match = re.search(pattern.pattern, request.path)
            if pattern_match == None:
                return False
        return True

    def check_url_parameters(self, request, parameter_conditions):
        """
        Checks if requested URL matches all patterns conditions.
        @param request
        @param parameter_conditions
        @return boolean
        """
        for pc in parameter_conditions:
            if request.GET.get(pc.parameter_name) != pc.parameter_value:
                return False
        return True