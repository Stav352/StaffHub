#!/bin/bash
# E2E tests:
success=0
function purge(){
	docker exec -it db mongosh -u root -p root --authenticationDatabase admin portfolio --eval "db.users.deleteMany({})"
}
purge
test1=$(curl app)
expected_result1='''<!DOCTYPE HTML>
<HTML>
  <head>
    <title>Employee Management</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.7.2/css/all.css" integrity="sha384-fnmOCqbTlWIlj8LyTjo7mOUStjsKC4pOpQbqyi7RrhN7udi9RwhKkMHpvLbHG9Sr" crossorigin="anonymous">
    <link rel=stylesheet type=text/css href="/static/index.css">
  </head>
  <body>
      <div class="container">
          <h2>Employee Management</h2>
          <div class="button" onclick="window.location.href = '/employees'"><i class="fas fa-users"></i> Employees Info</div> <!-- Views all employees -->
          <div class="button" onclick="window.location.href = '/add'"><i class="fas fa-user-plus"></i> Add an employee</div> <!-- Adds a specific employee -->
          <div class="button" onclick="window.location.href = '/delete'"><i class="fas fa-user-minus"></i> Delete an employee</div> <!-- Removes a specific employee -->
          <div class="button" onclick="window.location.href = '/upload'"><i class="fas fa-upload"></i> Upload </div> <!-- Imports employees file from a csv format -->
          <div class="button" onclick="window.location.href = '/update'"><i class="fas fa-edit"></i> Edit </div> <!-- Updates a specific employee information -->
          <div class="button" onclick="window.location.href = '/search'"><i class="fas fa-search"></i> Search </div> <!-- Searches for a specific employee -->
        </div>
  </body>
</html>'''
if echo "$test1" | grep -q "$expected_result1"
then
    ((success=$success+1))
else
    echo "Failed Test #1 - Could not curl to app on port 80"
    exit 1
fi
test2=$(curl --location --request POST 'app/add' \
--form 'user_id="314833203"' \
--form 'user_first_name="Stav"' \
--form 'user_last_name="Nahum"' \
--form 'user_address="Example"' \
--form 'user_email="stav352@gmail.com"' \
--form 'user_date_of_birth="26-09-1999"' \
--form 'user_gender="Male"' \
--form 'user_department="DevOps"' \
--form 'user_phone_number="0528349868"' \
--form 'status="active"')
expected_result2='{"address":"Example","date of birth":"26-09-1999","department":"DevOps","email":"stav352@gmail.com","first name":"Stav","gender":"Male","id":"314833203","last name":"Nahum","phone number":"0528349868","status":"active"}'
if echo "$test2" | grep -q "$expected_result2"
then
    ((success=$success+1))
else
    echo "Failed Test #2 - Could not add an employee to the database."
    exit 1
fi
test3="curl --location --request GET 'app/employees'"
expected_result3='<!DOCTYPE html>
<html>
  <head>
    <meta charset="UTF-8">
    <title>Employee Data</title>
    <link rel=stylesheet type=text/css href="/static/employees.css">
  </head>
  <body>
    <input type="reset" value="Back to Home" onClick="window.location.href='/'" />
    <h1>Employee Data</h1>
    <table>
      <tr>
        <th>ID</th>
        <th>First Name</th>
        <th>Last Name</th>
        <th>Address</th>
        <th>Email</th>
        <th>Date of Birth</th>
        <th>Gender</th>
        <th>Department</th>
        <th>Phone Number</th>
        <th>Status</th>
      </tr>

        <tr>
          <td>314833203</td>
          <td>Stav</td>
          <td>Nahum</td>
          <td>Example</td>
          <td>stav352@gmail.com</td>
          <td>26-09-1999</td>
          <td>Male</td>
          <td>DevOps</td>
          <td>0528349868</td>
          <td>active</td>
        </tr>

    </table>
  </body>
</html>'
if echo "$test3" | grep -q "$expected_result3"
then
    ((success=$success+1))
else
    echo "Failed Test #3 - Could not get employees information."
    exit 1
fi
test4=$(curl --location --request POST 'app/upload' \
--form 'file=@"./TestingEmployees.csv"')
expected_result4="The data was uploaded successfully"
if echo "$test4" | grep -q "$expected_result4"
then
    ((success=$success+1))
else
    echo "Failed Test #4 - Could not upload emplyees data file."
    exit 1
fi

test5=$(curl --location --request POST 'app/update' \
--form 'id="314833203"' \
--form 'first_name="Stav"' \
--form 'last_name="Nahum"' \
--form 'address="Testing"' \
--form 'email="stav352@gmail.com"' \
--form 'date_of_birth="26-09-1999"' \
--form 'gender="male"' \
--form 'department="QA"' \
--form 'phone_number="0123456789"' \
--form 'status="active"')
expected_result5="Data updated"

if echo "$test5" | grep -q "$expected_result5"
then
    ((success=$success+1))
else
    echo "Failed Test #5 - Could not update employee information."
    exit 1
fi

test6=$(curl --location --request POST 'app/delete' \
--form 'id="314833203"')
expected_result6="Employee was deleted successfully!"
if echo "$test6" | grep -q "$expected_result6"
then
    ((success=$success+1))
else
    echo "Failed Test #6 - Could not delete an employee."
    exit 1
fi
if [ $1 ]; then
  purge
fi
if [ $? -eq 0 ]
then
	echo "Success !"
    echo ${success}/6
else
	echo " Failure :(..."
fi

