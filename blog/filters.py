import django_filters
from .models import Post

class PostFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(field_name="title", lookup_expr="icontains")
    author_name = django_filters.CharFilter(field_name="author__name", lookup_expr="icontains")
    published_date = django_filters.DateFilter(field_name="published_date", lookup_expr="date")

    class Meta:
        model = Post
        fields = ["title", "author_name", "published_date"]
