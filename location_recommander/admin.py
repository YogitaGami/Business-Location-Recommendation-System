from django.contrib import admin
from location_recommander.models import Contact , History
# Register your models here.

admin.site.register(Contact)

class HistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'Business_search', 'result', 'created_at')
    search_fields = ('user__username', 'Business_search', 'result')
    list_filter = ('created_at',)
    ordering = ('-created_at',)  # Orders by created_at descending

admin.site.register(History, HistoryAdmin)