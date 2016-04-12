from pyramid.renderers import get_renderer
from pyramid.view import view_config
from ..resources import Book

@view_config(
    renderer='templates/splash.pt',
    )
def splash_view(request):
    manage_prefix = request.registry.settings.get('substanced.manage_prefix',
                                                  '/manage')
    return {'manage_prefix': manage_prefix}

@view_config(
    context=Book,
    renderer='templates/book.pt',
    )
def document_view(context, request):
    return {'isbn': context.isbn,
            'title': context.title,
            'author': context.author,
            'publisher': context.publisher,
            'year': context.year,
            'master': get_renderer('templates/master.pt').implementation(),
           }

