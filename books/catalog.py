from substanced.catalog import (
    catalog_factory,
    Text,
    Field,
    )

@catalog_factory('books')
class BookCatalogFactory(object):
    title = Text()
    author = Field()
    publisher = Field()
    year = Field()

from substanced.catalog import (
    indexview,
    indexview_defaults,
    )

@indexview_defaults(catalog_name='books')
class BookCatalogViews(object):
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
        isbn = getattr(self.resource, 'isbn', '')
        title = getattr(self.resource, 'title', '')
        author = getattr(self.resource, 'author', '')
        author = ' '.join(author)
        publisher = getattr(self.resource, 'publisher', '') 
        year = str(getattr(self.resource, 'year', ''))
        return ' '.join((isbn, title, author, publisher, year))
