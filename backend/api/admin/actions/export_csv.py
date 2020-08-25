import csv
import json
import operator
from datetime import datetime
from functools import reduce
from io import BytesIO
from zipfile import ZipFile

import requests
from django.conf import settings
from django.db.models import Q
from django.http import HttpResponse

from api.models import Factory, GovAgency
from docxtpl import DocxTemplate


class ExportCsvMixin:

    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(
            meta)
        response.write(u'\ufeff'.encode('utf8'))
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = '輸出成 csv 檔'
