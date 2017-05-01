'''
Created on Mar 20, 2015

@author: root
'''
from django import forms
from django.conf import settings
from django.utils.safestring import mark_safe 
from django.template.loader import render_to_string  

class Ueditor(forms.Textarea):
    class Media:
        js  = (  
                settings.STATIC_URL + 'ueditor/ueditor.config.js',
                settings.STATIC_URL + 'ueditor/ueditor.all.js',  
        )   
    def __init(self,attrs = {}):
        super(Ueditor,self).__init__(attrs)
        
    def render(self, name, value, attrs=None):  
        rendered = super(Ueditor, self).render(name, value, attrs)  
        context = {  
            'name': name,  
            'STATIC_URL': settings.STATIC_URL,
            'STATIC_ROOT': settings.STATIC_ROOT,
            'MEDIA_URL': settings.MEDIA_URL,
            'MEDIA_ROOT': settings.MEDIA_ROOT 
        }  
         
        return rendered  + mark_safe(render_to_string('ueditor.html',context))  
        
    
     
    