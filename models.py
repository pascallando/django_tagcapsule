# -*- coding: UTF-8 -*-
from django.db import models
from django.utils import simplejson

import re

INSERT_POINT_PLACES = (
    (0, 'Above'),
    (1, 'Below'),
)

class TagTemplate(models.Model):
    """
    This class is used to define tag templates. Ex: Google analytics template.
    """
    name = models.CharField(max_length=255)
    content = models.TextField()
    insert_point_place = models.PositiveSmallIntegerField(choices=INSERT_POINT_PLACES)
    insert_point_pattern = models.CharField(max_length=150)
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.name

class UrlPattern(models.Model):
    """
    URL patterns allow the user to restrict tag insertion.
    The tag will be inserted only if the requested URL matches one on the patterns.
    Ex. : "Insert the tag only if URL is like ^.*/market/.*$"
    """
    name = models.CharField(max_length=100)
    pattern = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name + ": " + self.pattern

class Tag(models.Model):
    """
    The tag class, allowing to store all the tags. A tag must have a tag template.
    """
    tag_template = models.ForeignKey(TagTemplate)
    url_patterns = models.ManyToManyField(UrlPattern, blank=True, null=True)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.tag_template.name
        
    def insert_in_html(self, html_source):
        """
        Inserts the tag and its values at the right place in html source.
        @param html_source The html code where we want to insert the tag
        """
        prepared_tag = self.tag_template.content

        tagcapsule_values_pattern = re.compile(r'<!--tagcapsule_values=(.*)-->')
        dynamic_values_json = re.search(tagcapsule_values_pattern, html_source)
        if dynamic_values_json:
            dynamic_values = simplejson.loads(dynamic_values_json.group(1))
        else:
            dynamic_values = None
        
        for value in self.values.all():
            placeholder = "{{!" + value.variable_name + "}}"
            if not value.is_dynamic:
                prepared_tag = prepared_tag.replace(placeholder, value.value)
            else:
                if dynamic_values and value.variable_name in dynamic_values:
                    prepared_tag = prepared_tag.replace(placeholder, str(dynamic_values[value.variable_name]))
        
        if self.tag_template.insert_point_place == 0:
            replacement_text = prepared_tag + self.tag_template.insert_point_pattern
        else:
            replacement_text = self.tag_template.insert_point_pattern + prepared_tag

        return html_source.replace(self.tag_template.insert_point_pattern, replacement_text)

class Value(models.Model):
    """
    A value which should be inserted in a tag.
    Values can be dynamic (i.e. calculated by the programer in the view) or not (stored in database).
    """
    tag = models.ForeignKey(Tag, related_name="values")
    variable_name = models.CharField(max_length=100)
    value = models.CharField(max_length=100, null=True, blank=True)
    is_dynamic = models.BooleanField(default=False)
    
class ParameterCondition(models.Model):
    """
    Parameter conditions allow the user to restrict tag insertion.
    The tag will be inserted only if the parameter is setted and the value matches.
    Ex. : "Insert the tag only if url parameter ?sourceId=12"
    """
    tag = models.ForeignKey(Tag, related_name="parameter_conditions")
    parameter_name = models.CharField(max_length=100)
    parameter_value = models.CharField(max_length=100)
    
