import django_filters
from shop.models import Product, Category


class CategoryFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name="name", lookup_expr="icontains")

    class Meta:
        model = Category
        fields = ["name"]


class ProductFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(
        field_name="category__id", lookup_expr="iexact"
    )
    name = django_filters.CharFilter(field_name="name", lookup_expr="icontains")

    class Meta:
        model = Product
        fields = ["category"]