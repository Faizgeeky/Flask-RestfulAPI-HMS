import sqlite3
import config
conn = sqlite3.connect(config.DATABASE_NAME)

# Create a cursor object to execute SQL queries
cursor = conn.cursor()

# Execute for the first time to crerate all tables 
cursor.execute('''CREATE TABLE IF NOT EXISTS Patient (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    age INTEGER,
                    gender TEXT,
                    contact_info TEXT
                )''')

cursor.execute('''CREATE TABLE IF NOT EXISTS Department (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL
                )''')

cursor.execute('''CREATE TABLE IF NOT EXISTS Doctor (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    specialization TEXT,
                    contact_info TEXT,
                    department_id INTEGER,
                    FOREIGN KEY(department_id) REFERENCES Department(id)
                )''')

cursor.execute('''CREATE TABLE IF NOT EXISTS doctor_availability (
                    id INTEGER PRIMARY KEY,
                    doctor_id INTEGER,
                    day TEXT,
                    available BOOLEAN,
                    FOREIGN KEY (doctor_id) REFERENCES Doctor(id)
                )''')

cursor.execute('''CREATE TABLE IF NOT EXISTS MedicalHistory (
                    id INTEGER PRIMARY KEY,
                    patient_id INTEGER,
                    previous_diagnoses TEXT,
                    allergies TEXT,
                    medications TEXT,
                    FOREIGN KEY(patient_id) REFERENCES Patient(id)
                )''')

cursor.execute('''CREATE TABLE IF NOT EXISTS AppointmentRecords (
                    id INTEGER PRIMARY KEY,
                    patient_id INTEGER,
                    doctor_id INTEGER,
                    department_id INTEGER,
                    date DATE,
                    time TIME,
                    FOREIGN KEY(patient_id) REFERENCES Patient(id),
                    FOREIGN KEY(doctor_id) REFERENCES Doctor(id),
                    FOREIGN KEY(department_id) REFERENCES Department(id)
                )''')

cursor.execute('''CREATE TABLE IF NOT EXISTS service_offered (
                    id INTEGER PRIMARY KEY,
                    department_id INTEGER,
                    service_name TEXT,
                    FOREIGN KEY (department_id) REFERENCES Department(id)
                )''')


# Commit changes and close connection
conn.commit()
conn.close()
