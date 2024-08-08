from django.contrib import admin
from .models import Event
from .models import Student
from .models import UserProfile
from django.apps import apps
from .models import Venue
from .models import Feedback
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name','phoneno' ,'event_type', 'location', 'date', 'venue','amount','payment_status','event_confirmation')
    search_fields = ('name', 'event_type', 'location', 'venue')
    list_filter = ('event_type','location', 'date')
    date_hierarchy = 'date'

admin.site.register(UserProfile)
admin.site.register(Venue)