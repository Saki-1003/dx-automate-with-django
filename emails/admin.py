from django.contrib import admin
from .models import List, Subscriber, Email, Sent, EmailTracking


class EmailTrackingAdmin(admin.ModelAdmin):
  list_display = ('email', 'subscriber', 'clicked_at')

# Register your models here.
admin.site.register(List)
admin.site.register(Subscriber)
admin.site.register(Email)
admin.site.register(Sent)
admin.site.register(EmailTracking, EmailTrackingAdmin)