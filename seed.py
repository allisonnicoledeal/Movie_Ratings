import model
import csv
import datetime

def load_users(session):
    # use u.user
    with open('./seed_data/u.user') as csvfile:
        userreader = csv.reader(csvfile, delimiter="|")
        for row in userreader:
            newuser = model.User(id=int(row[0]), age=int(row[1]), gender=row[2], occupation=row[3], zipcode=row[4])
            session.add(newuser)
            session.commit()


def load_movies(session):
    # use u.item
    with open('./seed_data/u.item') as csvfile:
        moviereader = csv.reader(csvfile, delimiter="|")
        for row in moviereader:
            if row[1] != "unknown":
                title = row[1]
                title = title.decode("latin-1")
                r_date = row[2].split("-")
                months = {"Jan": "01", "Feb": "02", "Mar": "03", "Apr": "04", "May": "05", "Jun": "06", "Jul": "07", "Aug": "08", "Sep": "09", "Oct": "10", "Nov": "11", "Dec": "12"}
                r_date_datetime = datetime.date(int(r_date[2]), int(months[r_date[1]]), int(r_date[0]))
                new_movie = model.Movie(movie_id=int(row[0]), movie_title=title, imdb_url=row[3], release_date=r_date_datetime)
                session.add(new_movie)
                session.commit()


def load_ratings(session):
    # use u.data
    with open('./seed_data/u.data') as csvfile:
        ratingreader = csv.reader(csvfile, delimiter="\t")
        for row in ratingreader:
            new_rating = model.Rating(user_id=int(row[0]), movie_id=int(row[1]), movie_rating=int(row[2]))
            session.add(new_rating)
            session.commit()


def main(session):
    # You'll call each of the load_* functions with the session as an argument
    load_users(session)
    load_movies(session)
    load_ratings(session)

if __name__ == "__main__":
    s= model.connect()
    main(s)
