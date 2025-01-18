from django.contrib import admin
from orgtree.models import Node

# Register your models here.
class NodeAdmin(admin.ModelAdmin):
    list_display = ('name', 'department', 'position', 'email', 'parent')
    search_fields = ('name', 'department', 'position', 'email')
    list_editable = ('department', 'position', 'email', 'parent')
    list_filter = ('department', 'position', 'parent')
    
admin.site.register(Node, NodeAdmin)