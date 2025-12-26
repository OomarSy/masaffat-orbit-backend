from django_filters import FilterSet

class BaseFilterSet(FilterSet):
    extra_filters = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, filter_instance in getattr(self, 'extra_filters', {}).items():
            self.filters[name] = filter_instance

    @classmethod
    def add_filter(cls, name, filter_instance):
        if not hasattr(cls, 'extra_filters'):
            cls.extra_filters = {}
        cls.extra_filters[name] = filter_instance

