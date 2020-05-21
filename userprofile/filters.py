from rest_framework import filters

# Enables user to dynamically select search fields
class DynamicSearchFilters(filters.SearchFilter):
    def get_search_fields(self, view, request):
        return request.GET.getlist("search_fields", [])