from flask import Flask, render_template, redirect, request
import model

app = Flask(__name__)


# log in as user
# view list of all users
@app.route("/")
def index():
    user_list = model.session.query(model.User).limit(5).all()
    return render_template("user_list.html", users=user_list)

@app.route("/index_error")
def index_error():
    user_list = model.session.query(model.User).limit(5).all()
    return render_template("user_list_error.html", users=user_list)

# create new user
@app.route("/new_user")
def new_user():
    return render_template("new_user.html")


# for a user, get a list of movies rated plus ratings given
@app.route("/user_profile")
def view_profile():
    user_id = request.args.get("id")
    current_user = model.session.query(model.User).get(user_id)
    user_ratings = current_user.movie_ratings
    movies_rated = []
    for rating in user_ratings:
        movie = model.session.query(model.Movie).get(rating.movie_id)
        movies_rated.append(movie)
    return render_template("user_profile.html", current_user=current_user, user_ratings=user_ratings, movie_ratings=movie_ratings)

@app.route("/login")
def login():
    user_email = request.args.get("email")
    user_password = request.args.get("password")
    current_user = model.session.query(model.User).filter(model.User.email == user_email).one() # user object
    #check to see if user_password == current_user.password
    if user_password == current_user.password:
        user_id = current_user.id
        return redirect('/user_profile?id=' + str(user_id))
    else:
        return redirect('/index_error')



@app.route("/add_user")
def add_user():
    new_email = request.args.get("email")
    new_password = request.args.get("password")
    new_gender = request.args.get("gender")
    new_age = request.args.get("age")
    new_occupation = request.args.get("occupation")
    new_zip_code = request.args.get("zip_code")

    user = model.User(email=new_email, password=new_password, gender=new_gender, age=int(new_age), occupation=new_occupation, zipcode=new_zip_code)
    model.session.add(user)
    model.session.commit()

    return redirect('/user_profile?id=' + str(user.id))


# view record for movie, click to add or update personal rating


if __name__ == "__main__":
    app.run(debug=True)
