import wtforms


class Filter:
    def get_form_field(self, query):
        raise NotImplementedError

    def filter(self, items, value):
        raise NotImplementedError


# pylint: disable=abstract-method
class SearchFilter(Filter):
    def get_form_field(self):
        return wtforms.TextField()


class FieldFilter(Filter):
    def get_form_field(self):
        choices = [('', 'All'), *list(self.get_choices())]
        return wtforms.SelectField(choices=choices)

    def get_choices(self):
        raise NotImplementedError


class Controller:
    def __init__(self, filters=None, per_page=100):
        self.filters = filters if filters is not None else {}
        self.per_page = per_page

    # {{{ Filter Interface
    def get_filter_form(self):
        class FilterForm(wtforms.Form):
            for key, filter_ in self.filters.items():
                vars()[key] = filter_.get_form_field()
                del key, filter_
        return FilterForm

    def get_filters(self, params):
        return [
            (self.filters[key], value)
            for key, value in params.items()
            if value and key in self.filters
        ]
    # }}}

    # {{{ View Interface
    def get_items(self, page=1, order_by=None, filters=None):
        """Return a paginated list of columns."""
        raise NotImplementedError

    def get_item(self, pk):
        """Return a entry with PK."""
        raise NotImplementedError

    def create_item(self, form):
        """Create a new entry in the storage."""
        raise NotImplementedError

    def update_item(self, item, form):
        """Update a entry in storage."""
        raise NotImplementedError

    def delete_item(self, item):
        """Delete a new entry in storage."""
        raise NotImplementedError
    # }}}
