import csv

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine("postgres://rzaakpzbspyfur:4cb6bef35b1a9f8f242206dc68132267df048c38590111606543c29a81195442@ec2-54-196-111-158.compute-1.amazonaws.com:5432/d2a0d7svr23q77")
db = scoped_session(sessionmaker(bind=engine))

def main():

    x = 0

    f = open("books.csv")
    reader = csv.reader(f)
    for isbn, title, author, yearp in reader:
        db.execute("INSERT INTO books (isbn, title,author, yearp) VALUES (:isbn,:title,:author,:yearp)",
                   {"isbn": isbn, "title": title, "author": author, "yearp": (yearp)})
        x=x+1
        print(f"Agregamos {x} filas")
    db.commit()

    
    

    
if __name__ == "__main__":
    main()