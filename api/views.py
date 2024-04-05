from flask import Blueprint
from flask_restful import Api

from api.resources.hm_system import  *
# AppointmentRecordList, AppointmentRecord, Medicalhistory, MedicalhistoryFilter, Patient, PatientList, Department , DepartmentList, Doctor , DoctorList

blueprint = Blueprint("api", __name__, url_prefix="/api")
api = Api(blueprint, errors=blueprint.errorhandler)

# Manage Patient end points
api.add_resource(PatientList, '/patients')
api.add_resource(MedicalhistoryFilter, '/medicalrecord/<int:patient_id>')
api.add_resource(Medicalhistory, '/medicalrecord')
api.add_resource(AppointmentRecordList, '/appointmentrecords')
api.add_resource(AppointmentRecord, '/filter-appointments')

# Manage doctors end point
api.add_resource(DoctorList, '/doctors')
# api.add_resource(Doctor, '/doctors/<int:doctor_id>', endpoint='get doctor by id')
api.add_resource(Doctor, '/doctors', endpoint='get all doctors')

api.add_resource(CheckAvailibility, '/availability/<int:doctor_id>/<string:date>', endpoint='check_availability_by_id_and_date')
api.add_resource(CheckAvailibility, '/availability', endpoint='check_availability')
api.add_resource(AddAvailibility, '/availibility')


#manage departments end points
api.add_resource(Department, '/departments/<int:department_id>')
api.add_resource(Department, '/departments',endpoint='get_department')
api.add_resource(Department, '/departments',endpoint='add_department')


# Manage search api 
api.add_resource(Doctor, '/doctors', endpoint='Get filter ')
api.add_resource(Patient, '/patient', endpoint='Get filter by Name and id')

#Manage pagination Patient
api.add_resource(PatientPagination, '/filter_patient')
