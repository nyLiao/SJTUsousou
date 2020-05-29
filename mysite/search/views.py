from django.shortcuts import render
from haystack.generic_views import SearchView

# Create your views here.


def hello(request):
    return render(request, 'hello.html')


# class mySearchView(SearchView):
#     template_name = 'search/search.html'
#
#     def get(self, request, *args, **kwargs):
#         query = request.GET.get('q')
#         return super().get(request, *args, **kwargs)
