from django.core.exceptions import ValidationError
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import redirect, get_object_or_404, render
from django.views.generic import ListView, DetailView, CreateView, TemplateView
from django.urls import reverse_lazy
from django.db.models import Count, Sum, F, Min, Q

from app.core.mixin import DataMixin, SuperUserRequiredMixin
from sklad.forms import *
from app.core.forms import *
from app.document.tasks import send_email_to_buyer
from app.core.utils import decode, make_qrcode


# TODO:
# Fix dublicate code in (shipment_add, delivery_add) Views
# Fix dublicate Nomenclature items in documents - Done
# Fix create null document - Done









