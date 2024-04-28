from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import text
from sqlalchemy.orm import relationship
from flask_cors import CORS  # Import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})  # Adjust as needed
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///daycare.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Facility(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    # classrooms = relationship("Classroom", back_populates="facility")


class Classroom(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    capacity = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    facility_id = db.Column(db.Integer, db.ForeignKey(id), nullable=False)

    # teachers = relationship("Teacher", back_populates="classroom")
    # children = relationship("Child", back_populates="classroom")
    # facility = relationship("Facility", back_populates="classrooms")

    def can_enroll_child(self):
        # Each teacher can supervise up to 10 children.
        # Children can be enrolled if there are enough teachers to supervise them up to the classroom capacity.
        max_children_allowed = 10 * len(self.teachers)
        return len(self.children) < min(self.capacity, max_children_allowed)


class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    room = db.Column(db.Integer, db.ForeignKey(id), nullable=False)
    # classroom = relationship("Classroom", back_populates="teachers")


class Child(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    classroom_id = db.Column(db.Integer, db.ForeignKey('classroom.id'), nullable=False)
    # classroom = relationship("Classroom", back_populates="children")


def test_connection(self):
    with app.app_context():
        db.create_all()
        db.init_app(app)


# FACILITIES
@app.route('/api/facilities', methods=['GET'])
def get_facilities():
    try:
        facilities = Facility.query.all()
        return jsonify([{"id": facility.id, "name": facility.name} for facility in facilities]), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500


# Example CRUD for Facility (add similar for Classroom, Teacher, Child)
@app.route('/api/facilities', methods=['POST'])
def create_facility():
    try:
        id = request.json["id"]
        name = request.json['name']
        new_facility = Facility()
        new_facility.name = name
        new_facility.id = id
        db.session.add(new_facility)
        db.session.commit()
        return jsonify({"message": "Facility created successfully"}), 201
    except Exception as e:
        return jsonify({"message": str(e)}), 500


@app.route('/api/facilities/<id>', methods=['PUT'])
def update_facility(id):
    try:
        facility = Facility.query.get(id)

        facility.name = request.json['name']
        db.session.commit()
        return jsonify({"message": "Facility updated successfully"}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500


@app.route('/api/facilities/id', methods=['DELETE'])
def delete_facility(id):
    try:
        facility = Facility.query.get(id)
        db.session.delete(facility)
        db.session.commit()
        return jsonify({"message": "Facility deleted successfully"}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500


# CLASSROOMS
@app.route('/api/classrooms', methods=['GET'])
def get_classrooms():
    try:
        classrooms = Classroom.query.all()
        return jsonify([{"id": classroom.id, "capacity": classroom.capacity, "name": classroom.name,
                         "facility_id": classroom.facility_id} for classroom in classrooms]), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500


@app.route('/api/classrooms', methods=['POST'])
def create_classroom():
    try:
        id = request.json["id"]
        capacity = request.json['capacity']
        name = request.json['name']
        facility_id = request.json['facility_id']
        new_classroom = Classroom()
        new_classroom.id = id
        new_classroom.capacity = capacity
        new_classroom.name = name
        new_classroom.facility_id = facility_id
        db.session.add(new_classroom)
        db.session.commit()
        return jsonify({"message": "Classroom created successfully"}), 201
    except Exception as e:
        return jsonify({"message": str(e)}), 500


@app.route('/api/classrooms/<id>', methods=['PUT'])
def update_classroom(id):
    try:
        classroom = Classroom.query.get(id)
        classroom.capacity = request.json['capacity']
        classroom.name = request.json['name']
        classroom.facility_id = request.json['facility_id']
        db.session.commit()
        return jsonify({"message": "Classroom updated successfully"}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500


@app.route('/api/classrooms/<id>', methods=['DELETE'])
def delete_classroom(id):
    try:
        classroom = Classroom.query.get(id)
        db.session.delete(classroom)
        db.session.commit()
        return jsonify({"message": "Classroom deleted successfully"}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500


# TEACHERS
@app.route('/api/teachers', methods=['GET'])
def get_teachers():
    try:
        teachers = Teacher.query.all()
        return jsonify(
            [{"id": teacher.id, "firstname": teacher.firstname, "lastname": teacher.lastname, "room": teacher.room} for
             teacher in teachers]), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500


@app.route('/api/teachers', methods=['POST'])
def create_teacher():
    try:
        id = request.json["id"]
        firstname = request.json['firstname']
        lastname = request.json['lastname']
        room = request.json['room']
        new_teacher = Teacher()
        new_teacher.id = id
        new_teacher.firstname = firstname
        new_teacher.lastname = lastname
        new_teacher.room = room
        db.session.add(new_teacher)
        db.session.commit()
        return jsonify({"message": "Teacher created successfully"}), 201
    except Exception as e:
        return jsonify({"message": str(e)}), 500


@app.route('/api/teachers/<id>', methods=['PUT'])
def update_teacher(id):
    try:
        teacher = Teacher.query.get(id)
        teacher.firstname = request.json['firstname']
        teacher.lastname = request.json['lastname']
        teacher.room = request.json['room']
        db.session.commit()
        return jsonify({"message": "Teacher updated successfully"}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500


@app.route('/api/teachers/<id>', methods=['DELETE'])
def delete_teacher(id):
    try:
        teacher = Teacher.query.get(id)
        db.session.delete(teacher)
        db.session.commit()
        return jsonify({"message": "Teacher deleted successfully"}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500


# CHILDREN
@app.route('/api/children', methods=['GET'])
def get_children():
    try:
        children = Child.query.all()
        return jsonify([{"id": child.id, "firstname": child.firstname, "lastname": child.lastname, "age": child.age,
                         "classroom_id": child.classroom_id} for child in children]), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500


@app.route('/api/children', methods=['POST'])
def create_child():
    try:
        id = request.json["id"]
        firstname = request.json['firstname']
        lastname = request.json['lastname']
        age = request.json['age']
        classroom_id = request.json['classroom_id']
        new_child = Child()
        new_child.id = id
        new_child.firstname = firstname
        new_child.lastname = lastname
        new_child.age = age
        new_child.classroom_id = classroom_id
        db.session.add(new_child)
        db.session.commit()
        return jsonify({"message": "Child created successfully"}), 201
    except Exception as e:
        return jsonify({"message": str(e)}), 500


@app.route('/api/children/<id>', methods=['PUT'])
def update_child(id):
    try:
        child = Child.query.get(id)
        child.firstname = request.json['firstname']
        child.lastname = request.json['lastname']
        child.age = request.json['age']
        child.classroom_id = request.json['classroom_id']
        db.session.commit()
        return jsonify({"message": "Child updated successfully"}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500


@app.route('/api/children/<id>', methods=['DELETE'])
def delete_child(id):
    try:
        child = Child.query.get(id)
        db.session.delete(child)
        db.session.commit()
        return jsonify({"message": "Child deleted successfully"}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@app.route('/login', methods=['POST'])
def login():
    try:
        username = request.json['username']
        password = request.json['password']
        if username == 'admin' and password == 'admin':
            return jsonify({"message": "Login successful"}), 200
        else:
            return jsonify({"message": "Invalid credentials"}), 401
    except Exception as e:
        return jsonify({"message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)