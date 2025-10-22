from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine('mysql+pymysql://app_book_tales:1234@localhost/book_tales_db')
Base = declarative_base()
Session = sessionmaker(bind=engine)
