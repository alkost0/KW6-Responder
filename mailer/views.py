import random

from django.http import Http404
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView, TemplateView

from blog.models import Blog
from mailer.forms import MessageForm, MailerForm
from mailer.models import Mailer, Logs, Message
from mailer.services import send_message_email, get_cache_count_mailer, get_cache_count_client


class MailerCreateView(CreateView):
    model = Mailer
    form_class = MailerForm
    success_url = reverse_lazy('mailer:mailer_list')

    def form_valid(self, form):
        self.obj = form.save()
        self.obj.owner = self.request.user
        send_message_email(self.obj)
        self.obj.save()

        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'uid': self.request.user.id})
        return kwargs


class MailerListView(ListView):
    model = Mailer

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Список рассылок"
        return context


class MailerDetailView(DetailView):
    model = Mailer

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Подробная информация о рассылке"
        return context


class MailerUpdateView(UpdateView):
    model = Mailer
    form_class = MailerForm

    def get_success_url(self):
        return reverse('mailer:mailer_view', args=[self.kwargs.get('pk')])

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user:
            raise Http404
        return self.object

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'uid': self.request.user.id})
        return kwargs


class MailerDeleteView(DeleteView):
    model = Mailer
    success_url = reverse_lazy('mailer:mailer_list')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user and not self.request.user.is_staff:
            raise Http404
        return self.object


class LogsListView(ListView):
    model = Logs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Отчет проведенных рассылок"
        return context


class MessageCreateView(CreateView):
    model = Message
    form_class = MessageForm

    def get_success_url(self, *args, **kwargs):
        return reverse('mailer:mailer_list')

    def form_valid(self, form):
        self.obj = form.save()
        self.obj.owner = self.request.user
        self.obj.save()

        return super().form_valid(form)



class MessageUpdateView(UpdateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mailer:mailer_list')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user:
            raise Http404
        return self.object


class MessageDeleteView(DeleteView):
    model = Message
    success_url = reverse_lazy('mailer:mailer_list')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user:
            raise Http404
        return self.object


class MainView(TemplateView):
    template_name = 'mailer/main.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = "Cервис управления рассылками"
        context_data['object_list'] = random.sample(list(Blog.objects.all()), 3)
        context_data['mailer'] = get_cache_count_mailer()
        context_data['active_mailer'] = Mailer.objects.filter(status='started').count()
        context_data['client'] = get_cache_count_client()
        return context_data
