# -*- coding: utf-8 -*-
'''
    saltci.database.upgrades.versions.001_Initial_Schema
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Initial database layout.

    :codeauthor: :email:`Pedro Algarvio (pedro@algarvio.me)`
    :copyright: © 2012 by the SaltStack Team, see AUTHORS for more details.
    :license: Apache 2.0, see LICENSE for more details.
'''
import logging
from saltci.database import db
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import create_session
from migrate import *

# No need to change logger name bellow, unless you're after something specific
log = logging.getLogger('saltci.database.upgrades.{0}'.format(__name__.split('_', 1).pop(0)))

# Local declarative base
Model = declarative_base(name='Model')
metadata = Model.metadata


class SchemaVersion(Model):
    '''SQLAlchemy-Migrate schema version control table.'''

    __tablename__   = 'migrate_version'

    repository_id   = db.Column(db.String(250), primary_key=True)
    repository_path = db.Column(db.Text)
    version         = db.Column(db.Integer)

    def __init__(self, repository_id, repository_path, version):
        self.repository_id = repository_id
        self.repository_path = repository_path
        self.version = version


class Account(Model):
    __tablename__   = 'accounts'

    gh_id           = db.Column('github_id', db.Integer, primary_key=True)
    gh_login        = db.Column('github_login', db.String(100))
    gh_token        = db.Column('github_access_token', db.String(100), index=True)
    gravatar_id     = db.Column(db.String(32))
    hooks_token     = db.Column(db.String(32), index=True, default=lambda: uuid4().hex)
    locale          = db.Column(db.String(10), default=lambda: 'en')
    timezone        = db.Column(db.String(25), default=lambda: 'UTC')


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata

    # Bind the metadata to the migrate engine
    metadata.bind = migrate_engine

    # Let's get a session
    session = create_session(migrate_engine, autoflush=True, autocommit=False)

    # Let's create our tables
    if not migrate_engine.has_table(Account.__tablename__):
        log.info('Creating accounts table')
        Account.__table__.create(migrate_engine)


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.

    # Bind the metadata to the migrate engine
    metadata.bind = migrate_engine

    if migrate_engine.has_table(Accounts.__tablename__):
        log.info('Removing the accounts table')
        Account.__table__.drop(migrate_engine)
