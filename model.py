from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, create_engine, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, backref, scoped_session
import correlation

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
    # ratings

    def similarity(self, other_user):
        d = {}
        rating_pairs = []
        for self_rating in self.ratings:
            d[self_rating.movie_id] = self_rating.movie_rating

        for other_user_rating in other_user.ratings:
            if (other_user_rating.movie_id in d) == True:
                rating_pairs.append((other_user_rating.movie_rating, d.get(other_user_rating.movie_id)))
        if rating_pairs:
            return correlation.pearson(rating_pairs)
        else:
            return 0.0

    def make_prediction(self, movie_id):
        ratings = self.ratings
        other_ratings = session.query(Rating).filter_by(movie_id=movie_id).all()
        other_users = []
        
        other_u_rating = []

        for r in other_ratings:
            other_users.append(r.rater)
            other_u_rating.append(r.movie_rating)

        correlation_tuples = []

        for i in range(len(other_users)):
            sim = self.similarity(other_users[i])
            rating = other_u_rating[i]
            correlation_tuples.append((sim, rating))

        #s = sorted(correlation_tuples, key=lambda i: i[1], reverse=True)
        numerator = sum([rating * sim for sim, rating in correlation_tuples])
        denominator = sum([correlation_tuples[0] for correlation_tuple in correlation_tuples])
        return numerator/denominator

        # best_match_tuple = s[0]     
        # best_match_id = best_match_tuple[0]
        # coefficient = best_match_tuple[1]
        # best_match_rating = session.query(Rating).filter_by(user_id=best_match_id, movie_id=movie_id).one()
        
        # return coefficient * best_match_rating.movie_rating


class Rating(Base):
    __tablename__ = "ratings"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    movie_id = Column(Integer, ForeignKey('movies.movie_id'), nullable=False)
    movie_rating = Column(Integer, nullable=False)

    rater = relationship("User", backref=backref("ratings", order_by=id))

    # movie


class Movie(Base):
    __tablename__ = "movies"

    movie_id = Column(Integer, primary_key=True)
    movie_title = Column(String(64), nullable=False)
    imdb_url = Column(String(128), nullable=True)
    release_date = Column(DateTime, nullable=True)

    # use rating class as association object
    ratings = relationship("Rating", backref="movie")




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
