from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, FileField, DateField, TimeField
from wtforms.validators import InputRequired, Length
from flask_wtf.file import FileField, FileAllowed, FileRequired




class CATForm(FlaskForm):
    viaje_ot = StringField('Viaje/OT', validators
                           =[InputRequired(),
                             Length(min=6, max=7) ])
    cliente = SelectField('Cliente', choices=[('','-----'),
                                              ('AMSA', 'AMSA'), 
                                              ('Alto Norte', 'Alto Norte'), 
                                              ('BHP', 'BHP'), 
                                              ('Codelco', 'Codelco'), 
                                              ('Codesa', 'Codesa'), 
                                              ('CMDIC', 'CMDIC'), 
                                              ('Engie', 'Engie'), 
                                              ('Finning', 'Finning'), 
                                              ('Glencore', 'Glencore'), 
                                              ('Lomas Bayas', 'Lomas Bayas'), 
                                              ], 
                                              validators=[InputRequired()])
    
    agencia = SelectField('Agencia', choices=[('','-----'),
                                              ('SCL', 'SCL'), 
                                              ('ANF', 'ANF'), 
                                              ('POZ', 'POZ'), 
                                              ('CPP', 'CPP'),  
                                              ], 
                                              validators=[InputRequired()])
    
     
    tipo_extra_costo = SelectField('Tipo Extra Costo', choices=[('','-----'),
                                                                 ('AJUSTE TARIFA', 'AJUSTE TARIFA'),                                                                  
                                                                 ('ARRIENDO FIJO', 'ARRIENDO FIJO'), 
                                                                 ('URGENCIA DOBLE CONDUCTOR', 'URGENCIA DOBLE CONDUCTOR'),                                                                   
                                                                 ('MOVIMIENTO INTERNO', 'MOVIMIENTO INTERNO'), 
                                                                 ('REDESTINACIÓN', 'REDESTINACIÓN'), 
                                                                 ('SOBRE ESTADÍA', 'SOBRE ESTADÍA'), 
                                                                 ('FALSO FLETE', 'FALSO FLETE'),
                                                                 ('POSICIONAMIENTO VACIO', 'POSICIONAMIENTO VACIO'),
                                                                 ('SOBREDIMENSION', 'SOBREDIMENSION')], 
                                                        validators=[InputRequired()])
    motivo_ajuste_tarifa = SelectField('Motivo', choices=[('','-----'),
                                                          ('DESCUENTA TARIFA', 'DESCUENTA TARIFA'),
                                                            ('AUMENTO TARIFA', 'AUMENTO TARIFA'),
                                                            ('EL LIBERTADOR', 'EL LIBERTADOR')])
    motivo_redestinacion = SelectField('Motivo', choices=[('','-----'),
                                                          ('POR CUENTA DE MINTRAL', 'POR CUENTA DE MINTRAL' ),  
                                                            ('POR CUENTA DE CLIENTE', 'POR CUENTA DE CLIENTE' ),
                                                            ])
    motivo_sobre_estadia = SelectField('Motivo', choices=[  ('','-----'),
                                                          ('BODEGA CLIENTE', 'BODEGA CLIENTE'),
                                                            ('BODEGA MINTRAL', 'BODEGA MINTRAL'),
                                                            ('BODEGA PROVEEDOR', 'BODEGA PROVEEDOR')
                                                            ])
    
    motivo_falso_flete = SelectField('Motivo', choices=[  ('','-----'),
                                                          ('POR CUENTA DE MINTRAL', 'POR CUENTA DE MINTRAL'),
                                                            ('POR CUENTA DE CLIENTE', 'POR CUENTA DE CLIENTE'),
                                                            ])
    
    motivo_posicionamiento_vacio = SelectField('Motivo', choices=[('','-----'),
                                                          ('POR CUENTA DE MINTRAL', 'POR CUENTA DE MINTRAL'),
                                                            ('POR CUENTA DE CLIENTE', 'POR CUENTA DE CLIENTE'),
                                                            ])
    
    hora_llegada = TimeField('Hora de Llegada', validators=[InputRequired()], render_kw={"class": "form-control mb-3"})

    dia2 = DateField('Dia', validators=[InputRequired()], render_kw={"class": "form-control mb-3"}) 
    hora_salida = TimeField('Hora de Llegada', validators=[InputRequired()], render_kw={"class": "form-control mb-3"})
    dia3 = DateField('Dia', validators=[InputRequired()], render_kw={"class": "form-control mb-3"})
    total_horas = StringField('Total Horas')
    empresa = SelectField('Empresa', choices=[('','-----'),
                                                                  ('LIBERTADOR', 'LIBERTADOR'),
                                                            ('TRANSPORTE IVAN MAURICIO MATELUNA', 'TRANSPORTE IVAN MAURICIO MATELUNA')
                                                            ], validators=[InputRequired()])
    monto = StringField('Monto', validators=[InputRequired()],render_kw={"id":"montoInput"})
    nombre_zip = FileField('Adjuntar Archivo', render_kw={"type": "file", "accept": ".rar, .zip"})
    submit = SubmitField('Guardar', render_kw={'onclick': 'confirmarGuardado();', 'type': 'submit'})


class historialForm(FlaskForm):
      fecha_inicio = DateField('Dia', render_kw={"class": "form-control mb-3"}) 
      fecha_fin = DateField('Dia', render_kw={"class": "form-control mb-3"}) 
      cliente = SelectField('Cliente', choices=[('','-----'),
                                              ('AMSA', 'AMSA'), 
                                              ('Alto Norte', 'Alto Norte'), 
                                              ('BHP', 'BHP'), 
                                              ('Codelco', 'Codelco'), 
                                              ('Codesa', 'Codesa'), 
                                              ('CMDIC', 'CMDIC'), 
                                              ('Engie', 'Engie'), 
                                              ('Finning', 'Finning'), 
                                              ('Glencore', 'Glencore'), 
                                              ('Lomas Bayas', 'Lomas Bayas'), 
                                              ])
      estado = SelectField('Estado', choices=[('','-----'),
                                              ('Aprobado', 'Aprobado'), 
                                              ('Rechazado', 'Rechazado'), 
                                              ('Ingresado Sitrack', 'Ingresado Sitrack'), 
                                              ('No ingresado Sitrack	', 'No ingresado Sitrack	'),  
                                              ])
      viaje_ot = StringField('Viaje/OT', validators
                        =[Length(min=6, max=7) ])
      
      submit = SubmitField('Buscar')

      
       





