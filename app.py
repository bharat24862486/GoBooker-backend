from flask import Flask, render_template, request,jsonify;
from flask_cors import CORS
from flask_pymongo import PyMongo
from bson import ObjectId

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb+srv://bharat:bharat@cluster0.rn63pja.mongodb.net/galaxy?retryWrites=true&w=majority"
app.config['SECRET_KEY'] = 'secret'

db = PyMongo(app).db

CORS(app)


def serialize_document(document):
    serialized = dict(document)
    serialized['_id'] = str(serialized['_id'])  # Convert ObjectId to string
    return serialized


 
@app.route('/movies', methods=['GET'])
def read():
    movies = db.movies.find()
    movies_arr=[]
    for i in movies:
        serialized_movies = serialize_document(i)
        movies_arr.append(serialized_movies)

    return jsonify(list(movies_arr))


@app.route('/single_movie/<ids>', methods=['GET'])
def single_movie(ids):
    movies = db.movies.find()
    movies_arr=[]
    for i in movies:
        serialized_movies = serialize_document(i)
        movies_arr.append(serialized_movies)

    arrs = list(movies_arr)
    for i in arrs:
        print(i["_id"])
        if i["_id"] == ids:
            return jsonify(i)
        

            

    return jsonify("Item not found")



@app.route('/single_movie_cinema/<name>', methods=['GET'])
def single_movie_cinema(name):
    cinema = db.cinema.find()
    param1 = request.args.get('param1')
    print(f"\n\n{param1}\n\n")
    cinema_arr=[]
    for i in cinema:
        serialized_movies = serialize_document(i)
        cinema_arr.append(serialized_movies)

    arrs = list(cinema_arr)
    arr1 = []
    for i in arrs:
        for j, movie_name in enumerate(i["movies"]):
            if movie_name == name:
                obj = {}
                obj["MovieName"] = movie_name
                obj["about_movie"] = i["about_movies"][j]
                obj["cinemaName"] = i["cinemaName"]
                obj["duration"] = i["duration"][j]
                obj["image"] = i["images"][j]
                obj["language"] = i["language"][j]
                obj["location"] = i["location"]
                obj["priceD"] = i["priceD"][j]
                obj["priceN"] = i["priceN"][j]
                obj["priceX"] = i["priceX"][j]
                obj["rating"] = i["rating"][j]
                obj["time"] = i["time"][j]

                arr1.append(obj)

    arr2=[]
    if param1:
        for i in arr1:
            if i["location"] == param1:
                arr2.append(i)

        return jsonify(arr2)
    return jsonify(arr1)


@app.route('/cinemas', methods=["GET"])
def get_cinema():
    cinema = db.cinema.find()
    cinema_arr=[]
    for i in cinema:
        serialized_movies = serialize_document(i)
        cinema_arr.append(serialized_movies)

    arrs = list(cinema_arr)
    return (arrs)


@app.route('/add_cinema', methods=["POST"])
def post_cinema():
    if request.method == "POST":
        data = request.get_json()
        cinema = db.cinema.find()
        cinema_arr=[]
        for i in cinema:
            serialized_movies = serialize_document(i)
            cinema_arr.append(serialized_movies)

        arrs = list(cinema_arr)
        for i in arrs:
            if i["cinemaName"] == data["cinemaName"]:
                return jsonify("This cinema is already present")
        
        db.cinema.insert_one(data)

        return jsonify("Cinema added successfully")


@app.route('/add_user',methods=["POST"])
def addUser():
    if request.method == "POST":
        data = request.get_json()

        all_users = db.users.find()
        users=[]
        for i in all_users:
            serialized_movies = serialize_document(i)
            users.append(serialized_movies)

        users2 = list(users)

        for i in users2:
            if i["Email"] == data["Email"]:
                return jsonify("User already exists")
            
        db.users.insert_one(data)

        return jsonify("User registered successfully")
    

@app.route('/get_user_by_Email', methods=["POST"])
def get_user_by_email():
    if request.method == "POST":
        data = request.get_json()

        isUser = db.users.find_one(data)

        if isUser:
            serialized_data = serialize_document(isUser)
            return jsonify(serialized_data)
        

    return jsonify("User did't found")




if __name__ == '__main__':
    app.run(debug=True)