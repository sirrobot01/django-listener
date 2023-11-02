from django.contrib import admin

from listener.models import Source, Event


# Register your models here.


@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'url', 'is_active', 'last_checked', 'content_type',)
    list_filter = ('is_active', 'content_type',)
    search_fields = ('name', 'slug', 'url', 'username', 'password',)
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('last_checked', 'created', 'modified',)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'name', 'unique_id', 'created', 'processed',)
    list_filter = ('source',)
    search_fields = ('source__name', 'name', 'unique_id',)
    readonly_fields = ('created', 'modified',)
    actions = ['process_event', ]

    def process_event(modeladmin, request, queryset):
        for obj in queryset:
            source = obj.source
            processor_class = source.get_processor_class()
            processor = processor_class(obj, force_process=True)
            processor.process()

    process_event.short_description = "Process selected events"
