# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime
import os

from cryptacular.bcrypt import BCRYPTPasswordManager
import markdown
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.config import Configurator
from pyramid.httpexceptions import (HTTPFound, HTTPNotFound,
                                    HTTPMethodNotAllowed)
from pyramid.security import remember, forget
from pyramid.view import view_config
import sqlalchemy as sa
from sqlalchemy.exc import DBAPIError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from waitress import serve
from zope.sqlalchemy import ZopeTransactionExtension

HERE = os.path.dirname(os.path.abspath(__file__))

DATABASE_URL = os.environ.get(
    'DATABASE_URL',
    'postgresql://jonathan@localhost:5432/learning-journal'
)

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))

Base = declarative_base()


class Entry(Base):
    __tablename__ = "entries"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    title = sa.Column(sa.Unicode(127), nullable=False)
    text = sa.Column(sa.UnicodeText, nullable=False)
    created = sa.Column(
        sa.DateTime, nullable=False, default=datetime.datetime.utcnow
    )

    def __repr__(self):
        return "Entry: {title} created at {date}".format(
            title=self.title, date=self.created
        )

    def __json__(self, request):
        return {
            'id': self.id,
            'title': self.title,
            'text': self.text,
            'created': self.created.isoformat(),
            'markdown': self.markdown
        }

    @classmethod
    def all(cls, session=None):
        if session is None:
            session = DBSession
        return session.query(cls).order_by(cls.created.desc()).all()

    @classmethod
    def newest(cls, session=None):
        if session is None:
            session = DBSession
        return session.query(cls).order_by(cls.created.desc()).first()

    @classmethod
    def by_id(cls, id_, session=None):
        if session is None:
            session = DBSession
        return session.query(cls).filter(cls.id == id_).first()

    @classmethod
    def write(cls, title=None, text=None, session=None):
        if session is None:
            session = DBSession
        instance = cls(title=title, text=text)
        session.add(instance)
        return instance

    @classmethod
    def update(cls, id_=None, title=None, text=None):
        instance = cls.by_id(id_)
        instance.title = title
        instance.text = text
        return instance

    @classmethod
    def delete(cls, id_, session=None):
        if session is None:
            session = DBSession
        instance = cls.by_id(id_)
        session.delete(instance)

    @property
    def markdown(self):
        return markdown.markdown(
            self.text,
            extensions=['codehilite', 'fenced_code'],
            ouput_format="html5"
        )


def init_db():
    engine = sa.create_engine(DATABASE_URL, echo=False)
    Base.metadata.create_all(engine)


def do_login(request):
    username = request.params.get('username', None)
    password = request.params.get('password', None)
    if not (username and password):
        raise ValueError('both username and password are required')

    settings = request.registry.settings
    manager = BCRYPTPasswordManager()
    if username == settings.get('auth.username', ''):
        hashed = settings.get('auth.password', '')
        return manager.check(hashed, password)
    return False


@view_config(
    route_name='home',
    request_method='GET',
    xhr=True,
    renderer='json'
)
@view_config(route_name='home', renderer='templates/list.jinja2')
def list_view(request):
    entries = Entry.all()
    return {'entries': entries}


@view_config(route_name='about', renderer='templates/about.jinja2')
def about_view(request):
    return {}


@view_config(route_name='detail', renderer='templates/detail.jinja2')
def detail_view(request):
    entry_id = int(request.matchdict.get('id', -1))
    entry = Entry.by_id(entry_id)
    if entry is None:
        return HTTPNotFound()
    return {'entry': entry}


@view_config(
    route_name='edit',
    request_method='POST',
    xhr=True,
    renderer='json'
)
@view_config(
    route_name='edit',
    request_method='GET',
    xhr=True,
    renderer='json'
)
@view_config(
    route_name='edit',
    request_method='POST',
    renderer='templates/edit.jinja2'
)
@view_config(
    route_name='edit',
    request_method='GET',
    renderer='templates/edit.jinja2'
)
def edit_view(request):
    if not request.authenticated_userid:
        return HTTPFound(request.route_url('login'))

    entry_id = int(request.matchdict.get('id', -1))
    entry = Entry.by_id(entry_id)
    if request.method == 'POST':
        title = request.params.get('title')
        text = request.params.get('text')
        Entry.update(id_=entry_id, title=title, text=text)
        if 'HTTP_X_REQUESTED_WITH' in request.environ:
            return {'entry': entry}
        return HTTPFound(request.route_url('detail', id=entry_id))
    elif request.method == 'GET':
        if entry is None:
            return HTTPNotFound()
        return {'entry': entry}
    else:
        return HTTPMethodNotAllowed()


@view_config(
    route_name='delete',
    request_method='POST',
    xhr=True,
    renderer='json'
)
@view_config(
    route_name='delete',
    request_method='POST',
    renderer='templates/edit.jinja2'
)
def del_entry(request):
    if not request.authenticated_userid:
        return HTTPFound(request.route_url('login'))

    entry_id = int(request.matchdict.get('id', -1))
    if request.method == 'POST':
        Entry.delete(entry_id)
        return HTTPFound(request.route_url('home'))
    else:
        return HTTPMethodNotAllowed()


@view_config(
    route_name='add',
    request_method='POST',
    xhr=True,
    renderer='json'
)
@view_config(
    route_name='add',
    request_method='POST')
@view_config(
    route_name='create',
    request_method='GET',
    xhr=True, renderer='json'
)
@view_config(
    route_name='create',
    request_method='GET',
    renderer='templates/create.jinja2'
    )
def add_entry(request):
    if not request.authenticated_userid:
        return HTTPFound(request.route_url('login'))

    if request.method == 'POST':
        title = request.params.get('title')
        text = request.params.get('text')
        Entry.write(title=title, text=text)
        if 'HTTP_X_REQUESTED_WITH' in request.environ:
            return {}
        return HTTPFound(request.route_url('home'))
    elif request.method == 'GET':
        if 'HTTP_X_REQUESTED_WITH' in request.environ:
            newest = Entry.newest()
            return {'new_entry': newest}
        return {}
    else:
        return HTTPMethodNotAllowed()


@view_config(context=DBAPIError)
def db_exception(context, request):
    from pyramid.response import Response
    response = Response(context.message)
    response.status_int = 500
    return response


@view_config(route_name='login', renderer="templates/login.jinja2")
def login(request):
    """authenticate a user by username/password"""
    username = request.params.get('username', '')
    error = ''
    if request.method == 'POST':
        error = "Login Failed"
        authenticated = False
        try:
            authenticated = do_login(request)
        except ValueError as e:
            error = str(e)

        if authenticated:
            headers = remember(request, username)
            return HTTPFound(request.route_url('home'), headers=headers)

    return {'error': error, 'username': username}


@view_config(route_name='logout')
def logout(request):
    headers = forget(request)
    return HTTPFound(request.route_url('home'), headers=headers)


def main():
    """Create a configured wsgi app"""
    settings = {}
    debug = os.environ.get('DEBUG', True)
    settings['reload_all'] = debug
    settings['debug_all'] = debug
    settings['auth.username'] = os.environ.get('AUTH_USERNAME', 'admin')
    manager = BCRYPTPasswordManager()
    settings['auth.password'] = os.environ.get(
        'AUTH_PASSWORD', manager.encode('secret')
    )
    if not os.environ.get('TESTING', False):
        # only bind the session if we are not testing
        engine = sa.create_engine(DATABASE_URL)
        DBSession.configure(bind=engine)
    # add a secret value for auth tkt signing
    auth_secret = os.environ.get('JOURNAL_AUTH_SECRET', 'itsaseekrit')
    # and add a new value to the constructor for our Configurator:
    config = Configurator(
        settings=settings,
        authentication_policy=AuthTktAuthenticationPolicy(
            secret=auth_secret,
            hashalg='sha512'
        ),
        authorization_policy=ACLAuthorizationPolicy(),
    )
    config.include('pyramid_tm')
    config.include('pyramid_jinja2')
    config.add_static_view('static', os.path.join(HERE, 'static'))
    config.add_route('home', '/')
    config.add_route('about', '/about')
    config.add_route('detail', '/detail/{id}')
    config.add_route('edit', '/edit/{id}')
    config.add_route('delete', '/delete/{id}')
    config.add_route('create', '/create')
    config.add_route('add', '/add')
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')
    config.scan()
    app = config.make_wsgi_app()
    return app


if __name__ == '__main__':
    app = main()
    port = os.environ.get('PORT', 5000)
    serve(app, host='0.0.0.0', port=port)
