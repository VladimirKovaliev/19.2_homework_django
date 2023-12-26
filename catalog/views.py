from django.forms import inlineformset_factory
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

from catalog.forms import ProductForm, VersionForm
from catalog.models import Product, Version


class ProductListView(ListView):
    model = Product
    template_name = 'catalog/index.html'


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        print(f'{name} ({email}): {message}')

    context = {
        'title': 'Контакты'
    }

    return render(request, 'catalog/contact.html', context)


class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'


class ProductCreateView(CreateView):
    # model = Product
    # fields = ('category', 'name', 'description', 'preview', 'price')
    # success_url = reverse_lazy('catalog:index')

    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:index')


class ProductUpdateView(LoginRequiredMixin, UpdateView):

    login_url = 'users:login'
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:index')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        version_formset = inlineformset_factory(Product, Version, form=VersionForm, extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = version_formset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = version_formset(instance=self.object)
        return context_data

    def form_valid(self, form):
        formset = self.get_context_data()['formset']
        self.object = form.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()

        return super().form_valid(form)


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    success_url = reverse_lazy('catalog:index')
    login_url = 'users:login'
