import colander

from persistent import Persistent

from substanced.content import content
from substanced.folder import Folder
from substanced.property import PropertySheet
from substanced.schema import (
    Schema,
    NameSchemaNode
    )
from substanced.util import renamer


def book_columns(folder, subobject, request, default_columnspec):

    return default_columnspec + [
        {'name': 'Title',
         'value': getattr(subobject, 'title', None),
         },
        {'name': 'Author',
         'value': getattr(subobject, 'author', None),
         },
        {'name': 'Publisher',
         'value': getattr(subobject, 'publisher', None),
         },
        {'name': 'Year',
         'value': getattr(subobject, 'year', None),
         },
    ]

def book_buttons(context, request, default_buttonspec):
    return default_buttonspec + [
            {'type': 'single',
             'buttons': [{'id': 'fromisbn',
                          'name': 'fromisbn',
                          'class': 'btn-primary btn-sdi-act',
                          'value': 'fromisbn',
                          'text': 'Add Book using ISBN Database'},
                          ]},
            ]

def context_is_a_book_folder(context, request):
    return request.registry.content.istype(context, 'BookFolder')

class BookFolderSchema(Schema):
    name = NameSchemaNode(
        editing=context_is_a_book_folder,
        )
    title = colander.SchemaNode(
        colander.String(),
        )

class BookFolderPropertySheet(PropertySheet):
    schema = BookFolderSchema()

@content(
    'BookFolder',
    icon='glyphicon glyphicon-list-alt',
    add_view='add_book_folder',
    columns=book_columns,
    buttons=book_buttons,
)
class BookFolder(Folder):

    __sdi_addable__ = ('Book',)
    name = renamer()

    def __init__(self, name='', title=''):
        super(BookFolder, self).__init__()
        self.title = title

def context_is_a_book(context, request):
    return request.registry.content.istype(context, 'Book')

class Authors(colander.SequenceSchema):
    name = colander.SchemaNode(
        colander.String(),
        )

class BookSchema(Schema):
    isbn = NameSchemaNode(
        editing=context_is_a_book,
        )
    title = colander.SchemaNode(
        colander.String(),
        )
    author = Authors()
    publisher = colander.SchemaNode(
        colander.String(),
        missing=colander.null,
        )
    year = colander.SchemaNode(
        colander.Int(),
        missing=colander.null,
        )

class BookPropertySheet(PropertySheet):
    schema = BookSchema()

def maybe_add_book(context, request):
    if request.registry.content.istype(context, 'BookFolder'):
        return 'add_book'

@content(
    'Book',
    icon='glyphicon glyphicon-book',
    add_view=maybe_add_book,
    )
class Book(Persistent):

    isbn = renamer()

    def __init__(self, isbn='', title='', author=(), publisher='', year=2000):
        self.title = title
        self.author = author
        self.publisher = publisher
        self.year = year

def includeme(config): # pragma: no cover
    config.add_propertysheet('Basic', BookFolderPropertySheet, BookFolder)
    config.add_propertysheet('Basic', BookPropertySheet, Book)
