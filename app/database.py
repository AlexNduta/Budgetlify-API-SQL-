from sqlalchemy import create_engine
from sqlalchemy.ext/declarative import declarative_base
from sqlalchemy.orm import sesionmaker

# url to connect to the DB
SQLALCHEMY_DATABASE_URL = 'postgresql://was:123@localhost/Budgelify'

# engine is used to connect to the database
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# create a session that enables talking to the db
sessionLocal = sesionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
