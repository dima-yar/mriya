
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy, reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView, TemplateView, CreateView, DeleteView, UpdateView, FormView
from dal import autocomplete
from dreams.forms import DreamForm, DonateForm
from dreams.models import Dream, Tag



class PrivatePolycyView(TemplateView):
    template_name = "dreams/privicy_polycy.html"

class TermsOfServiceView(TemplateView):
    template_name = "dreams/terms_of_service.html"


class HomePageView(TemplateView):
    template_name = "dreams/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tags'] = Tag.objects.all()
        return context


class DreamsListView(ListView):
    model = Dream
    paginate_by = 3
    template_name = "dreams/dream_list.html"
    context_object_name = "dreams"



class DreamsSearchView(ListView):
    model = Dream

    template_name = "dreams/dream_search.html"
    context_object_name = "dreams"

    def get_queryset(self):
        search = self.request.GET.get("search", "")
        tags = self.request.GET.getlist("tags")

        queries1 = (
                Q(title__icontains=search) |
                Q(short_descriptions__icontains=search) |
                Q(content__icontains=search)
        )

        if search:
            result = Dream.objects.filter(queries1)
        else:
            result = Dream.objects.all()

        if tags:
            queries2 = Q(tags__name=tags[0])
            for tag_name in tags[1:]:
                queries2 |= Q(tags__name=tag_name)

            result = result.filter(queries2).distinct()

        return result

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = self.request.GET.get("search", "")
        return context


class DreamsDetailView(DetailView):
    model = Dream
    template_name = "dreams/dream_detail.html"
    pk_url_kwarg = 'id'
    context_object_name = "dreams"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_owner'] = self.object.author == self.request.user
        print( context['is_owner'])
        context['dream_id'] = self.object.pk
        return context

# views.py
class DreamsCreateView(LoginRequiredMixin, CreateView):
    model = Dream
    form_class = DreamForm
    template_name = 'dreams/dream_create.html'
    success_url = 'success_url'  # Заміни на реальний URL успіху

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('dream_list')
class DreamUpdateView(UserPassesTestMixin, UpdateView):
    model = Dream
    template_name = "dreams/dream_update.html"
    form_class = DreamForm
    pk_url_kwarg = 'id'

    def get_success_url(self):
        return reverse_lazy("dream_detail", kwargs={'id': self.object.id})

    def test_func(self):

        dreams = self.get_object()
        return dreams.author == self.request.user



class DreamsDeleteView(UserPassesTestMixin, DeleteView):
    model = Dream
    success_url = reverse_lazy("dream_list")
    pk_url_kwarg = 'id'

    def test_func(self):

        dreams = self.get_object()
        return dreams.author == self.request.user



class DreamsDonatetView(FormView):

    form_class = DonateForm
    template_name = "dreams/dream_donate.html"

    def get_success_url(self):
        # Повертає URL на сторінку мрії після успішного платежу
        return reverse_lazy("dream_detail", kwargs={'id': self.kwargs['id']})

    def form_valid(self, form):
        dream = get_object_or_404(Dream, id=self.kwargs['id'])

        if dream.status == 'active':
            prise = form.cleaned_data['amount']

            dream.current_amount += prise
            dream.save()

            if dream.current_amount >= dream.target_amount:
                dream.status = 'completed'
                dream.save()

            return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['dream'] = get_object_or_404(Dream, id=self.kwargs['id'])
        return context




class TagAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Збираємо всі теги, фільтруючи їх за введеним значенням
        if not self.request.user.is_authenticated:
            return Tag.objects.none()

        qs = Tag.objects.all()

        if self.q:
            qs = qs.filter(name__icontains=self.q)  # Припускаємо, що у вас є поле "name" для тегів

        return qs

@csrf_exempt
def upload_image(request):

    if request.method == 'POST' and request.FILES.get('file'):
        file = request.FILES['file']
        path = default_storage.save(f'uploads/{file.name}', ContentFile(file.read()))
        return JsonResponse({'location': default_storage.url(path)})

    return JsonResponse({'error': 'File upload failed'}, status=400)


