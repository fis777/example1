from django.db import models
from django.db.models import Q


class Product(models.Model):
    categories = models.ManyToManyField(Category,
                                        related_name='products',
                                        blank=True, verbose_name=u"категории")
    related_products = models.ManyToManyField('Product',
                                              blank=True,
                                              verbose_name="связанные продукты")

    sku = models.CharField(u'артикул', max_length=128, validators=[validators.check_bad_symbols], unique=True)

    price = models.DecimalField(u'цена', max_digits=12, decimal_places=4)

    slug = models.SlugField(u'slug', max_length=80, db_index=True, unique=True)

    name = models.CharField(u'название', max_length=128)
    title = models.CharField(u'заголовок страницы (<title>)', max_length=256, blank=True)
    description = models.TextField(u'описание', blank=True)


def live_search(request, template_name="shop/livesearch_results.html"):
    from django.core import serializers
    from django.http import HttpResponse

    q = request.GET.get("q", "")
    qs = Product.objects.filter(Q(sku__icontains=q) | Q(name__icontains=q) | Q(description__icontains=q)).all()

    try:
        json = serializers.serialize("json", list(qs))
    except Exception:
        json = serializers.serialize("json", [])
        return HttpResponse(json, content_type='application/json')


# или

def live_search(request, template_name="shop/livesearch_results.html"):
    from django.http import JsonResponse

    q = request.GET.get("q", "")
    qs = Product.objects.filter(Q(sku__icontains=q) | Q(name__icontains=q) | Q(description__icontains=q)).all()
    return JsonResponse(qs, safe=False)
