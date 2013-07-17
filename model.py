from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, create_engine, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, backref, scoped_session

engine = create_engine("sqlite:///ratings.db", echo=False)
session = scoped_session(sessionmaker(bind=engine,
                                      autocommit=False,
                                      autoflush = False))

Base = declarative_base()
Base.query = session.query_property()

### Class declarations go here
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String(64), nullable=True)
    password = Column(String(64), nullable=True)
    age = Column(Integer, nullable=True)
    zipcode = Column(String(15), nullable=True)
    gender = Column(String(1), nullable=True)
    occupation = Column(String(32), nullable=True)

    movie_ratings = relationship("Rating", backref=backref("users"))

class Rating(Base):
    __tablename__ = "ratings"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    movie_id = Column(Integer, ForeignKey('movies.movie_id'), nullable=False)
    movie_rating = Column(Integer, nullable=False)

    rater = relationship("User", backref=backref("ratings", order_by=id))


class Movie(Base):
    __tablename__ = "movies"

    movie_id = Column(Integer, primary_key=True)
    movie_title = Column(String(64), nullable=False)
    imdb_url = Column(String(128), nullable=True)
    release_date = Column(DateTime, nullable=True)

    # use rating class as association object
    ratings = relationship("Rating", backref="movies")




### End class declarations

def main():
    pass

if __name__ == "__main__":
    main()



###u.data = id(primary key), user_id, movie_id, movie_rating
###u.item = movie_id (primary key), movie_title, IMDB_url, release_date
###u.user = user_id(primary key), email_address, password, zip_code, gender=nullable age=nullable

# SQL ALCHEMY NOTES
# ========================
#  al = session.query(Movie).filter(Movie.movie_title.like('%Aladdin%')).all()
#  >>> for user in session.query(Movie).\
# ...       filter(Movie.release_date>=date1).\
# ...       filter(Movie.release_date<=date2):
# ...     print user.release_date
