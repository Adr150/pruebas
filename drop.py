import csv

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine("postgres://rzaakpzbspyfur:4cb6bef35b1a9f8f242206dc68132267df048c38590111606543c29a81195442@ec2-54-196-111-158.compute-1.amazonaws.com:5432/d2a0d7svr23q77")
db = scoped_session(sessionmaker(bind=engine))

def main():
    
    x = db.execute("DROP TABLE comments;")

    db.commit()

    print(x)
if __name__ == "__main__":
    main()

#CREATE TABLE books (isbn VARCHAR PRIMARY KEY NOT NULL,title VARCHAR NOT NULL,author VARCHAR NOT NULL,yearp INTEGER NOT NULL);")
        