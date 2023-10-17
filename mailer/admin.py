from django.contrib import admin
from mailer.models import Mailer, Logs, Message

@admin.register(Mailer)
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

