from flask import Flask, render_template, redirect, request, session
# import flask.ext.login
import model


app = Flask(__name__)

Flask.secret_key = "THE_KEY"


@app.route("/")
def index():
    user_list = model.session.query(model.User).limit(5).all()
    return render_template("user_list.html", users=user_list)


@app.route("/index_error")
def index_error():
    user_list = model.session.query(model.User).limit(5).all()
    return render_template("user_list_error.html", users=user_list)


@app.route("/login", methods=["GET", "POST"])
def login():
    # form = flask.ext.login.LoginForm()
    # if form.validate_on_submit():
    user_email = request.args.get("email")
    user_password = request.args.get("password")
    current_user = model.session.query(model.User).filter(model.User.email == user_email).one()  # user object
    #check to see if user_password == current_user.password
    if user_password == current_user.password:
        session['user_id'] = current_user.id
        return redirect('/user_profile?id=' + str(current_user.id))
    else:
        return redirect('/index_error')

# @app.route("/login_check")
# def login_check():
#     if request.args.get("id") in session:
#         return True
#     return False

# create new user
@app.route("/new_user")
def new_user():
    return render_template("new_user.html")


# for a user, get a list of movies rated plus ratings given
@app.route("/user_profile")
def view_profile():
    user_id = request.args.get("id")
    current_user = model.session.query(model.User).get(user_id)
    print "USER RATINGS:", current_user.ratings
    return render_template("user_profile.html", current_user=current_user)


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
@app.route("/movie")
def view_movie():
    movie_id = request.args.get("movie_id")
    movie = model.session.query(model.Movie).get(movie_id)
    user_id = session['user_id']
    values = [0, 1, 2, 3, 4, 5]
    rating_value = values[0]
    for rating in movie.ratings:
        if (rating.user_id == int(user_id)):
            rating_value = rating.movie_rating

    return render_template("movie.html", movie=movie, user_id=user_id, values = values, rating_value=rating_value)


@app.route("/rate_movie")
def rate_movie():
    movie_id = request.args.get("movie_id")
    movie_rating = request.args.get("value")
    user_id = session['user_id']
    user = model.session.query(model.User).get(user_id)
    ratings = user.ratings
    for rating in ratings:
        movie_id = int(movie_id)
        if rating.movie_id == movie_id:
            rating.movie_rating = movie_rating
            model.session.add(rating)
            model.session.commit()
            return redirect('/movie?movie_id=' +str(movie_id))
    rating = model.Rating(user_id=user_id, movie_id=movie_id, movie_rating=movie_rating)
    model.session.add(rating)
    model.session.commit()
    return redirect('/movie?movie_id=' +str(movie_id))


@app.before_request
def before_request():
    print "REQUEST:", request.path
    request_paths = ["/", "/favicon.ico"]
    if request.path not in request_paths:
        if 'user_id' not in session:
            return redirect('/')    



if __name__ == "__main__":
    app.run(debug=True)
