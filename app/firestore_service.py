import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from flask import flash
from datetime import datetime


credential = credentials.ApplicationDefault()
firebase_admin.initialize_app(credential)

db = firestore.client()


def get_users():
    return db.collection('users').get()

def get_user(user_id):
    return db.collection('users').document(user_id).get()

def user_put(user_data):
    user_ref = db.collection('users').document(user_data.username)
    user_ref.set({
        'password': user_data.password,
        'email': user_data.email
    })


def put_registro(registro):
    id_documento = db.collection('registros').document().id
    registro['id_documento'] = id_documento
    db.collection('registros').document(id_documento).set(registro)

def search_registros(query_string):
    query = db.collection('registros')
    resultados = []

    if query_string:
        query_string = query_string.lower()
        registros = query.stream()
        for registro in registros:
            registro_data = registro.to_dict()
            for valor in registro_data.values():
                if query_string in str(valor).lower():
                    resultados.append(registro_data)
                    break
    return resultados

def informe_registros():
    registros_ref = db.collection('registros')
    resultados = []

    for registro in registros_ref.stream():
        resultados.append(registro.to_dict())
    return resultados

def eliminar_registro(id_documento):
    try:
        db.collection('registros').document(id_documento).delete()
        flash('Registro eliminado correctamente', 'success')
    except Exception as e:
        flash('Error al eliminar el registro: ' + str(e), 'danger')

def actualizar_registro(id_documento, nuevos_datos):
    try:
        db.collection('registros').document(id_documento).update(nuevos_datos)
        flash('Registro actualizado correctamente', 'success')
    except Exception as e:
        flash('Error al actualizar el registro: ' + str(e), 'danger')

def obtener_registro_por_id(id_documento):
    registro_ref = db.collection('registros').document(id_documento)
    registro = registro_ref.get()

    if registro.exists:
        registro_data = registro.to_dict()
        fecha_str = registro_data.get('fecha', '')
        if fecha_str:
            registro_data['fecha'] = datetime.strptime(fecha_str, '%Y-%m-%d')
        print(f"Registro encontrado: {registro_data}")
        return registro_data
    else:
        print(f"Registro no encontrado para ID: {id_documento}")
        return None