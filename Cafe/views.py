from django.shortcuts import render
from django.views import View, generic
from .models import *
from django.http import HttpResponse, HttpResponseRedirect

# Create your views here.
items = []


class Home(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'Cafe/home.html')


class About(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'Cafe/aboutttt.html')


class ContactUs(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'Cafe/Contact.html')


class Menu(generic.ListView):
    template_name = 'Cafe/menu.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['menu_items'] = MenuItem.objects.all()
        return context
    queryset = get_context_data
    context_object_name = "info"

    def post(self, request, *args, **kwargs):
        item = [MenuItem.objects.get(name__exact=request.POST['item']), int(request.POST['number'])]
        items.append(item)
        print(items)

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class OrderList(View):
    def get(self, request, *args, **kwargs):
        tables = Table.objects.filter(status=0)
        return render(request, 'Cafe/order_list.html', {'tables': tables, 'items': items})

    def post(self, request, *args, **kwargs):
        table = int(request.POST['table'])
        if table:
            order = Order.objects.create(
                table_id=table
            )
            for item in items:
                OrderMenuItem.objects.create(
                    order_id_id=order.id,
                    menu_item_id_id=item[0].id,
                    quantity=item[1]
                )
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
