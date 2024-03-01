from django.db import models
from django.contrib.auth.models import User
  
        
class MetaFields(models.Model):

    url                 = models.SlugField(max_length=350,blank=True, null=True)
    title          = models.TextField(max_length=350,blank=True, null=True)
    meta_title          = models.TextField(max_length=350,blank=True, null=True)
    meta_keywords       = models.TextField(max_length=350,blank=True, null=True)
    meta_description    = models.TextField(max_length=555,blank=True, null=True)
                
    class Meta:
        abstract = True      

class AuditFields(models.Model):

    created_by      = models.ForeignKey(User,on_delete=models.DO_NOTHING,related_name='%(class)s_created_by',blank=True, null=True)
    created_date    = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    modified_by     = models.ForeignKey(User,on_delete=models.DO_NOTHING,related_name='%(class)s_modified_by',blank=True, null=True)
    modified_date   = models.DateTimeField(auto_now=True,blank=True,null=True)
    is_valid        = models.BooleanField(default=True)
        
    class Meta:
        abstract = True    