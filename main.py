from flask import Flask, request, render_template, url_for
from pymongo import MongoClient
import id_validate
import os

app = Flask(__name__)

def db_connect():
    # Connection to MongoDB database
    MONGO_URI = os.getenv('MONGO')
    client = MongoClient(f'{MONGO_URI}')
    db = client["portfolio"]
    collection = db["users"]
    return collection

@app.route('/health')
def health():
    return "OK!",200

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html"), 200

@app.route("/<option>")
def choice(option):
    return render_template(f"{option}.html"), 200

@app.post('/add')
def adduser():
    conn = db_connect()
    status = request.form.get("status")
    user_id = request.form.get("user_id")
    user_first_name = request.form.get("user_first_name")
    user_last_name = request.form.get("user_last_name")
    user_address = request.form.get("user_address")
    user_email = request.form.get("user_email")
    user_date_of_birth = request.form.get("user_date_of_birth")
    user_gender = request.form.get("user_gender")
    user_department = request.form.get("user_department")
    user_phone_number = request.form.get("user_phone_number")
    
    if not id_validate.CheckID(user_id):
        return "ID not valid", 404
    if any(char.isdigit() for char in f"{user_first_name},{user_last_name},{user_gender},{user_department}"):
        return "There's a invalid character in the input field", 404

    if not int(f"{user_phone_number}"):
        return "The phone number is not a valid number", 404
    if conn.find_one({"id": user_id}) is not None:
        return "User ID already exists", 404
    data = [ user_id, user_first_name, user_last_name, user_address, user_email, user_date_of_birth, user_gender, user_department, user_phone_number ]
    data = {
        "id": user_id,
        "first name": user_first_name,
        "last name": user_last_name,
        "address": user_address,
        "email": user_email,
        "date of birth": user_date_of_birth,
        "gender": user_gender,
        "department": user_department,
        "phone number": user_phone_number,
        "status": status
    }
    conn.insert_one(
   {
      "id": user_id,
      "first name": user_first_name,
      "last name": user_last_name,
      "address": user_address,
      "email": user_email,
      "date of birth": user_date_of_birth,
      "gender": user_gender,
      "department": user_department,
      "phone number": user_phone_number,
      "status": status
   }) 
   # Insert data to mongodb collection
    return data, 200

@app.route('/search')
def getuser():
    conn = db_connect()
    data = list(conn.find({}))
    clean_data = []
    for i in data:
        cleanest = []
        cleanest.append(i["id"])
        cleanest.append(i["first name"])
        cleanest.append(i["last name"])
        cleanest.append(i["address"])
        cleanest.append(i["email"])
        cleanest.append(i["date of birth"])
        cleanest.append(i["gender"])
        cleanest.append(i["department"])
        cleanest.append(i["phone number"])
        cleanest.append(i["status"])
        clean_data.append(cleanest)
    return render_template("search.html", data=clean_data), 200

@app.route('/employees')
def getbatch():
    conn = db_connect()
    data = list(conn.find({}))
    clean_data = []
    for i in data:
        cleanest = []
        cleanest.append(i["id"])
        cleanest.append(i["first name"])
        cleanest.append(i["last name"])
        cleanest.append(i["address"])
        cleanest.append(i["email"])
        cleanest.append(i["date of birth"])
        cleanest.append(i["gender"])
        cleanest.append(i["department"])
        cleanest.append(i["phone number"])
        cleanest.append(i["status"])
        clean_data.append(cleanest)
    return render_template("employees.html", data=clean_data), 200

@app.route('/update', methods=['GET', 'POST'])
def updateuser():
    if request.method == 'POST':
        conn = db_connect()
        id = request.form['id']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        address = request.form['address']
        email = request.form['email']
        date_of_birth = request.form['date_of_birth']
        gender = request.form['gender']
        department = request.form['department']
        phone_number = request.form['phone_number']
        status = request.form['status']
        conn.update_one({'id': id}, {"$set": {
            'first name': first_name,
            'last name': last_name,
            'address': address,
            'email': email,
            'date of birth': date_of_birth,
            'gender': gender,
            'department': department,
            'phone number': phone_number,
            'status': status
        }})
        return 'Data updated', 200
    else:
        conn = db_connect()
        data = list(conn.find({}))
        clean_data = []
        for i in data:
            cleanest = []
            cleanest.append(i["id"])
            cleanest.append(i["first name"])
            cleanest.append(i["last name"])
            cleanest.append(i["address"])
            cleanest.append(i["email"])
            cleanest.append(i["date of birth"])
            cleanest.append(i["gender"])
            cleanest.append(i["department"])
            cleanest.append(i["phone number"])
            cleanest.append(i["status"])
            clean_data.append(cleanest)
        print(clean_data)
        return render_template("update.html", data=clean_data), 200

@app.post('/upload')
def upload():
    conn = db_connect()
    file = request.files['file']
    data = file.read().decode()
    for i in data.split('\n'):
        i = i.split(',')
        if not id_validate.CheckID(i[0]):
            return "Given ID's are not valid"
        if any(char.isdigit() for char in f"{i[1]},{i[2]},{i[6]},{i[7]}"):
            return "There's a invalid character in the input field", 404

        if not int(f"{i[8]}"):
            return "The phone number is not a valid number", 404
    
        if conn.find_one({"id": i[0]}) is not None:
            return "User ID already exists", 401
        conn.insert_one(
            {
                "id": i[0],
                "first name": i[1],
                "last name": i[2],
                "address": i[3],
                "email": i[4],
                "date of birth": i[5],
                "gender": i[6],
                "department": i[7],
                "phone number": i[8],
                "status": i[9]
            })
    return "The data was uploaded successfully!", 200

@app.post('/delete')
def deleteuser():
    conn = db_connect()
    id = request.form.get('id')
    conn.delete_one({'id': id})
    return "Document deleted successfully!", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000, debug=False)