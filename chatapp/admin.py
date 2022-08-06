from django.contrib import admin
from .models import Thread,Chat
# Register your models here.


class ChatInline(admin.StackedInline):
    model=Chat
    fields = ('sender', 'text')
    readonly_fields =('sender', 'text')

class ThreadAdmin(admin.ModelAdmin):
    list_display = ['id']
    model = Thread
    inlines = (ChatInline,)


admin.site.register(Thread, ThreadAdmin)

admin.site.register(Chat)