from pyramid.config import Configurator

from substanced.db import root_factory
from substanced.root import Root
from substanced.event import subscribe_created

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings, root_factory=root_factory)
    config.include('substanced')
    config.include('.resources')
    config.scan()
    return config.make_wsgi_app()

@subscribe_created(Root)
def created(event):
    root = event.object
    root.sdi_title = 'Simple Book Catalog'
    service = root['catalogs']
    service.add_catalog('books', update_indexes=True)
