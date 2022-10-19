from django.core.exceptions import ValidationError
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, get_object_or_404, render
from django.views.generic import ListView, DetailView, CreateView, TemplateView
from django.urls import reverse_lazy
from django.db.models import Count, Sum, F, Min, Q

from sklad.mixin import DataMixin, SuperUserRequiredMixin
from sklad.forms import *
from sklad.tasks import send_email_to_buyer
from sklad.utils import decode, make_qrcode


# TODO:
# Fix dublicate code in (shipment_add, delivery_add) Views
# Fix dublicate Nomenclature items in documents - Done
# Fix create null document - Done


class IndexView(LoginRequiredMixin, DataMixin, ListView):
    """"Веб сервис отображающий главную страницу, с последними заявками на
    отгрузку (поставку) товара."""

    model = Document
    template_name = 'sklad/index.html'
    context_object_name = 'documents'
    extra_context = {'title': 'Заявки на поставку/отгрузку'}
    login_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context()
        context = dict(list(context.items()) + list(c_def.items()))
        context['search_form'] = SearchForm(data=self.request.GET)
        return context

    def get_query_search(self):
        return self.request.GET.get('search', '')

    def get_status(self):
        status = self.request.GET.get('status')
        status = (status, ) if status else Status
        return status

    def get_queryset(self):
        query = self.get_query_search()
        status = self.get_status()
        return Document.objects.filter(
            Q(vendor__name__icontains=query) | Q(buyer__fio__icontains=query)
        ).filter(status__in=status).order_by('-time_create')


class DeliveryListView(SuperUserRequiredMixin, IndexView):
    """"Веб сервис для работы с заявками на поставку."""
    extra_context = {
        'left_menu': [
            {'url_name': 'delivery_add', 'title': 'Создать заявку'}
        ],
        'title': 'Заявки на поставку',
    }

    def get_queryset(self):
        query = self.get_query_search()
        status = self.get_status()
        return Document.objects.filter(
            vendor__isnull=False).filter(
            vendor__name__icontains=query).filter(
            status__in=status).order_by('-time_create')


class ShipmentListView(SuperUserRequiredMixin, IndexView):
    """"Веб сервис для работы с заявками."""
    extra_context = {
        'left_menu': [
            {'url_name': 'shipment_add', 'title': 'Создать заявку'}
        ],
        'title': 'Заявки на отгрузку',
    }

    def get_queryset(self):
        query = self.get_query_search()
        status = self.get_status()
        return Document.objects.filter(
            buyer__isnull=False).filter(
            buyer__fio__icontains=query).filter(
            status__in=status).order_by('-time_create')


class DocumentView(LoginRequiredMixin, DataMixin, DetailView):
    """" Веб сервис для работы с заявкой
    на поставку/отгрузку (отображение карточки) """

    model = Document
    template_name = 'sklad/document.html'
    context_object_name = 'document'
    login_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Информация по заявке")
        context = dict(list(context.items()) + list(c_def.items()))
        context['qrcode'] = make_qrcode(self.object.pk)

        # Select Sum(price * amount), Min(store.amount - amount)
        # for document.nomenclatures
        context['total'] = self.object.nomenclatures.aggregate(
            sum=Sum(F('documentnomenclatures__amount') * F('price')),
            min=Min(F('store__amount') - F('documentnomenclatures__amount'))
        )

        # Select price * amount, amount, store.amount
        # for each document.nomenclatures
        context['result'] = self.object.nomenclatures.annotate(
            total=F('documentnomenclatures__amount') * F('price'),
            amount=F('documentnomenclatures__amount'),
            store_amount=F('store__amount')
        )
        return context


class NomenclatureListView(SuperUserRequiredMixin, DataMixin, ListView):
    """"Веб сервис для работы с номенклатурой
    (отображение, поиск, добавление)."""

    model = Nomenclature
    template_name = 'sklad/nomenclature_list.html'
    context_object_name = 'nomenclatures'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Номенклатура")
        context = dict(list(context.items()) + list(c_def.items()))
        context['subcats'] = SubCategory.objects.annotate(total=Count(
            'nomenclature')
        ).filter(total__gt=0).order_by('category__name', 'name')
        context['search_form'] = SearchForm(data=self.request.GET)
        return context

    def get_queryset(self):
        query = self.request.GET.get('search', '')
        return Nomenclature.objects.filter(name__icontains=query).annotate(
            store_amount=F('store__amount')).order_by(
            'subcategory__category__name',
            'subcategory__name',
            'name'
        )


class BuyerListView(SuperUserRequiredMixin, DataMixin, ListView):
    """"Веб сервис для работы с покупателями"""

    model = Buyer
    template_name = 'sklad/contactor_list.html'
    context_object_name = 'buyers'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context()
        context = dict(list(context.items()) + list(c_def.items()))
        context['left_menu'] = [
            {'url_name': 'buyer_add', 'title': 'Создать покупателя'}
        ]
        context['title'] = 'Покупатели'
        return context


class VendorListView(SuperUserRequiredMixin, DataMixin, ListView):
    """"Веб сервис для работы с поставщиками"""

    model = Vendor
    template_name = 'sklad/contactor_list.html'
    context_object_name = 'vendors'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Главная страница")
        context = dict(list(context.items()) + list(c_def.items()))
        context['left_menu'] = [
            {'url_name': 'vendor_add', 'title': 'Создать поставщика'}
        ]
        context['title'] = 'Поставщики'
        return context


class CategoryBase(SuperUserRequiredMixin, DataMixin, ListView):
    model = Nomenclature
    template_name = 'sklad/nomenclature_list.html'
    context_object_name = 'nomenclatures'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context()
        context = dict(list(context.items()) + list(c_def.items()))
        context['subcats'] = SubCategory.objects.annotate(total=Count(
            'nomenclature')
        ).filter(total__gt=0).order_by('category__name', 'name')
        context['search_form'] = SearchForm(data=self.request.GET)
        return context


class CategoryView(CategoryBase):
    """"Веб сервис для работы с номенклатурой
    (отображение, фильтрация) в зависимости от выбранной категории."""

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Category.objects.get(pk=self.kwargs['pk']).name
        return context

    def get_queryset(self):
        query = self.request.GET.get('search', '')
        return Nomenclature.objects.filter(
            subcategory__category=self.kwargs['pk']
        ).filter(name__icontains=query).annotate(
            store_amount=F('store__amount')).order_by(
            'subcategory__name',
            'name'
        )


class SubCategoryView(CategoryBase):
    """"Веб сервис для работы с номенклатурой
      (отображение, фильтрация) в зависимости от выбранной подкатегории."""

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = SubCategory.objects.get(pk=self.kwargs['pk']).name
        return context

    def get_queryset(self):
        query = self.request.GET.get('search', '')
        return Nomenclature.objects.filter(
            Q(subcategory=self.kwargs['pk'])).filter(Q(name__icontains=query)
        ).annotate(store_amount=F('store__amount')).order_by('name')


class NomenclatureView(SuperUserRequiredMixin, DataMixin, DetailView):
    """"Веб сервис для работы с номенклатурой
      (отображение карточки)"""

    model = Nomenclature
    template_name = 'sklad/nomenclature.html'
    context_object_name = 'nomenclature'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="")
        context = dict(list(context.items()) + list(c_def.items()))

        subcategories = SubCategory.objects.filter(
            category=self.object.subcategory.category)

        context['subcategories'] = subcategories

        context['store'], _ = Store.objects.get_or_create(
            nomenclature=self.object)

        nomenclatures = Nomenclature.objects.filter(
            subcategory__in=subcategories)

        context['total_category'] = Store.objects.filter(
            nomenclature__in=nomenclatures).aggregate(
            sum=Sum(F('nomenclature__price') * F('amount'))).get('sum')

        return context


class BuyerView(SuperUserRequiredMixin, DataMixin, DetailView):
    """"Веб сервис для работы с покупателем
      (отображение карточки)"""

    model = Buyer
    template_name = 'sklad/details_contactor.html'
    context_object_name = 'buyer'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Сведения о покупателе")
        context = dict(list(context.items()) + list(c_def.items()))
        context['left_menu'] = [
            {'url_name': 'buyer_add', 'title': 'Создать покупателя'}
        ]
        context['documents'] = Document.objects.filter(
            buyer=self.object).order_by('-time_create')
        return context


class VendorView(SuperUserRequiredMixin, DataMixin, DetailView):
    """"Веб сервис для работы с покупателем
      (отображение карточки)"""

    model = Vendor
    template_name = 'sklad/details_contactor.html'
    context_object_name = 'vendor'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Сведения о поставщике")
        context = dict(list(context.items()) + list(c_def.items()))
        context['left_menu'] = [
            {'url_name': 'vendor_add', 'title': 'Создать поставщика'}
        ]
        context['documents'] = Document.objects.filter(
            vendor=self.object).order_by('-time_create')

        return context


class NomenklatureAddView(SuperUserRequiredMixin, DataMixin, CreateView):
    """"Веб сервис для добавления номенклатуры. """

    form_class = NomenklatureAddForm
    template_name = 'sklad/nomenclature_add.html'
    success_url = reverse_lazy('nomenclature_list')
#    login_url = reverse_lazy('home')
    raise_exception = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Добавление номенклатуры')
        return dict(list(context.items()) + list(c_def.items()))


class BuyerAddView(SuperUserRequiredMixin, DataMixin, CreateView):
    """"Веб сервис для добавления покупателя. """

    form_class = BuyerAddForm
    template_name = 'sklad/contactor_add.html'
    success_url = reverse_lazy('buyer_list')
#    login_url = reverse_lazy('home')
    raise_exception = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Добавление покупателя')
        context['left_menu'] = [
            {'url_name': 'buyer_add', 'title': 'Создать покупателя'}
        ]
        return dict(list(context.items()) + list(c_def.items()))


class VendorAddView(SuperUserRequiredMixin, DataMixin, TemplateView):
    """"Веб сервис для добавления поставщика. """

    template_name = 'sklad/vendor_add.html'
    success_url = reverse_lazy('vendor_list')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Добавление поставщика')
        context['left_menu'] = [
            {'url_name': 'vendor_add', 'title': 'Создать поставщика'}
        ]
        context['bank_details_form'] = BankDetailsAddForm()
        context['vendor_form'] = VendorAddForm()
        return dict(list(context.items()) + list(c_def.items()))

    def post(self, request, *args, **kwargs):
        bank_details_form = BankDetailsAddForm(request.POST)
        vendor_form = VendorAddForm(request.POST)
        if bank_details_form.is_valid() or vendor_form.is_valid():
            bd_form = bank_details_form.save(commit=False)
            bank_details_form.save()
            v_form = vendor_form.save(commit=False)
            v_form.bank_details = bd_form
            vendor_form.save()
        return redirect(self.success_url)


class DeliveryAddView(SuperUserRequiredMixin, DataMixin, TemplateView):
    """"Веб сервис для создания заявки на поставку. """

    template_name = 'sklad/document_add.html'
    success_url = reverse_lazy('delivery_list')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Создание заяки на поставку')
        context['document_add_form'] = DeliveryAddForm()
        context['document_nomenclature_form_set'] = DocumentNomenclaturesFormSet()
        return dict(list(context.items()) + list(c_def.items()))

    def post(self, request, *args, **kwargs):
        document_add_form = DeliveryAddForm(request.POST)
        document_nomenclature_form_set = DocumentNomenclaturesFormSet(
            data=request.POST
        )
        if document_add_form.is_valid() or document_nomenclature_form_set.is_valid():
            print(document_add_form.is_valid())
            document = Document(
                vendor=document_add_form.cleaned_data.get('contactor')
            )

            # Generate valid nomenclatures list
            nomenclatures = []
            for form in document_nomenclature_form_set:
                print(form.is_valid())
                try:
                    nomenclature = DocumentNomenclatures(
                        **form.cleaned_data,
                        document=document
                    )
                    nomenclature.full_clean(exclude=['document'])
                    nomenclatures.append(nomenclature)
                except ValidationError:
                    print('Error')

            if nomenclatures:
                document.save()

                # Merge dublicate nomenclature item
                nomenclatures_dict = dict()
                for n in nomenclatures:
                    if n.nomenclature in nomenclatures_dict:
                        nomenclatures_dict[n.nomenclature].amount += n.amount
                    else:
                        nomenclatures_dict[n.nomenclature] = n

                [nomenclature.save() for nomenclature in nomenclatures_dict.values()]
            else:
                document_add_form.add_error(
                    None,
                    'Укажите корректные данные для номенклатуры'
                )
                context = self.get_context_data(*args, **kwargs)
                context['document_add_form'] = document_add_form
                context['document_nomenclature_form_set'] = document_nomenclature_form_set
                return self.render_to_response(context)

        return redirect(self.success_url)


class ShipmentAddView(SuperUserRequiredMixin, DataMixin, TemplateView):
    """"Веб сервис для создания заявки на отгрузку. """

    template_name = 'sklad/document_add.html'
    success_url = reverse_lazy('shipment_list')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Создание заявки на отгрузку')
        context['document_add_form'] = ShipmentAddForm()
        context['document_nomenclature_form_set'] = DocumentNomenclaturesFormSet()
        return dict(list(context.items()) + list(c_def.items()))

    def post(self, request, *args, **kwargs):
        document_add_form = ShipmentAddForm(request.POST)
        document_nomenclature_form_set = DocumentNomenclaturesFormSet(
            data=request.POST
        )
        if document_add_form.is_valid() or document_nomenclature_form_set.is_valid():
            print(document_add_form.is_valid())
            document = Document(
                buyer=document_add_form.cleaned_data.get('contactor')
            )

            # Generate valid nomenclatures list
            nomenclatures = []
            for form in document_nomenclature_form_set:
                print(form.is_valid())
                try:
                    nomenclature = DocumentNomenclatures(
                        **form.cleaned_data,
                        document=document
                    )
                    nomenclature.full_clean(exclude=['document'])
                    nomenclatures.append(nomenclature)
                except ValidationError:
                    print('Error')

            if nomenclatures:
                document.save()

                # Merge dublicate nomenclature item
                nomenclatures_dict = dict()
                for n in nomenclatures:
                    if n.nomenclature in nomenclatures_dict:
                        nomenclatures_dict[n.nomenclature].amount += n.amount
                    else:
                        nomenclatures_dict[n.nomenclature] = n

                [nomenclature.save() for nomenclature in nomenclatures_dict.values()]
            else:
                document_add_form.add_error(
                    None,
                    'Укажите корректные данные для номенклатуры'
                )
                context = self.get_context_data(*args, **kwargs)
                context['document_add_form'] = document_add_form
                context['document_nomenclature_form_set'] = document_nomenclature_form_set
                return self.render_to_response(context)

        return redirect(self.success_url)


class LoginUser(DataMixin, LoginView):
    """ Веб сервис для авторизации. """

    form_class = LoginUserForm
    template_name = 'sklad/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизация")
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')


class ConfirmView(DataMixin, TemplateView):
    """ Веб сервис для подтвеждения заказа покупателем """

    template_name = 'sklad/document_confirm.html'
    context_object_name = 'document'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Подтвеждение получения товара")
        return dict(list(context.items()) + list(c_def.items()))

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        code = request.POST.get('code')
        if not code:
            raise Http404
        document_id = decode(code)
        d = get_object_or_404(Document, pk=document_id)
        context['document_id'] = document_id
        if d.status != Status.COLLECTED:
            raise Http404
        d.status = Status.FINISHED
        d.save()
        return self.render_to_response(context)

    def get(self, request, *args, **kwargs):
        code = request.GET.get('code')
        if not code:
            raise Http404
        context = self.get_context_data(**kwargs)
        document_id = decode(code)
        get_object_or_404(Document, pk=document_id)
        context['document_id'] = document_id
        return self.render_to_response(context)


def logout_user(request):
    """ Выход пользователя из аккаунта """

    logout(request)
    return redirect('login')


class UpdateStatusDocumentView(DocumentView):
    """ Веб сервис для обновления статуса заказа отгрузки """

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Информация по заявке")
        context = dict(list(context.items()) + list(c_def.items()))
        return context

    def get(self, request, *args, **kwargs):
        super().get(self, request, *args, **kwargs)

        status = self.kwargs.get('status')
        document_id = self.kwargs.get('pk')

        if status not in Status:
            raise Http404("Status code is not founded")

        if self.object.status in (Status.FINISHED, status):
            raise Http404("Can't change Status code")

        self.object.status = status
        self.object.save()

        if self.object.vendor is not None:
            if status in (Status.FINISHED, ):
                # Add nomenclatures amount to Store
                for item in DocumentNomenclatures.objects.filter(document=self.object):
                    Store.objects.filter(nomenclature=item.nomenclature).update(
                        amount=F('amount') + item.amount
                    )

        if self.object.buyer is not None:
            if status in (Status.CANCELED, Status.COLLECTED):
                send_email_to_buyer.delay(document_id, status)

            if status in (Status.COLLECTED):
                # Sub nomenclatures amount to Store (Reserve)
                for item in DocumentNomenclatures.objects.filter(document=self.object):
                    Store.objects.filter(nomenclature=item.nomenclature).update(
                        amount=F('amount') - item.amount
                    )
        return redirect(reverse('document', args={document_id: document_id}))


# For Ajax TEST

from django.http import JsonResponse


def ajax_view(request):
    context = {}
    return render(request, 'sklad/ajax.html', context=context)


def search_result(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        res = None
        series = request.POST.get('series')
        query_se = Nomenclature.objects.filter(name__icontains=series)
        print('Is AJAX')
        if len(query_se) > 0 and len(series) > 0:
            data = []
            for pos in query_se:
                item = {
                    'url': pos.get_absolute_url(),
                    'name': pos.name,
                }
                data.append(item)
            res = data
        else:
            res = 'No Nomenclature found'
        print(res)
        return JsonResponse({'data': res})
    print({}, request.headers)
    return JsonResponse({})
