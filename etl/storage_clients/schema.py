from sqlalchemy import *

class DbSchema:

    _metadata = MetaData()

    mlas = Table('mlas', _metadata,
        Column('Id', Integer, primary_key=True, autoincrement=True),
        Column('RidingNumber', Integer),
        Column('RidingName', Text),
        Column('Title', Text),
        Column('FirstName', Text),
        Column('LastName', Text),
        Column('HansardName', Text),
        Column('Caucus', Text),
        Column('LegislativePhoneNumber', Text),
        Column('RidingPhoneNumber', Text),
        Column('Email', Text)
    )

    documents = Table('documents', _metadata,
        Column('Id', Integer, primary_key=True, autoincrement=True),
        Column('DateCode', Text),
        Column('DateString', Text),
        Column('Date', Text),
        Column('Url', Text)
    )

    ranks = Table('ranks', _metadata,
        Column('Id', Integer, primary_key=True, autoincrement=True),
        Column('Rank', Integer),
        Column('Sentence', Text),
        Column('DocumentId', Integer, ForeignKey("documents.Id")),
        Column('MLAId', Integer, ForeignKey("mlas.Id"))
    )

    comparison = Table('mlacomparision', _metadata,
        Column('Id', Integer, primary_key=True, autoincrement=True),
        Column('MLAId', Integer, ForeignKey('mlas.Id')),
        Column('MostSimilar', Integer, ForeignKey('mlas.Id')),
        Column('LeastSimilar', Integer, ForeignKey('mlas.Id'))
    )

    images = Table('images', _metadata,
        Column('Id', Integer, primary_key=True, autoincrement=True),
        Column('LastName', Text),
        Column('URL', Text)
    )
