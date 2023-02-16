from flask import Flask, request, render_template, url_for
from pymongo import MongoClient
import id_validate
import os, sys
from werkzeug.exceptions import HTTPException
import logging, json_logging
logging.basicConfig(level=logging.INFO, stream=sys.stdout, format='%(asctime)s %(levelname)s %(message)s')

app = Flask(__name__)

json_logging.init_flask(enable_json=True)
json_logging.init_request_instrument(app)


def db_connect():
    # Connection to MongoDB database
    MONGO_URI = os.environ.get('MONGO')
    client = MongoClient(str(MONGO_URI))
    db = client["portfolio"]
    collection = db["users"]
    return collection

def toDict(data):
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
    return clean_data

@app.route("/<option>")
def choice(option):
    return render_template(f"{option}.html"), 200

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html"), 200

@app.post('/add')
def add_employee():
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
        logging.info("Failed to add an employee")
        return "ID not valid", 404
    if any(char.isdigit() for char in f"{user_first_name},{user_last_name},{user_gender},{user_department}"):
        logging.info("Failed to add an employee")
        return "There's an invalid character in the input field", 404

    if not int(f"{user_phone_number}"):
        logging.info("Failed to add an employee")
        return "The phone number is not a valid number", 404
    if conn.find_one({"id": user_id}) is not None:
        logging.info("Failed to add an employee")
        return "User ID already exists", 404
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
    logging.info("Employee added successfully")
    return data, 200

@app.route('/search')
def get_employee():
    conn = db_connect()
    data = list(conn.find({}))
    clean_data = toDict(data)
    return render_template("search.html", data=clean_data), 200

@app.route('/employees')
def get_employees_info():
    conn = db_connect()
    data = list(conn.find({}))
    clean_data = toDict(data)
    return render_template("employees.html", data=clean_data), 200

@app.route('/update', methods=['GET', 'POST'])
def update_employee():
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
        if conn.find_one({'id': id}):
            conn.update_one({'id': id}, {"$set": {
                'first name': first_name,
                'last name': last_name,
                'address': address,
                'email': email,
                'date of birth': date_of_birth,
                'gender': gender,
                'department': department,
                'phone number': phone_number,
                'status': status}})
            logging.info("Employee's information was updated successfully")
            return 'Data updated', 200
        else:
            logging.info("Could not update employee")
            return "Could not find the employee specified. Please valdiate the legitimacy of the desired employee's ID"
    else:
        conn = db_connect()
        data = list(conn.find({}))
        clean_data = toDict(data)
        return render_template("update.html", data=clean_data), 200

@app.post('/upload')
def upload():
    conn = db_connect()
    file = request.files['file']
    data = file.read().decode()
    for i in data.split('\n'):
        i = i.split(',')
        if not id_validate.CheckID(i[0]):
            logging.info("Failed to upload file")
            return "Given ID's are not valid", 404
        if any(char.isdigit() for char in f"{i[1]},{i[2]},{i[6]},{i[7]}"):
            logging.info("Failed to upload file")
            return "There's a invalid character in the input field", 404

        if not int(f"{i[8]}"):
            logging.info("Failed to upload file")
            return "The phone number is not a valid number", 404
    
        if conn.find_one({"id": i[0]}) is not None:
            logging.info("Failed to upload file")
            return "User ID already exists", 404
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
        logging.info("Employee added successfully via file")
    return "The data was uploaded successfully!", 200

@app.post('/delete')
def delete_employee():
    conn = db_connect()
    id = request.form.get('id')
    if conn.find_one({'id': id}):
        conn.delete_one({'id': id})
    else:
        logging.info("Failed to delete employee")
        return "The user was not found", 404
    if conn.find_one({'id': id}):
        logging.info("Failed to delete employee")
        return "The employee could not be deleted", 500
    else:
        logging.info("Employee removed successfully")
        return "Employee was deleted successfully!", 200

@app.errorhandler(Exception)
def handle_exception(error):
    # pass through HTTP errors
    if isinstance(error, HTTPException):
        return error
    logging.critical("HTTP error has occurred in: %s", error)
    # now you're handling non-HTTP exceptions only
    return render_template("404.html", error=error)

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000, debug=False)