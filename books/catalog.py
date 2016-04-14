"""
This module sets up a **Substance D** catalog for searching the books.
"""
from substanced.catalog import (
    catalog_factory,
    Text,
    Field,
    indexview,
    indexview_defaults,
    )


@catalog_factory('books')
class BookCatalogFactory(object):
    """
    The catalog factory will be called at initialization time and will create
    a catalog index for each book field.  We do not add an ``isbn`` field,
    because that's the book's id and it's handled by the system catalog.
    """
    title = Text()
    author = Field()
    publisher = Field()
    year = Field()


@indexview_defaults(catalog_name='books')
class BookCatalogViews(object):
    """
    The catalog views are used by the catalog to get the actual value that we
    want to store for each field. This allows us to examine the value before
    indexing and pass in a modified value if necessary. ``indexview_defaults``
    are for setting parameters that will be used in all the class views. Here,
    the views will be set for the catalog named ``books``. which is the one we
    created above.
    """
    def __init__(self, resource):
        self.resource = resource

    @indexview()
    def title(self, default):
        return getattr(self.resource, 'title', default)

    @indexview()
    def author(self, default):
        return getattr(self.resource, 'author', default)

    @indexview()
    def publisher(self, default):
        return getattr(self.resource, 'publisher', default)

    @indexview()
    def year(self, default):
        return getattr(self.resource, 'year', default)

    @indexview(catalog_name='system')
    def text(self, default):
        """
        Index views are overridable. We take advantage of this by creating our
        own text view for the system catalog, so that the filter search box in
        the **SDI** will use all the book's fields for searching.
        """
        isbn = getattr(self.resource, 'isbn', '')
        title = getattr(self.resource, 'title', '')
        author = getattr(self.resource, 'author', '')
        author = ' '.join(author)
        publisher = getattr(self.resource, 'publisher', '') 
        year = str(getattr(self.resource, 'year', ''))
        return ' '.join((isbn, title, author, publisher, year))
