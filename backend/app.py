#from crypt import methods
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__) #Flask class instance 
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:pgadmin@localhost/babytracker'
db = SQLAlchemy(app)
CORS(app)

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(100),nullable=False) 
    created_at = db.Column(db.DateTime,nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return F"Event: {self.description}"

    def __init__(self,description):
        self.description = description

def format_event(event):
    return{
        "description": event.description,
        "id": event.id,
        "created_at": event.created_at
    }

@app.route('/') #decorator
def hello():
    return 'hey!'

#Create Item
@app.route('/events',methods =['POST']) #POST REQUEST event
def created_event():
    description = request.json['description'] #Grab request from json body
    event = Event(description) #Var event, pass 'description' to Event class
    db.session.add(event) 
    db.session.commit()
    return format_event(event) #return to frontend

#Get all items
@app.route('/events',methods =['GET']) #POST REQUEST event
def get_events():
    events = Event.query.order_by(Event.id.asc()).all()
    event_list = []
    for event in events:
        event_list.append(format_event(event))
    return {'events': event_list} #return to frontend

#Get single items
@app.route('/events/<id>',methods =['GET']) #POST REQUEST event
def get_event(id):
    events = Event.query.filter_by(id=id).one()
    formated_event = format_event(events)
    return {'event': formated_event} #return to frontend


if __name__ == '__main__':
    app.run()