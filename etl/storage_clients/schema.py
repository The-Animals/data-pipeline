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

    



    