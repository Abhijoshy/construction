from django.contrib import admin
from .models import Project

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'location', 'status', 'priority', 'budget', 'manager', 'start_date', 'end_date']
    list_filter = ['status', 'priority', 'manager']
    search_fields = ['name', 'location', 'description']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Project Information', {
            'fields': ('name', 'description', 'location', 'manager')
        }),
        ('Project Details', {
            'fields': ('status', 'priority', 'budget', 'start_date', 'end_date')
        }),
        ('Documents', {
            'fields': ('document',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
