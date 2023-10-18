from flask import request, redirect, render_template, url_for, flash
from flask_login import login_required, current_user


from app import create_app
from app.forms import *
from app.firestore_service import *

app = create_app()

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html', error=error)

@app.errorhandler(500)
def server_error(error):
    return render_template('500.html', error=error)


@app.route('/', methods=['GET', 'POST'])
def index():
    ingreso_form = IngresoForm()
    context = {
        'ingreso_form': ingreso_form,
    }
    if ingreso_form.validate_on_submit():
        return redirect(url_for('auth.login'))
    return render_template('welcome.html', **context)


@app.route('/hello', methods=['GET', 'POST'])
@login_required
def hello():
    username = current_user.id
    context = {
        'username': username,
    }

    if request.method == 'POST':
        if 'crear' in request.form:
            return redirect(url_for('registrar'))
        elif 'buscar' in request.form:
            return redirect(url_for('buscar'))
        elif 'update' in request.form:
            return redirect(url_for('buscar_actualizar'))
        elif 'delete' in request.form:
            return redirect(url_for('buscar_eliminar'))
        elif 'informe' in request.form:
            return redirect(url_for('informe'))
    return render_template('hello.html', **context)


@app.route('/registrar', methods=['GET', 'POST'])
def registrar():
    nuevo_form = CrearRegistro()

    if nuevo_form.validate_on_submit():
        id_orden = nuevo_form.id_orden.data
        fecha = nuevo_form.fecha.data
        fecha_str = fecha.strftime('%Y-%m-%d')
        nombre_cliente = nuevo_form.nombre_cliente.data
        email_cliente = nuevo_form.email_cliente.data
        telefono_cliente = nuevo_form.telefono_cliente.data
        doc_cliente = nuevo_form.doc_cliente.data
        tipo_vehiculo = nuevo_form.tipo_vehiculo.data
        marca_mod = nuevo_form.marca_mod.data
        status_trabajo = nuevo_form.status_trabajo.data
        trabajo = nuevo_form.trabajo.data
        observaciones = nuevo_form.observaciones.data

        registro = {
            'id_orden': id_orden,
            'fecha': fecha_str,
            'nombre_cliente': nombre_cliente,
            'email_cliente': email_cliente,
            'telefono_cliente': telefono_cliente,
            'doc_cliente': doc_cliente,
            'tipo_vehiculo': tipo_vehiculo,
            'marca_mod': marca_mod,
            'status_trabajo': status_trabajo,
            'trabajo': trabajo,
            'observaciones': observaciones
        }
        put_registro(registro)
        flash('Registro creado con éxito')
        return redirect(url_for('hello'))
    return render_template('nuevo.html', nuevo_form=nuevo_form)


@app.route('/buscar', methods=['GET', 'POST'])
def buscar():
    buscar_form = BuscarRegistro()
    resultados = []

    if buscar_form.validate_on_submit():
        query_string = buscar_form.query_string.data
        resultados = search_registros(query_string)
        flash(f'Se encontraron {len(resultados)} resultados.', 'info')
    return render_template('buscar.html', buscar_form=buscar_form, resultados=resultados)


@app.route('/informe', methods=['GET', 'POST'])
def informe():
    informe_form = VerBotonInforme()
    resultados = []

    if informe_form.validate_on_submit():
        resultados = informe_registros()
    return render_template('informe.html', informe_form=informe_form, resultados=resultados)


@app.route('/eliminar', methods=['GET', 'POST'])
def buscar_eliminar():
    buscar_form = BuscarRegistro()
    delete_form = DeleteBotonForm()
    resultados = []

    if buscar_form.validate_on_submit():
        query_string = buscar_form.query_string.data
        resultados = search_registros(query_string)
        flash(f'Se encontraron {len(resultados)} resultados.', 'info')
    return render_template('buscar_eliminar.html', buscar_form=buscar_form, delete_form=delete_form, resultados=resultados)


@app.route('/eliminar/buscar_eliminar/<id_documento>', methods=['POST'])
def eliminar(id_documento):
    eliminar_registro(id_documento)

    return redirect(url_for('hello'))

@app.route('/editar', methods=['GET', 'POST'])
def buscar_actualizar():
    buscar_form = BuscarRegistro()
    update_form = UpdateBotonForm()
    resultados = []

    if buscar_form.validate_on_submit():
        query_string = buscar_form.query_string.data
        resultados = search_registros(query_string)
        flash(f'Se encontraron {len(resultados)} resultados.', 'info')
    return render_template('buscar_actualizar.html', buscar_form=buscar_form, update_form=update_form, resultados=resultados)

@app.route('/editar/buscar_actualizar/<id_documento>', methods=['GET', 'POST'])
def actualizar(id_documento):
    resultado = obtener_registro_por_id(id_documento)
    update_form = UpdateRegistroForm()

    if request.method == 'POST' and update_form.validate_on_submit():
        nuevos_datos = {
            'id_orden': update_form.nuevo_id_orden.data,
            'fecha': update_form.nuevo_fecha_str.data.strftime('%Y-%m-%d'),
            'nombre_cliente': update_form.nuevo_nombre_cliente.data,
            'email_cliente': update_form.nuevo_email_cliente.data,
            'telefono_cliente': update_form.nuevo_telefono_cliente.data,
            'doc_cliente': update_form.nuevo_doc_cliente.data,
            'tipo_vehiculo': update_form.nuevo_tipo_vehiculo.data,
            'marca_mod': update_form.nuevo_marca_mod.data,
            'status_trabajo': update_form.nuevo_status_trabajo.data,
            'trabajo': update_form.nuevo_trabajo.data,
            'observaciones': update_form.nuevo_observaciones.data
        }
        actualizar_registro(id_documento, nuevos_datos)
        flash('Registro actualizado correctamente', 'success')
        return redirect(url_for('hello'))

    if resultado:
        update_form.nuevo_id_orden.data = resultado.get('id_orden', '')
        update_form.nuevo_fecha_str.data = resultado.get('fecha', '')
        update_form.nuevo_nombre_cliente.data = resultado.get('nombre_cliente', '')
        update_form.nuevo_email_cliente.data = resultado.get('email_cliente', '')
        update_form.nuevo_telefono_cliente.data = resultado.get('telefono_cliente', '')
        update_form.nuevo_doc_cliente.data = resultado.get('doc_cliente', '')
        update_form.nuevo_tipo_vehiculo.data = resultado.get('tipo_vehiculo', '')
        update_form.nuevo_marca_mod.data = resultado.get('marca_mod', '')
        update_form.nuevo_status_trabajo.data = resultado.get('status_trabajo', '')
        update_form.nuevo_trabajo.data = resultado.get('trabajo', '')
        update_form.nuevo_observaciones.data = resultado.get('observaciones', '')
    return render_template('actualizar.html', update_form=update_form, resultado=resultado)

