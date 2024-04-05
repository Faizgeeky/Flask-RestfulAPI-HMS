from flask import request
from flask_restful import Resource , reqparse
import sqlite3
import jsonify
import json

parser = reqparse.RequestParser()
parser.add_argument('page', type=int, default=1, help='Page number')
parser.add_argument('per_page', type=int, default=5, help='Items per page')


#  Connect to the database
def create_connection():
    try:
        conn = sqlite3.connect('hospital.db')
        cursor = conn.cursor()
        return conn, cursor
    except sqlite3.Error as e:
        print("Error connecting to the database:", e)
        return None, None

# ------------------ Patients ------------------------
class PatientList(Resource):
    def __init__(self):
        self.conn, self.cursor = create_connection()
        
    def get(self):
        query = '''SELECT * FROM Patient'''
        self.cursor.execute(query)
        patients = self.cursor.fetchall()
        patients_list = [{'id': patient[0], 'name': patient[1], 'age': patient[2], 'gender': patient[3], 'contact_information': patient[4]} for patient in patients]
        return patients_list, 200

    def post(self):
        data = request.json
        
        name = data.get('name')
        age = data.get('age')
        gender = data.get('gender')
        contact_information = data.get('contact_information')

        query = '''INSERT INTO Patient (name, age, gender, contact_info)
                   VALUES (?, ?, ?, ?)'''
        self.cursor.execute(query, (name, age, gender, contact_information))
        self.conn.commit()
        self.conn.close()
        return {'message': 'Patient added successfully'}, 201 

class Patient(Resource):
    def __init__(self):
        self.conn, self.cursor = create_connection()
        print("here",self.conn, self.cursor)

    def get(self):
        patient_id = request.args.get('patient_id')
        name = request.args.get('name')

        conditions = []
        values = []
        if patient_id:
            conditions.append("id = ?")
            values.append(int(patient_id))
        if name:
            conditions.append("name = ?")
            values.append(name)
        # Make this block dynamic to filter out by any passed varibales
        query = '''SELECT * FROM Patient '''
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
            self.cursor.execute(query, tuple(values))
            patients = self.cursor.fetchone()
            if patients:
                return patients, 200
            else:
                return {'message': 'Patient not found'}, 404
        else:
            query = '''SELECT * FROM Patient'''
            self.cursor.execute(query)
            patients = self.cursor.fetchall()
            patients_list = [{'id': patient[0], 'name': patient[1], 'age': patient[2], 'gender': patient[3], 'contact_information': patient[4]} for patient in patients]
            return patients_list, 200

            
class MedicalhistoryFilter(Resource):
    def __init__(self):
        self.conn, self.cursor = create_connection()
        print("here",self.conn, self.cursor)
    
    def get(self, patient_id):
        print("reched here?")
        query = '''SELECT * FROM MedicalHistory WHERE patient_id = ?'''
        self.cursor.execute(query, (patient_id,))
        patient = self.cursor.fetchone()
        if patient:
            patient_data = {'id': patient[0], 'patient_id': patient[1], 'previous_diagnoses': patient[2], 'allergies': patient[3], 'medications': patient[4]}
            return patient_data, 200
        else:
            return {'message': 'Medical record not found'}, 404
        
class Medicalhistory(Resource):
    def __init__(self):
        self.conn, self.cursor = create_connection()
        print("here",self.conn, self.cursor)
        
    def post(self):
        data = request.json

        patient_id = data.get('patient_id')
        previous_diagnoses = data.get('previous_diagnoses')
        allergies = data.get('allergies')
        medications = data.get('medications')

        # Check if the patient exists
        patient_query = '''SELECT id FROM Patient WHERE id = ?'''
        self.cursor.execute(patient_query, (patient_id,))
        patient = self.cursor.fetchone()

        if patient:
            # Insert medical history if user exist
            query = '''INSERT INTO MedicalHistory (patient_id, previous_diagnoses, allergies, medications)
                    VALUES (?, ?, ?, ?)'''
            self.cursor.execute(query, (patient_id, previous_diagnoses, allergies, medications))
            self.conn.commit()
            self.conn.close()
            return {'message': 'Medical history added successfully'}, 201
        else:
            # Handle the case where the patient does not exist
            return {'error': 'Patient does not exist'}, 404
    
class AppointmentRecord(Resource):
    def __init__(self):
        self.conn, self.cursor = create_connection()
        print("here",self.conn, self.cursor)

    def get(self):
        doctor_id = request.args.get('doctor_id')
        day = request.args.get('day')
        appointment_id = request.args.get('appointment_id')

        conditions = []
        values = []
        if doctor_id:
            conditions.append("doctor.id = ?")
            values.append(int(doctor_id))

        if day:
            conditions.append("AppointmentRecords.date = ?")
            values.append(day)

        if appointment_id:
            conditions.append("id = ?")
            values.append(int(appointment_id))
            
        query = '''SELECT AppointmentRecords.id, AppointmentRecords.date, AppointmentRecords.time,
                          Patient.name AS patient_name, Patient.age AS patient_age, Patient.gender AS patient_gender,
                          Doctor.name AS doctor_name, Doctor.specialization AS doctor_specialization,
                          Department.name AS department_name
                   FROM AppointmentRecords
                   INNER JOIN Patient ON AppointmentRecords.patient_id = Patient.id
                   INNER JOIN Doctor ON AppointmentRecords.doctor_id = Doctor.id
                   INNER JOIN Department ON AppointmentRecords.department_id = Department.id
                    '''
        field_names = ['id', 'date', 'time', 'patient_name', 'patient_age', 'patient_gender', 'doctor_name', 'doctor_specialization', 'department_name']
        if conditions :
            query += " WHERE " + " AND ".join(conditions)
            
            self.cursor.execute(query, tuple(values))
            appointments = self.cursor.fetchall()

            appointments_data = [dict(zip(field_names, appointment)) for appointment in appointments]
            
            self.conn.close()
            if appointments_data:
                return appointments_data, 200
            else:
                return {"message": "Appointment not found"}, 404
        else:
            self.cursor.execute(query)
            appointments = self.cursor.fetchall()

            appointments_data = [dict(zip(field_names, appointment)) for appointment in appointments]
            
            self.conn.close()
            if appointments_data:
                return appointments_data, 200
            else:
                return {"message": "Appointment not found"}, 404
            
            
class AppointmentRecordList(Resource):
    def __init__(self):
        self.conn, self.cursor = create_connection()
        print("here",self.conn, self.cursor)

    def post(self):
        data = request.json
        patient_id = data.get('patient_id')
        doctor_id = data.get('doctor_id')
        department_id = data.get('department_id')
        date = data.get('date')
        time = data.get('time')

        # Validations 
        patient_query = '''SELECT id FROM Patient WHERE id = ?'''
        self.cursor.execute(patient_query, (patient_id,))
        patient = self.cursor.fetchone()

        doctor_query = '''SELECT id FROM Doctor WHERE id = ?'''
        self.cursor.execute(doctor_query, (doctor_id,))
        doctor = self.cursor.fetchone()

        department_query = '''SELECT id FROM Department WHERE id = ?'''
        self.cursor.execute(department_query, (department_id,))
        department = self.cursor.fetchone()
        
        # Now check if Doctor is Available on particular date before taking appointment
        if doctor:
            query = '''SELECT id from doctor_availability WHERE day = ? and doctor_id = ? and available = 1'''
            self.cursor.execute(query, (date, doctor_id,))
            available = self.cursor.fetchone()
        
        if available:
            if patient and doctor and department:
                # Save appt record once validated
                query = '''INSERT INTO AppointmentRecords (patient_id, doctor_id, department_id, date, time)
                        VALUES (?, ?, ?, ?, ?)'''
                self.cursor.execute(query, (patient_id, doctor_id, department_id, date, time))
                self.conn.commit()
                self.conn.close()
                return {'message': 'Appointment added successfully'}, 201
            else:
                return {'error': 'Patient, doctor, or department does not exist'}, 404
        else:
            return{'message': 'Doctor is not avalibale for Appointmen'}, 200
         
# ------------------ Doctor  ------------------------
class DoctorList(Resource):
    def __init__(self):
        self.conn, self.cursor = create_connection()
        print("here",self.conn, self.cursor)
    
    def post(self):
        data = request.json
        
        name = data.get('name')
        specialization = data.get('specialization')
        contact_info = data.get('contact_info')
        department_id = data.get('department_id')

        department_query = '''SELECT id FROM Department WHERE id = ?'''
        self.cursor.execute(department_query, (department_id,))
        department = self.cursor.fetchone()

        if department:
            query = '''INSERT INTO Doctor (name, specialization, contact_info, department_id)
                    VALUES (?, ?, ?, ?)'''
            self.cursor.execute(query, (name, specialization, contact_info, department_id))
            self.conn.commit()
            self.conn.close()
            return {'message': 'Doctor added successfully'}, 201 
        else:
            return {'message': 'Department not Found'}, 404

class Doctor(Resource):
    def __init__(self):
        self.conn, self.cursor = create_connection()
        print("here",self.conn, self.cursor)

    def get(self):
        doctor_id = request.args.get('doctor_id')
        doctor_name = request.args.get('doctor_name')
        specialization = request.args.get('specialization')

        conditions = []
        values = []

        # Add conditions based on provided parameters
        if doctor_id:
            conditions.append("doctor.id = ?")
            values.append(int(doctor_id))
        if doctor_name:
            conditions.append("doctor.name = ?")
            values.append(doctor_name)
        if specialization:
            conditions.append("doctor.specialization = ?")
            values.append(specialization)
        # Construct the SQL query
        query = '''SELECT doctor.id , doctor.name, 
                   doctor.specialization , doctor.contact_info, 
                   department.id , department.name  
                   FROM Doctor 
                   INNER JOIN Department ON doctor.department_id = department.id'''
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
            
            self.cursor.execute(query, tuple(values))
            doctors = self.cursor.fetchall()
            if doctors:
                return doctors, 200
            else:
                return {"message": "No Doctor found"}, 404 

        else:
            query = '''SELECT doctor.id, doctor.name, doctor.specialization, doctor.contact_info, department.id, department.name FROM Doctor 
                        INNER JOIN Department ON Doctor.department_id = Department.id'''
            self.cursor.execute(query,)

            doctor = self.cursor.fetchall()
            if doctor:
                return doctor, 200
            else:
                return {"message": "No Doctor found"}, 404    

class AddAvailibility(Resource):
    def __init__(self):
        self.conn, self.cursor = create_connection()
        print("here",self.conn, self.cursor)
    
    def post(self):
        data = request.json
        doctor_id = data.get('doctor_id')
        day = data.get('day')
        available = data.get('available')

        # Check if doctor exisit 
        doctor_query = '''SELECT id FROM Doctor WHERE id = ?'''
        self.cursor.execute(doctor_query, (doctor_id,))
        doctor = self.cursor.fetchone()

        if doctor :
            # Save appt record once validated
            query = '''INSERT INTO doctor_availability ( doctor_id, day, available)
                    VALUES (?, ?, ?)'''
            self.cursor.execute(query, (doctor_id, day, available))
            self.conn.commit()
            self.conn.close()
            return {'message': 'Availibility added successfully'}, 201
        else:
            return {'error': 'Doctor does not exist'}, 404

class CheckAvailibility(Resource):
    def __init__(self):
        self.conn, self.cursor = create_connection()
        
    def get(self, doctor_id, date):
        print("date is", date)
        try:
            doctor_query = '''SELECT id FROM Doctor WHERE id = ?'''
            self.cursor.execute(doctor_query, (doctor_id,))
            doctor = self.cursor.fetchone()
            
            if doctor:
                query = '''SELECT doctor_availability.available, doctor_availability.day, 
                    Doctor.name, Doctor.specialization, Doctor.contact_info 
                    FROM doctor_availability 
                    INNER JOIN Doctor ON doctor_availability.doctor_id = Doctor.id 
                    WHERE doctor_availability.doctor_id = ? AND day = ?'''

                self.cursor.execute(query, (doctor_id,date,))
                availability = self.cursor.fetchone()
                # Handle return as per availibity check
                if availability:
                    availability_data = {
                        "available": availability[0],
                        "date": availability[1],
                        "doctor": {
                            "name": availability[2],
                            "specialization": availability[3],
                            "contact_info": availability[4]
                        }
                    }
                    return availability_data, 200
                else:
                    return {"message": "No availability found for the doctor on the specified date"}, 404
            else:
                return {'error': 'Doctor does not exist'}, 404
        except Exception as e:
            return {'error': str(e)}, 500  

    
    def post(self):
        try:
            data = request.json
            date = data.get('date') 
            query = '''SELECT doctor_availability.available, doctor_availability.day, 
                    Doctor.name, Doctor.specialization, Doctor.contact_info 
            FROM doctor_availability 
            INNER JOIN Doctor ON doctor_availability.doctor_id = Doctor.id 
            WHERE day = ?'''
            self.cursor.execute(query, (date,))
            availabilities = self.cursor.fetchall()

            result = []
            for availability in availabilities:
                availability_data = {
                    "available": availability[0],
                    "day": availability[1],
                    "doctor": {
                        "name": availability[2],
                        "specialization": availability[3],
                        "contact_info": availability[4]
                    }
                }
                result.append(availability_data)

            return result, 200
        except Exception as e:
            return {"message": str(e)}, 500  # Return an error message and status code 500 for internal server error

#  ------------------- Departments  --------------------------
class Department(Resource):
    def __init__(self):
        self.conn, self.cursor = create_connection()

    def get(self, department_id=None):
        if department_id:
            query = '''SELECT * FROM Department 
                        WHERE id = ?'''
            self.cursor.execute(query, (department_id,))
            department = self.cursor.fetchone()
            if department:
                return department, 200
            else:
                return {"message": "Department not found"}, 404
        else:
            query = '''SELECT * FROM Department '''
            self.cursor.execute(query)
            departments = self.cursor.fetchall()
            if departments:
                return departments, 200
            else:
                return {"message": "No departments found"}, 404

    def post(self):
        data = request.json
        name = data.get('name')
        # Handle adding a new department
        try:
            query = '''INSERT INTO Department (name)
                       VALUES (?)'''
            self.cursor.execute(query, (name,))
            self.conn.commit()
            self.conn.close()

            return {'message': 'Department added successfully'}, 201
        except Exception as e:
            print("Error:", e)
            return {'error': 'Unable to add department'}, 500  # Change status code to 500 for internal server error


# ---------------- Pagination -----------------

class PatientPagination(Resource):
    def __init__(self):
        self.conn, self.cursor = create_connection()

    def get(self):
        print("any data here ?")
        try:
            # Parse query parameters
            page = int(request.args.get('page', 1))
            per_page = int(request.args.get('per_page', 10))

            # Calculate start and end indices for pagination
            start_index = (page - 1) * per_page
            end_index = page * per_page

            query = '''SELECT * FROM Patient LIMIT ?, ?'''
            self.cursor.execute(query, (start_index, per_page))
            paginated_patients = self.cursor.fetchall()

            # Close the database connection
            self.conn.close()

            return paginated_patients, 200
        except Exception as e:
            return {'error': str(e)}, 201
