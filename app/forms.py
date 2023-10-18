from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField, DateField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, Email

class IngresoForm(FlaskForm):
    submit = SubmitField('Comenzar')

class SignupForm(FlaskForm):
    username = StringField('Nombre de usuario', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Enviar')

class LoginForm(FlaskForm):
    username = StringField('Nombre de usuario', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Enviar')
    

class CrearRegistro(FlaskForm):
    id_orden = StringField('Id Trabajo:', validators=[DataRequired()])
    fecha = DateField('Fecha Recepción:', validators=[DataRequired()])
    nombre_cliente = StringField('Nombre del cliente:', validators=[DataRequired()])
    email_cliente = StringField('Email del cliente:', validators=[Email()])
    telefono_cliente = IntegerField('Teléfono del cliente:', validators=[DataRequired()])
    doc_cliente = StringField('DNI/CIF del cliente:')
    tipo_vehiculo = StringField('Tipo de vehículo:', validators=[DataRequired()])
    marca_mod = StringField('Marca/Modelo/Color:', validators=[DataRequired()])
    status_trabajo = StringField('Status Trabajo:', validators=[DataRequired()])
    trabajo = StringField('Descripción del Trabajo:', validators=[DataRequired()])
    observaciones = TextAreaField('Observaciones:')
    submit = SubmitField('Crear')

class BuscarRegistro(FlaskForm):
    query_string = StringField('Palabra clave')
    submit = SubmitField('Buscar Registro')

class VerBotonInforme(FlaskForm):
    submit = SubmitField('Generar Informe')

class DeleteBotonForm(FlaskForm):
    submit = SubmitField('Borrar')

class UpdateBotonForm(FlaskForm):
    submit = SubmitField('Actualizar')

class UpdateRegistroForm(FlaskForm):
    nuevo_id_orden = StringField('Id Trabajo:', validators=[DataRequired()])
    nuevo_fecha_str = DateField('Fecha Recepción:', validators=[DataRequired()])
    nuevo_nombre_cliente = StringField('Nombre del cliente:', validators=[DataRequired()])
    nuevo_email_cliente = StringField('Email del cliente:', validators=[Email()])
    nuevo_telefono_cliente = IntegerField('Teléfono del cliente:', validators=[DataRequired()])
    nuevo_doc_cliente = StringField('DNI/CIF del cliente:')
    nuevo_tipo_vehiculo = StringField('Tipo de vehículo:', validators=[DataRequired()])
    nuevo_marca_mod = StringField('Marca/Modelo/Color:', validators=[DataRequired()])
    nuevo_status_trabajo = StringField('Status Trabajo:', validators=[DataRequired()])
    nuevo_trabajo = StringField('Descripción del Trabajo:', validators=[DataRequired()])
    nuevo_observaciones = TextAreaField('Observaciones:')
    submit = SubmitField('Actualizar')