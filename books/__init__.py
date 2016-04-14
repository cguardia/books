"""
This is the module where the application is initialized. No **SubstanceD**
tricks here. Other than the ``config`` calls to **SubstanceD** methods and
modules, this is just a regular **Pyramid** initialization.
"""
from pyramid.config import Configurator

from substanced.db import root_factory
from substanced.root import Root
from substanced.event import subscribe_created


def main(global_config, **settings):
    """
    This function returns a Pyramid WSGI application. Note that we first
    include **SubstanceD** itself, then do our own includes. Finally, we
    ``scan``, so that any decorators placed in our module code will be
    processed.
    """
    config = Configurator(settings=settings, root_factory=root_factory)
    config.include('substanced')
    config.include('.resources')
    config.scan()
    return config.make_wsgi_app()


@subscribe_created(Root)
def created(event):
    """
    We use **Pyramid**'s events to register a subscriber to the ``Root``
    object's creation event. This is for setting the **SDI** title and
    adding our catalog (see [[catalog.py]]).
    """
    root = event.object
    root.sdi_title = 'Simple Book Catalog'
    service = root['catalogs']
    service.add_catalog('books', update_indexes=True)
