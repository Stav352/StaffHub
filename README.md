
# Employee Management

This project is an employees' management platform that aims to streamline the process of managing your team members' information.


## Architecture

![App Screenshot](https://i.imgur.com/Lgc0DFe.png)


## licenses
[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)
[![GPLv3 License](https://img.shields.io/badge/License-GPL%20v3-yellow.svg)](https://opensource.org/licenses/)
[![AGPL License](https://img.shields.io/badge/license-AGPL-blue.svg)](http://www.gnu.org/licenses/agpl-3.0)

## Tech Stack

**Containerization:** Docker, Kubernetes

**Package Manager**: Helm

**Frontend:** HTML, CSS and JS

**Backend:** Flask and MongoDB

**Logging:** Elasticsearch, Fluentd and Kibana

**Monitoring:** Prometheus and Grafana stack

**CI/CD:** GitHub Actions, ArgoCD

**Cloud Provider:** AWS
## 🔗 Links
[![linkedin](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/stav-nahum-810091207/)


## FAQ

#### What is the purpose of this app?

This app is intended to provide a user-friendly and efficient way to manage employee records and data.

#### How do I add a new employee?

To add a new employee, you can either fill in the fields on the “Add Employee” page or upload a csv file containing the employee information on the “Upload” page. 

#### How do I update an employee’s information?

You can update an employee’s information by entering their employee ID and the updated information on the “Update Employee” page.

#### How do I find an employee’s information?

You can look up an employee’s information by entering their employee ID on the “Search” page.

#### How do I view all the current employees?

You can view all the current employees by navigating to the “Employees” page.
## Run Locally

```bash
  git clone https://github.com/Stav352/Portfolio-application.git \
  pushd Portfolio-application \ 
  docker compose up -d 
```

- Note: Make sure to add .mongoenv and .appenv files for the MongoDB and Flask application communications.

## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`MONGO` Connection string that Flask uses to connect to MongoDB

`MONGO_ROOT_USERNAME` Username for MongoDB

`MONGO_ROOT_PASSWORD` Password for MongoDB

## Support

For support, email Stav@example.com.
## Roadmap

- Add more API methods
- Study and integrate AWS Secret Manager for MongoDB secrets
- Study and integrate KEDA for Event-driven Kubernetes Autoscaling