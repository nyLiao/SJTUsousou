from django.shortcuts import render
from haystack.generic_views import SearchView
from haystack.query import SearchQuerySet

# Create your views here.


def hello(request):
    return render(request, 'hello.html')


class mySearchView(SearchView):
    template_name = 'search/search.html'
    # queryset = SearchQuerySet()

    # def get_queryset(self):
    #     queryset = super(SearchView, self).get_queryset()
    #     # further filter queryset based on some set of criteria
    #     return queryset
    #
    # def get_context_data(self, *args, **kwargs):
    #     context = super(SearchView, self).get_context_data(*args, **kwargs)
    #     # do something
    #     return context

    # def get(self, request, *args, **kwargs):
    #     query = request.GET.get('q')
    #     return super().get(request, *args, **kwargs)
