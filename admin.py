# -*- coding: UTF-8 -*-
from django.contrib import admin
from django_tagcapsule.models import *


class UrlPatternAdmin(admin.ModelAdmin):
    list_display = ('name', 'pattern')
    list_filter = ('name',)
    search_fields = ('name',)
    ordering = ('name',)

class ParameterConditionInline(admin.TabularInline):
    model = ParameterCondition
    extra = 1

class ValueInline(admin.TabularInline):
    model = Value
    extra = 1
    
class TagAdmin(admin.ModelAdmin):
    list_display = ('tag_template', 'active')
    list_filter = ('tag_template',)
    inlines = (ValueInline, ParameterConditionInline)
    ordering = ('tag_template',)


admin.site.register(TagTemplate)
admin.site.register(UrlPattern, UrlPatternAdmin)
admin.site.register(Tag, TagAdmin)
