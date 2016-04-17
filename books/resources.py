"""
This module has the definitions for our content types. We define a book
folder, for storing books, and the book itself.
"""
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
    """
    **SubstanceD** make it easy to add custom columns to the contents
    listing. Here is where the extra columns are added. ``default_columnspec``
    contains the original columns used by **SubstanceD**. In this case, we add
    to them, but we could just as easily override them by omitting the default
    columns in the list that we return. Here, we simply get the book field
    values to display in the columns, but we could pass in a method to make
    some calculations and display those instead.
    """
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
    """
    Custom buttons can be added to the contents view as well. Original buttons
    are passed in the ``default_buttonspec`` parameter. As with columns, we
    have the option of not using them.
    """
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
    """
    This is a simple method to allow the ``NameSchemaNode`` from
    **SubstanceD** to detect if it shoud be in edit mode.
    """
    return request.registry.content.istype(context, 'BookFolder')


class BookFolderSchema(Schema):
    """
    **Substanced** schemas are defined using the **colander** library. Note
    the use of ``context_is_a_book_folder`` defined above.
    """
    name = NameSchemaNode(
        editing=context_is_a_book_folder,
        )
    title = colander.SchemaNode(
        colander.String(),
        )


class BookFolderPropertySheet(PropertySheet):
    """
    A property sheet turns a ``colander`` schema into a persistent form for
    storing content data.
    """
    schema = BookFolderSchema()

@content(
    'BookFolder',
    icon='glyphicon glyphicon-list-alt',
    add_view='add_book_folder',
    columns=book_columns,
    buttons=book_buttons,
)
class BookFolder(Folder):
    """
    Once we have our schema, we can use **SubstanceD**'s ``content`` decorator
    to define the content type. Notice how we pass in our custom columns and
    buttons here. The icon that will be used for the content type in the
    **SDI** is taken from **Glyphicons**. We only allow books to be added in a
    book folder, by setting ``__sdi_addable__`` to the allowed content types.
    """
    __sdi_addable__ = ('Book',)
    name = renamer()

    def __init__(self, name='', title=''):
        super(BookFolder, self).__init__()
        self.title = title

def context_is_a_book(context, request):
    """
    This is a simple method to allow the ``NameSchemaNode`` from
    **SubstanceD** to detect if it shoud be in edit mode.
    """
    return request.registry.content.istype(context, 'Book')

class Authors(colander.SequenceSchema):
    """
    A book can have multiple authors, so we use ``colander.SequenceSchema``
    here to store them, each in their own string field.
    """
    name = colander.SchemaNode(
        colander.String(),
        )

class BookSchema(Schema):
    """
    This is a very simple book schema, but will be enough for the demo.
    """
    isbn = NameSchemaNode(
        editing=context_is_a_book,
        )
    title = colander.SchemaNode(
        colander.String(),
        )
    author = Authors()
    publisher = colander.SchemaNode(
        colander.String(),
        missing='',
        )
    year = colander.SchemaNode(
        colander.Int(),
        missing=0,
        )

class BookPropertySheet(PropertySheet):
    """
    The book property sheet.
    """
    schema = BookSchema()

def maybe_add_book(context, request):
    """
    Instead of using a view name for the ``add_view`` parameter of the content
    definition. We can use a method to decide if the content can be added in
    the current container. If iot can, we return the name of the add view.
    """
    if request.registry.content.istype(context, 'BookFolder'):
        return 'add_book'


@content(
    'Book',
    icon='glyphicon glyphicon-book',
    add_view=maybe_add_book,
    )
class Book(Persistent):
    """
    Use the content decorator to define the book content type.
    """

    isbn = renamer()

    def __init__(self, isbn='', title='', author=(), publisher='', year=2000):
        self.title = title
        self.author = author
        self.publisher = publisher
        self.year = year


def includeme(config): # pragma: no cover
    """
    The ``includeme`` method is called at initialization time **if** this
    module is included using ``config.include``. We use it in this case for
    adding the property sheets for our content types.
    """
    config.add_propertysheet('Basic', BookFolderPropertySheet, BookFolder)
    config.add_propertysheet('Basic', BookPropertySheet, Book)
