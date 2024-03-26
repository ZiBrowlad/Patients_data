CREATE_PATIENTS_TABLE = (
    'CREATE TABLE IF NOT EXISTS patients (id serial PRIMARY KEY, surname VARCHAR(30), name VARCHAR(30), age INT);'
)

INSERT_PATIENT = (
    'INSERT INTO patients (surname, name, age) VALUES (%s, %s, %s);'
)

DATA_REPETITION = (
    'SELECT * FROM patients WHERE surname = %s AND name = %s AND age = %s;'
)

GET_ALL_PATIENTS = (
    'SELECT * FROM patients;'
)

GET_PATIENT = (
    'SELECT id, surname, name, age FROM patients WHERE id = %s'
)

DELETE_PATIENT = (
    'DELETE FROM patients WHERE id = %s'
)

UPDATE_PATIENT = (
    'UPDATE patients SET surname = %s, name = %s, age = %s WHERE id = %s'
)