from django.contrib import admin

from mailling.models import Client, Mailling, Logs, Message


@admin.register(Mailling)
class MaillingAdmin(admin.ModelAdmin):
    list_display = ('date_start', 'date_end', 'periodicity', 'status',)
    list_filter = ('status', 'periodicity',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('subject_letter', 'body_letter',)


@admin.register(Logs)
class LogsAdmin(admin.ModelAdmin):
    list_display = ('last_try', 'status_try',)
    list_filter = ('status_try', 'answer',)

