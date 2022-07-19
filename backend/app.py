from flask import Flask, request, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_cors import CORS, cross_origin 
from flask_swagger_ui import get_swaggerui_blueprint


app = Flask(__name__) #Flask class instance 
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:pgadmin@localhost/babytracker'
db = SQLAlchemy(app)

CORS(app,resources={r'/*': {'origins': 'http://localhost:5000'}}) #Cross-Origin Resource Sharing 

#Table
class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team_name = db.Column(db.String(100),nullable=False) 
    role_name = db.Column(db.String(100),nullable=False) 
    created_at = db.Column(db.DateTime,nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return F"Employee: {self.team_name}"

    def __init__(self,team_name,role_name):
        self.team_name = team_name,
        self.role_name = role_name


#Formater
def format_employee(employee):
    return{
        "team_name": employee.team_name,
        "role_name": employee.role_name,
        "id": employee.id,
        "created_at": employee.created_at
    }


#SWAGGER CONFIG
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "API_TEST"
    }
)
app.register_blueprint(swaggerui_blueprint,url_prefix=SWAGGER_URL)

#ENDPOINTS

#SWAGGER ENDPOINT
@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static',path)

#TEST
@app.route('/') #decorator
def hello():
    return 'hey!'

#Create Item
@app.route('/employees',methods =['POST']) #POST REQUEST employee
@cross_origin(origin='http://localhost:3000',headers=['Content- Type','Authorization'])
def created_employee():
    team_name = request.json['teamName'] #Grab request from json body
    role_name = request.json['roleName'] #Grab request from json body
    employee = Employee(team_name,role_name) #Var employee, pass 'team_name' to Employee class
    db.session.add(employee) 
    db.session.commit()
    return format_employee(employee) #return to frontend

#Get all items
@app.route('/employees',methods =['GET']) #GET REQUEST employee
@cross_origin()
def get_employees():
    employees = Employee.query.order_by(Employee.id.asc()).all()
    employee_list = []
    for employee in employees:
        employee_list.append(format_employee(employee))
    return {'employees': employee_list} #return to frontend

#Get single items
@app.route('/employees/<id>',methods =['GET']) #GET REQUEST employee
@cross_origin()
def get_employee(id):
    employees = Employee.query.filter_by(id=id).one()
    formated_employee = format_employee(employees)
    return {'employee': formated_employee} #return to frontend

#Get single items 2
@app.route('/employees_role/',methods =['GET']) #GET REQUEST employee
@cross_origin()
def employees_role():
    team_name = request.args.get("team_name")
    employees = Employee.query.filter_by(team_name=team_name).one()
    formated_employee = format_employee(employees)
    return {'employee': formated_employee} #return to frontend

if __name__ == '__main__':
    app.run()