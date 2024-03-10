from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///daycare.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

if __name__ == '__main__':
    app.run(debug=True)
class Facility(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    classrooms = db.relationship('Classroom', backref='facility', lazy=True)

class Classroom(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    capacity = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    facility_id = db.Column(db.Integer, db.ForeignKey('facility.id'), nullable=False)
    teachers = db.relationship('Teacher', backref='classroom', lazy=True)
    children = db.relationship('Child', backref='classroom', lazy=True)

class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    classroom_id = db.Column(db.Integer, db.ForeignKey('classroom.id'), nullable=False)

class Child(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    classroom_id = db.Column(db.Integer, db.ForeignKey('classroom.id'), nullable=False)

@app.route('/api/login', methods=['POST'])
def login():
    user = request.json['username']
    password = request.json['password']
    if user == "admin" and password == "admin":
        return jsonify({"message": "Login successful"}), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401

# Example CRUD for Facility (add similar for Classroom, Teacher, Child)
@app.route('/api/facilities', methods=['POST'])
def create_facility():
    name = request.json['name']
    new_facility = Facility(name=name)
    db.session.add(new_facility)
    db.session.commit()
    return jsonify({"message": "Facility created successfully"}), 201

@app.route('/api/facilities', methods=['GET'])
def get_facilities():
    facilities = Facility.query.all()
    return jsonify([{"id": facility.id, "name": facility.name} for facility in facilities]), 200

@app.route('/api/facilities/<int:id>', methods=['PUT'])
def update_facility(id):
    facility = Facility.query.get_or_404(id)
    facility.name = request.json['name']
    db.session.commit()
    return jsonify({"message": "Facility updated successfully"}), 200

@app.route('/api/facilities/<int:id>', methods=['DELETE'])
def delete_facility(id):
    facility = Facility.query.get_or_404(id)
    db.session.delete(facility)
    db.session.commit()
    return jsonify({"message": "Facility deleted successfully"}), 200
