from flask import Flask, request
import psycopg2
import os
from dotenv import load_dotenv
from sql_queries import *

load_dotenv()

app = Flask(__name__)

url = os.getenv('DATABASE_URL')

@app.get('/')
def home():
    return {
        'ФМБА России': 'Карты пациентов'
    }, 200

@app.post('/patients')
def get_patient():
    data = request.get_json()
    surname = data['surname']
    name = data['name']
    age = data['age']

    with psycopg2.connect(url) as connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_PATIENTS_TABLE)
            cursor.execute(DATA_REPETITION, (surname, name, age))
            if cursor.fetchone():
                return {'msg': 'There is already a patient'}, 400
            else:
                cursor.execute(INSERT_PATIENT, (surname, name, age))
    return {
        'msg': f'Successfully added patient: "{surname, name, age}"'}, 201


@app.get('/patients')
def get_all_patients():
    with psycopg2.connect(url) as connection:
        with connection.cursor() as cursor:
            cursor.execute(GET_ALL_PATIENTS)
            patients = cursor.fetchall()
            if patients:
                patient_list = []
                for patient in patients:
                    patient_info = {
                        'id': patient[0],
                        'surname': patient[1],
                        'name': patient[2],
                        'age': patient[3]
                    }
                    patient_list.append(patient_info)
                return {'patients': patient_list}, 200
            else:
                return {'msg': 'No patients found'}, 404

@app.get('/patients/<int:id>')
def view_patient(id):
    try:
        with psycopg2.connect(url) as connection:
            with connection.cursor() as cursor:
                cursor.execute(GET_PATIENT, (id,))
                patient_data = cursor.fetchone()
        return {
            "id": patient_data[0],
            "surname": patient_data[1],
            "name": patient_data[2],
            "age": patient_data[3]
        }, 200
    except:
        return {'msg': f'No patient: "{id}"'}, 404

@app.put('/patients/<int:id>')
def put_patient(id):
    data = request.get_json()
    surname = data['surname']
    name = data['name']
    age = data['age']

    with psycopg2.connect(url) as connection:
        with connection.cursor() as cursor:
            cursor.execute(UPDATE_PATIENT, (surname, name, age, id))
    if cursor.rowcount > 0:
        return {'msg': f'Patient updated successfully: "{id}"'}, 200
    else:
        return {'msg': f'No patient with id: "{id}"'}, 404

@app.delete('/patients/<int:id>')
def delete_patient(id):
    with psycopg2.connect(url) as connection:
        with connection.cursor() as cursor:
            cursor.execute(DELETE_PATIENT, (id,))
            if cursor.rowcount > 0:
                return {'msg': f'Patient deleted successfully: "{id}"'}, 200
            else:
                return {'msg': f'No patient with id: "{id}"'}, 404
