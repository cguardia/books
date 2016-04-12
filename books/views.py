import isbnlib
from pyramid.httpexceptions import HTTPFound

from substanced.sdi import mgmt_view
from substanced.form import FormView
from substanced.interfaces import IFolder

from .resources import (
    BookSchema,
    BookFolderSchema,
)

@mgmt_view(
    context=IFolder,
    name='add_book',
    tab_title='Add Book',
    permission='sdi.add-content',
    renderer='substanced.sdi:templates/form.pt',
    tab_condition=False,
    )
class AddBookView(FormView):
    title = 'Add Book'
    schema = BookSchema()
    buttons = ('add',)

    def add_success(self, appstruct):
        registry = self.request.registry
        isbn = appstruct.pop('isbn')
        book = registry.content.create('Book', **appstruct)
        self.context[isbn] = book
        return HTTPFound(
            self.request.sdiapi.mgmt_path(self.context, '@@contents')
            )


@mgmt_view(
    context=IFolder,
    name='add_book_folder',
    tab_title='Add Book Folder',
    permission='sdi.add-content',
    renderer='substanced.sdi:templates/form.pt',
    tab_condition=False,
    )
class AddBookFolderView(FormView):
    title = 'Add Book'
    schema = BookFolderSchema()
    buttons = ('add',)

    def add_success(self, appstruct):
        registry = self.request.registry
        name = appstruct.pop('name')
        book_folder = registry.content.create('BookFolder', **appstruct)
        self.context[name] = book_folder
        return HTTPFound(
            self.request.sdiapi.mgmt_path(self.context, '@@contents')
            )

@mgmt_view(
    context=IFolder,
    content_type='BookFolder',
    name='contents',
    renderer='templates/add_book.pt',
    permission='sdi.manage-contents',
    request_method='POST',
    tab_condition=False,
    )
def prepare_add_book(context, request):
    isbn = request.POST.get('isbn', '')
    if isbn:
        if isbnlib.notisbn(isbn):
            request.session.flash('Not a valid ISBN: %s.' % isbn, 'danger')
        else:
            metadata = isbnlib.meta(isbn)
            if metadata:
                year = metadata['Year']
                if not year:
                    year = 0
                else:
                    year = int(year)
                book = request.registry.content.create('Book',
                    isbn,
                    metadata['Title'],
                    metadata['Authors'],
                    metadata['Publisher'],
                    year,
                )
                context[isbn] = book
                request.session.flash('Added book with ISBN: %s.' % isbn, 'success')
            else:
                request.session.flash('No data exists for ISBN: %s.' % isbn, 'danger')
        return HTTPFound(request.sdiapi.mgmt_path(context, '@@contents'))
    else:
        return {}
