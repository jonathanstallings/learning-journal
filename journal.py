# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime
import os

from pyramid.config import Configurator
from pyramid.view import view_config
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, DateTime, Integer, Unicode, UnicodeText
from waitress import serve


Base = declarative_base


class Entry(Base):
    __tablename__ = "entries"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(Unicode(127), nullable=False)
    text = Column(UnicodeText, nullable=False)
    created = Column(DateTime, nullable=False)

    def __repr__(self):
        return "Entry: {title} created at {date}".format(
            title=self.title, date=self.date
        )


@view_config(route_name='home', renderer='string')
def home(request):
    return "Hello World"


def main():
    """Create a configured wsgi app"""
    settings = {}
    debug = os.environ.get('DEBUG', True)
    settings['reload_all'] = debug
    settings['debug_all'] = debug
    # configuration setup
    config = Configurator(
        settings=settings
    )
    config.add_route('home', '/')
    config.scan()
    app = config.make_wsgi_app()
    return app


if __name__ == '__main__':
    app = main()
    port = os.environ.get('PORT', 5000)
    serve(app, host='0.0.0.0', port=port)
