# pyrefly: ignore [missing-import]
from flask import Flask, render_template, request, send_file, redirect, url_for, session, flash
from functools import wraps
# pyrefly: ignore [missing-import]
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from datetime import datetime
import io
import os
import zipfile
# pyrefly: ignore [missing-import]
from dotenv import load_dotenv
import pandas as pd
from models.predio import Predio
from models.jefe import Jefe
from models.conyuge import Conyuge
from models.carga_familiar import CargaFamiliar
from models.familiar_adicional import FamiliarAdicional
from models.contacto import Contacto
from models.empresa import Empresa
from models.constatacion import Constatacion

from models.beneficiario import Beneficiario
# pyrefly: ignore [missing-import]
from docxtpl import DocxTemplate
# pyrefly: ignore [missing-import]
import jinja2
# pyrefly: ignore [missing-import]
from werkzeug.security import generate_password_hash, check_password_hash
from models.database import db
from models.usuario import Usuario
from models.admin import Admin
from models.entidad_tecnica import EntidadTecnica
from models.ingeniero import Ingeniero
from models.registro_et import RegistroET
from models.ficha_inscripcion import FichaInscripcion
from models.ficha_predio import FichaPredio
from models.ficha_jefe import FichaJefe
from models.ficha_conyuge import FichaConyuge
from models.ficha_carga import FichaCarga
from models.ficha_adicional import FichaAdicional
app = Flask(__name__)
app.secret_key = 'clave_secreta_ptp_fipi_2025'  # Clave para firmar las sesiones

# Cargar variables de entorno desde el archivo .env si existe
load_dotenv()

# --- CONFIGURACIÓN BASE DE DATOS ---
# En Render, la cadena de conexión se inyecta automáticamente en la variable DATABASE_URL.
url_bd = os.environ.get('DATABASE_URL')

# Render a veces proporciona la URL con "postgres://", pero SQLAlchemy requiere "postgresql://"
if url_bd and url_bd.startswith("postgres://"):
    url_bd = url_bd.replace("postgres://", "postgresql://", 1)

# Fallback para desarrollo local (por ejemplo, base de datos SQLite u otra URL)
app.config['SQLALCHEMY_DATABASE_URI'] = url_bd or 'sqlite:///local.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_pre_ping': True,
    'pool_recycle': 300,
}
db.init_app(app)



# --- CONFIGURACIÓN ---
NOMBRE_PLANTILLA = "FORMULARIO DE INSCRIPCION 2025 II.pdf"  # El nombre de tu archivo PDF real

# --- DECORADOR DE PROTECCIÓN DE RUTAS ---
def login_requerido(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin' not in session:
            return redirect(url_for('mostrar_login'))
        return f(*args, **kwargs)
    return decorated_function

def get_current_user():
    if 'admin' in session:
        return Admin.query.filter_by(username=session['admin']).first()
    return None

def get_entidades_permitidas():
    return EntidadTecnica.query.all()

@app.context_processor
def inject_user():
    return dict(current_user=get_current_user())


# ==========================================
# GLOBAL ERROR HANDLERS (Evitar pantallas feas)
# ==========================================
from sqlalchemy.exc import OperationalError, SQLAlchemyError

@app.errorhandler(500)
@app.errorhandler(OperationalError)
@app.errorhandler(SQLAlchemyError)
def handle_database_error(error):
    db.session.rollback()
    flash('El servidor de base de datos cortó la conexión inesperadamente por inactividad. Por favor, vuelve a intentar la acción.', 'danger')
    # Intenta redirigir a la página donde estaba, si no, al dashboard
    from flask import request
    return redirect(request.referrer or url_for('dashboard'))

@app.route('/') 
def mostrar_login():
    return render_template('login.html')

@app.route('/validar', methods=['POST'])
def login():
    if request.method == 'POST':
        usuario = request.form.get('usuario')
        password = request.form.get('password')
        
        # Validación con Base de Datos usando la tabla Admin
        admin_user = Admin.query.filter_by(username=usuario).first()
        
        if admin_user and check_password_hash(admin_user.password_hash, password):
            session['admin'] = admin_user.username  # Registramos al admin en la sesión
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error='Administrador o contraseña incorrectos')
    
    return render_template('login.html')

# 2. RUTA DASHBOARD (La bienvenida)
@app.route('/dashboard')
@login_requerido
def dashboard():
    # Renderiza la página de bienvenida que hereda de base.html
    return render_template('dashboard.html')

# 3. RUTA FORMULARIO (La herramienta)
@app.route('/formulario')
@login_requerido
def formulario():
    entidades = get_entidades_permitidas()
    return render_template('formulario.html', entidades=entidades)

# 3.5 RUTA CONSTATACION
@app.route('/constatacion', methods=['GET', 'POST'])
@login_requerido
def constatacion():
    if request.method == 'POST':
        archivo = request.files.get('archivo_excel')

        if archivo and archivo.filename != '':
            try:
                # Leemos la hoja 'ID EMPRESA'. Usamos dtype=str para evitar el .0 en los números
                df = pd.read_excel(archivo, sheet_name='ID EMPRESA', dtype=str)
                
                # df.iloc[0] obtiene la primera fila de valores (que es la fila 2 en tu Excel)
                primera_fila = df.iloc[0]
                
                # Extraemos los datos e instanciamos nuestra clase Empresa
                mi_empresa = Empresa(
                    dnirl=primera_fila.get('DNI', ''),
                    rl=primera_fila.get('RL', ''),
                    et=primera_fila.get('ET', ''),
                    dir_geret=primera_fila.get('DIR GERET', ''),
                    ruc=primera_fila.get('RUC', ''),
                    cod_reg=primera_fila.get('COD REG', ''),
                    dni_ing=primera_fila.get('DNI ING', ''),
                    cip=primera_fila.get('CIP', ''),
                    nombre_ing=primera_fila.get('NOMBRE ING', '')
                )
                
                print("--- Datos extraídos de la empresa ---")
                print(f"DNI: {mi_empresa.dnirl} | RUC: {mi_empresa.ruc} | Empresa(ET): {mi_empresa.et}")
                print(f"Ingeniero: {mi_empresa.nombre_ing} (CIP: {mi_empresa.cip})")
                print("-------------------------------------")
                
                # --- LEER HOJA DE BENEFICIARIOS ---
                # Usamos dtype=str para que DNI, RUC y todo se lea como texto puro y no como número decimal
                df_beneficiarios = pd.read_excel(archivo, sheet_name='BENEFICIARIOS', dtype=str)
                
                # Como me indicaste, usamos el DNI para detenernos/filtrar.
                # dropna(subset=['DNI']) elimina cualquier fila donde el DNI esté vacío (NaN)
                df_beneficiarios = df_beneficiarios.dropna(subset=['DNI'])
                
                # Lista donde guardaremos nuestros objetos Beneficiario
                lista_beneficiarios = []
                
                # Convertimos las filas limpias en una lista de diccionarios temporales
                filas_diccionarios = df_beneficiarios.to_dict('records')
                
                # Recorremos cada fila para crear un objeto Beneficiario y agregarlo a nuestra lista
                for fila in filas_diccionarios:
                    nuevo_beneficiario = Beneficiario(
                        item=fila.get('ITEM', ''),
                        dnibene=fila.get('DNI', ''),
                        grupo_familiar=fila.get('GRUPO FAMILIAR', ''),
                        direccion_predio=fila.get('DIRECCION PREDIO', ''),
                        partida=fila.get('PARTIDA', ''),
                        sin_agua=fila.get('SIN AGUA', ''),
                        sin_saneamiento=fila.get('SIN SANEAMIENTO', ''),
                        distrito=fila.get('DISTRITO', ''),
                        provincia=fila.get('PROVINCIA', '')
                    )
                    lista_beneficiarios.append(nuevo_beneficiario)
                
                print(f"\n--- Se encontraron {len(lista_beneficiarios)} beneficiarios ---")
                
                # ====== GENERACIÓN DEL DOCUMENTO WORD ======
                if len(lista_beneficiarios) > 0:
                    
                    # Creamos un archivo ZIP en memoria para guardar todos los documentos
                    memory_zip = io.BytesIO()
                    with zipfile.ZipFile(memory_zip, 'w', zipfile.ZIP_DEFLATED) as zf:
                        
                        def safe_text(val):
                            if pd.isna(val) or val is None:
                                return ""
                            val_str = str(val)
                            if val_str.lower() == 'nan':
                                return ""
                            # Escapamos los caracteres que rompen el XML de Word
                            return val_str.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

                        # Hacemos un bucle para procesar a TODOS los beneficiarios
                        for b in lista_beneficiarios:
                            
                            # Lógica para SI/NO AGUA
                            if pd.isna(b.sin_agua) or str(b.sin_agua).strip() == '' or str(b.sin_agua).lower() == 'nan':
                                si_agua = "X"
                                no_agua = ""
                            else:
                                si_agua = ""
                                no_agua = "X"
                                
                            # Lógica para SI/NO SANEAMIENTO
                            if pd.isna(b.sin_saneamiento) or str(b.sin_saneamiento).strip() == '' or str(b.sin_saneamiento).lower() == 'nan':
                                si_saneamiento = "X"
                                no_saneamiento = ""
                            else:
                                si_saneamiento = ""
                                no_saneamiento = "X"
                                
                            # Mapeo de los datos del Excel a las etiquetas de tu Word, limpiando caracteres XML
                            contexto = {
                                'RL': safe_text(mi_empresa.rl),
                                'DNIRL': safe_text(mi_empresa.dnirl),
                                'DOMICILIADORL': safe_text(mi_empresa.dir_geret),
                                'ET': safe_text(mi_empresa.et),
                                'RUC': safe_text(mi_empresa.ruc),
                                'CODIGOREGISTRO': safe_text(mi_empresa.cod_reg),
                                'DIRECCIONPREDIO': safe_text(b.direccion_predio),
                                'PARTIDA': safe_text(b.partida),
                                'GRUPOFAMILIAR': safe_text(b.grupo_familiar),
                                'DNIBENEFICIARIO': safe_text(b.dnibene),
                                'SIAGUA': si_agua,
                                'NOAGUA': no_agua,
                                'SISANEAMIENTO': si_saneamiento,
                                'NOSANEAMIENTO': no_saneamiento,
                                'NOMBREING': safe_text(mi_empresa.nombre_ing),
                                'DNIING': safe_text(mi_empresa.dni_ing),
                                'CIP': safe_text(mi_empresa.cip),
                                'DISTRITOBENE': safe_text(b.distrito),
                                'FECHA': datetime.now().strftime("%d/%m/%Y")
                            }
                            
                            # Creamos una carpeta virtual para este beneficiario dentro del ZIP
                            nombre_limpio = str(b.grupo_familiar).replace('/', '_').replace('\\', '_')
                            carpeta_beneficiario = f"{b.dnibene}_{nombre_limpio}/"
                            
                            # 1. Cargar y generar FORMATO DE CONSTATACIÓN
                            doc_const = DocxTemplate("FORMATO DE CONSTATACIÓN.docx")
                            doc_const.render(contexto)
                            
                            doc_io_const = io.BytesIO()
                            doc_const.save(doc_io_const)
                            
                            nombre_archivo_const = f"{carpeta_beneficiario}FORMATO_CONSTATACION_{b.dnibene}.docx"
                            zf.writestr(nombre_archivo_const, doc_io_const.getvalue())
                            
                            # 2. Elegir y generar INFORME TÉCNICO (Senia o Coquitos)
                            et_lower = str(mi_empresa.et).lower()
                            if 'coquitos' in et_lower:
                                plantilla_informe = "INFORME_TECNICO_COQUITOS.docx"
                            elif 'senia' in et_lower:
                                plantilla_informe = "INFORME_TECNICO_SENIA.docx"
                            else:
                                plantilla_informe = None
                                
                            print(f"ET procesado: '{et_lower}' | Plantilla seleccionada: {plantilla_informe}")
                                
                            if plantilla_informe:
                                doc_inf = DocxTemplate(plantilla_informe)
                                doc_inf.render(contexto)
                                
                                doc_io_inf = io.BytesIO()
                                doc_inf.save(doc_io_inf)
                                
                                nombre_archivo_inf = f"{carpeta_beneficiario}INFORME_{b.dnibene}.docx"
                                zf.writestr(nombre_archivo_inf, doc_io_inf.getvalue())
                    
                    # Preparamos el ZIP para enviarlo
                    memory_zip.seek(0)
                    
                    # Devolvemos el archivo ZIP al navegador para que se descargue
                    return send_file(
                        memory_zip,
                        as_attachment=True,
                        download_name="Constataciones_Completas.zip",
                        mimetype="application/zip"
                    )

            except ValueError:
                print("Error: No se encontró la hoja llamada 'ID EMPRESA' en el Excel.")
            except Exception as e:
                print(f"Error al leer el archivo Excel: {str(e)}")

    # Renderiza el formato de constatacion
    return render_template('constatacion.html')

# 3.6 RUTA DESCARGAR PLANTILLA EXCEL
@app.route('/descargar_plantilla_fc')
@login_requerido
def descargar_plantilla_fc():
    return send_file('PLANTILLA_FC.xlsx', as_attachment=True)

# --- RUTA LOGOUT (Cierre de sesión seguro) ---
@app.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect(url_for('mostrar_login'))

# ==========================================
# GESTIÓN DE USUARIOS
# ==========================================

@app.route('/usuarios')
def listar_usuarios():
    usuarios = Usuario.query.all()
    return render_template('usuarios.html', usuarios=usuarios)

@app.route('/usuarios/crear', methods=['POST'])
def crear_usuario():
    nuevo_username = request.form.get('nuevo_usuario')
    nuevo_correo = request.form.get('nuevo_correo')
    nueva_clave = request.form.get('nueva_clave')
    
    nuevo_dni = request.form.get('nuevo_dni')
    nuevo_nombres = request.form.get('nuevo_nombres')
    nuevo_ap_paterno = request.form.get('nuevo_ap_paterno')
    nuevo_ap_materno = request.form.get('nuevo_ap_materno', '')
    
    if Usuario.query.filter_by(username=nuevo_username).first():
        flash('Error: El nombre de usuario ya existe.', 'danger')
    elif Usuario.query.filter_by(correo_electronico=nuevo_correo).first():
        flash('Error: El correo electrónico ya está registrado.', 'danger')
    else:
        try:
            hashed_pw = generate_password_hash(nueva_clave)
            nuevo_user = Usuario(
                username=nuevo_username, 
                correo_electronico=nuevo_correo, 
                password_hash=hashed_pw
            )
            db.session.add(nuevo_user)
            db.session.commit()
            
            flash(f'Usuario {nuevo_username} creado exitosamente.', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Ocurrió un error al guardar en base de datos: {str(e)}', 'danger')
            
    return redirect(url_for('listar_usuarios'))

@app.route('/usuarios/cambiar_clave/<int:id>', methods=['POST'])
def cambiar_clave(id):
    usuario = Usuario.query.get_or_404(id)
    nueva_clave = request.form.get('nueva_clave')
    
    usuario.password_hash = generate_password_hash(nueva_clave)
    db.session.commit()
    flash(f'Contraseña actualizada para {usuario.username}.', 'success')
    
    return redirect(url_for('listar_usuarios'))

@app.route('/usuarios/eliminar/<int:id>', methods=['POST'])
def eliminar_usuario(id):
    usuario = Usuario.query.get_or_404(id)
    
    if session.get('usuario') == usuario.username:
        flash('Error: No puedes eliminar el usuario con el que tienes sesión iniciada.', 'danger')
    else:
        db.session.delete(usuario)
        db.session.commit()
        flash(f'Usuario {usuario.username} eliminado.', 'success')
        
    return redirect(url_for('listar_usuarios'))

        

        
    return redirect(url_for('listar_usuarios'))

# 4. RUTA GENERAR PDF RAPIDO (Sin BD)
@app.route('/generar_rapido', methods=['POST'])
def generar_pdf_rapido():

    if not os.path.exists(NOMBRE_PLANTILLA):
        return "Error: No encuentro la plantilla (asegúrate que el nombre coincida).", 404

    try:
        
        # Creamos el objeto mi_predio con los datos del form
        mi_predio = Predio(
            direccion=request.form.get('direccion') or "",
            departamento=request.form.get('departamento') or "",
            provincia=request.form.get('provincia') or "",
            distrito=request.form.get('distrito') or "",
            manzana=request.form.get('manzana') or "",
            lote=request.form.get('lote') or "",
            sublote=request.form.get('sublote') or "",
            centro_poblado=request.form.get('centro_poblado') or "",
            referencia=request.form.get('referencia') or ""
        )

        mi_jefe = Jefe(
            nombres=request.form.get('nombres_jefe') or "",
            ap_paterno=request.form.get('ap_paterno_jefe') or "",
            ap_materno=request.form.get('ap_materno_jefe') or "",
            sit_laboral=request.form.get('sit_laboral') or "",
            dni=request.form.get('dni_jefe') or "",
            nacimiento=request.form.get('nacimiento_jefe') or "",
            estado_civil=request.form.get('estado_civil_jefe') or "",
            condicion_eco=request.form.get('condicion_eco') or "",
            grado_instruccion=request.form.get('grado_instruccion') or "",
            ocupacion=request.form.get('ocupacion') or "",
            discapacidad=request.form.get('discapacidad') or "",
            ingreso_mensual=request.form.get('ingreso_mensual') or ""
        )

        mi_conyuge = Conyuge(
            nombres=request.form.get('nombres_conyuge') or "",
            ap_paterno=request.form.get('ap_paterno_conyuge') or "",
            ap_materno=request.form.get('ap_materno_conyuge') or "",
            sit_laboral=request.form.get('sit_laboral_conyuge') or "",
            dni=request.form.get('dni_conyuge') or "",
            nacimiento=request.form.get('nacimiento_conyuge') or "",
            estado_civil=request.form.get('estado_civil_conyuge') or "",
            condicion_eco=request.form.get('condicion_conyuge') or "",
            grado_instruccion=request.form.get('grado_instruccion_conyuge') or "",
            ocupacion=request.form.get('ocupacion_conyuge') or "",
            discapacidad=request.form.get('discapacidad_conyuge') or "",
            ingreso_mensual=request.form.get('ingreso_mensual_conyuge') or ""
        )

        carga_1 = CargaFamiliar(
            nombres=request.form.get('nombres_carga_1') or "",
            dni=request.form.get('dni_carga_1') or "",
            nacimiento=request.form.get('nacimiento_carga_1') or "",
            vinculo=request.form.get('vinculo_carga_1') or "",
            instruccion=request.form.get('instruccion_carga_1') or "",
            discapacidad=request.form.get('discapacidad_carga_1') or ""
        )

        carga_2 = CargaFamiliar(
            nombres=request.form.get('nombres_carga_2') or "",
            dni=request.form.get('dni_carga_2') or "",
            nacimiento=request.form.get('nacimiento_carga_2') or "",
            vinculo=request.form.get('vinculo_carga_2') or "",
            instruccion=request.form.get('instruccion_carga_2') or "",
            discapacidad=request.form.get('discapacidad_carga_2') or ""
        )

        carga_3 = CargaFamiliar(
            nombres=request.form.get('nombres_carga_3') or "",
            dni=request.form.get('dni_carga_3') or "",
            nacimiento=request.form.get('nacimiento_carga_3') or "",
            vinculo=request.form.get('vinculo_carga_3') or "",
            instruccion=request.form.get('instruccion_carga_3') or "",
            discapacidad=request.form.get('discapacidad_carga_3') or ""
        )

        familiar_adic_1 = FamiliarAdicional(
            nombres=request.form.get('nombres_adic_1') or "",
            ap_paterno=request.form.get('ap_paterno_adic_1') or "",
            ap_materno=request.form.get('ap_materno_adic_1') or "",
            dni=request.form.get('dni_adic_1') or "",
            vinculo=request.form.get('vinculo_adic_1') or ""
        )

        mi_contacto = Contacto(
            correo=request.form.get('correo_contacto') or "",
            telefono=request.form.get('telefono_contacto') or ""
        )

        packet = crear_pdf_datos(mi_predio, mi_jefe, mi_conyuge, carga_1, carga_2, carga_3, familiar_adic_1, mi_contacto)

        new_pdf = PdfReader(packet)
        existing_pdf = PdfReader(NOMBRE_PLANTILLA)
        output = PdfWriter()

        for i in range(len(existing_pdf.pages)):
            page = existing_pdf.pages[i]
            if i < len(new_pdf.pages):
                page.merge_page(new_pdf.pages[i])
            output.add_page(page)

        output_stream = io.BytesIO()
        output.write(output_stream)

        output_stream.seek(0)
        return send_file(
            output_stream,
            as_attachment=True,
            download_name=f"Ficha_{request.form.get('dni_jefe')}.pdf",
            mimetype='application/pdf'
        )
    except Exception as e:
        return f"Ocurrió un error: {e}", 500

# 4.5 RUTA GENERAR PDF DESDE LA BD
@app.route('/generar/<int:id_ficha>', methods=['POST', 'GET'])
@login_requerido
def generar_pdf(id_ficha):
    ficha = FichaInscripcion.query.get_or_404(id_ficha)

    if not os.path.exists(NOMBRE_PLANTILLA):
        return "Error: No encuentro la plantilla (asegúrate que el nombre coincida).", 404

    try:
        # Creamos el objeto mi_predio con los datos de la BD
        mi_predio = Predio(
            direccion=ficha.predio.direccion if ficha.predio else "",
            departamento=ficha.predio.departamento if ficha.predio else "",
            provincia=ficha.predio.provincia if ficha.predio else "",
            distrito=ficha.predio.distrito if ficha.predio else "",
            manzana=ficha.predio.manzana if ficha.predio else "",
            lote=ficha.predio.lote if ficha.predio else "",
            sublote=ficha.predio.sublote if ficha.predio else "",
            centro_poblado=ficha.predio.centro_poblado if ficha.predio else "",
            referencia=ficha.predio.referencia if ficha.predio else ""
        )

        mi_jefe = Jefe(
            nombres=ficha.jefe.nombres if ficha.jefe else "",
            ap_paterno=ficha.jefe.ap_paterno if ficha.jefe else "",
            ap_materno=ficha.jefe.ap_materno if ficha.jefe else "",
            sit_laboral=ficha.jefe.sit_laboral if ficha.jefe else "",
            dni=ficha.jefe.dni if ficha.jefe else "",
            nacimiento=ficha.jefe.nacimiento if ficha.jefe else "",
            estado_civil=ficha.jefe.estado_civil if ficha.jefe else "",
            condicion_eco=ficha.jefe.condicion_eco if ficha.jefe else "",
            grado_instruccion=ficha.jefe.grado_instruccion if ficha.jefe else "",
            ocupacion=ficha.jefe.ocupacion if ficha.jefe else "",
            discapacidad=ficha.jefe.discapacidad if ficha.jefe else "",
            ingreso_mensual=ficha.jefe.ingreso_mensual if ficha.jefe else ""
        )

        mi_conyuge = Conyuge(
            nombres=ficha.conyuge.nombres if ficha.conyuge else "",
            ap_paterno=ficha.conyuge.ap_paterno if ficha.conyuge else "",
            ap_materno=ficha.conyuge.ap_materno if ficha.conyuge else "",
            sit_laboral=ficha.conyuge.sit_laboral if ficha.conyuge else "",
            dni=ficha.conyuge.dni if ficha.conyuge else "",
            nacimiento=ficha.conyuge.nacimiento if ficha.conyuge else "",
            estado_civil=ficha.conyuge.estado_civil if ficha.conyuge else "",
            condicion_eco=ficha.conyuge.condicion if ficha.conyuge else "",
            grado_instruccion=ficha.conyuge.grado_instruccion if ficha.conyuge else "",
            ocupacion=ficha.conyuge.ocupacion if ficha.conyuge else "",
            discapacidad=ficha.conyuge.discapacidad if ficha.conyuge else "",
            ingreso_mensual=ficha.conyuge.ingreso_mensual if ficha.conyuge else ""
        )

        # Map cargas
        cargas_list = ficha.cargas
        carga_1 = CargaFamiliar(
            nombres=cargas_list[0].nombres if len(cargas_list) > 0 else "",
            dni=cargas_list[0].dni if len(cargas_list) > 0 else "",
            nacimiento=cargas_list[0].nacimiento if len(cargas_list) > 0 else "",
            vinculo=cargas_list[0].vinculo if len(cargas_list) > 0 else "",
            instruccion=cargas_list[0].instruccion if len(cargas_list) > 0 else "",
            discapacidad=cargas_list[0].discapacidad if len(cargas_list) > 0 else ""
        )

        carga_2 = CargaFamiliar(
            nombres=cargas_list[1].nombres if len(cargas_list) > 1 else "",
            dni=cargas_list[1].dni if len(cargas_list) > 1 else "",
            nacimiento=cargas_list[1].nacimiento if len(cargas_list) > 1 else "",
            vinculo=cargas_list[1].vinculo if len(cargas_list) > 1 else "",
            instruccion=cargas_list[1].instruccion if len(cargas_list) > 1 else "",
            discapacidad=cargas_list[1].discapacidad if len(cargas_list) > 1 else ""
        )

        carga_3 = CargaFamiliar(
            nombres=cargas_list[2].nombres if len(cargas_list) > 2 else "",
            dni=cargas_list[2].dni if len(cargas_list) > 2 else "",
            nacimiento=cargas_list[2].nacimiento if len(cargas_list) > 2 else "",
            vinculo=cargas_list[2].vinculo if len(cargas_list) > 2 else "",
            instruccion=cargas_list[2].instruccion if len(cargas_list) > 2 else "",
            discapacidad=cargas_list[2].discapacidad if len(cargas_list) > 2 else ""
        )

        # Map adicional
        adicionales_list = ficha.adicionales
        familiar_adic_1 = FamiliarAdicional(
            nombres=adicionales_list[0].nombres if len(adicionales_list) > 0 else "",
            ap_paterno=adicionales_list[0].ap_paterno if len(adicionales_list) > 0 else "",
            ap_materno=adicionales_list[0].ap_materno if len(adicionales_list) > 0 else "",
            dni=adicionales_list[0].dni if len(adicionales_list) > 0 else "",
            vinculo=adicionales_list[0].vinculo if len(adicionales_list) > 0 else ""
        )

        mi_contacto = Contacto(
            correo=ficha.correo_contacto or "",
            telefono=ficha.telefono_contacto or ""
        )


        # --- 1. CREAMOS EL LIENZO (CANVAS) CON LOS DATOS ---
        packet = crear_pdf_datos(mi_predio, mi_jefe, mi_conyuge, carga_1, carga_2, carga_3, familiar_adic_1, mi_contacto)

        # 2. FUSIÓN (Merge)
        new_pdf = PdfReader(packet)
        existing_pdf = PdfReader(NOMBRE_PLANTILLA)
        output = PdfWriter()

        # Recorremos las páginas del original
        for i in range(len(existing_pdf.pages)):
            page = existing_pdf.pages[i]
            
            # Si nuestra "capa de datos" tiene esa página, la pegamos
            if i < len(new_pdf.pages):
                page.merge_page(new_pdf.pages[i])
            
            output.add_page(page)

        # 3. ENVIAR AL NAVEGADOR
        output_stream = io.BytesIO()
        output.write(output_stream)
        output_stream.seek(0)

        return send_file(
            output_stream,
            as_attachment=True,
            download_name=f"Ficha_{ficha.jefe.dni if ficha.jefe else ficha.id_ficha}.pdf",
            mimetype='application/pdf'
        )

    except Exception as e:
        return f"<h1>Ocurrió un error:</h1><p>{str(e)}</p>"


def format_fecha(fecha_str):
    """Convierte YYYY-MM-DD a DD/MM/YYYY"""
    if not fecha_str:
        return ""
    try:
        fecha_obj = datetime.strptime(fecha_str, '%Y-%m-%d')
        return fecha_obj.strftime('%d/%m/%Y')
    except:
        return fecha_str # Si falla, devuelve el texto original

def crear_pdf_datos(mi_predio, mi_jefe, mi_conyuge, carga_1, carga_2, carga_3, familiar_adic_1, mi_contacto):
    """
    Crea el lienzo (canvas) con los datos de los objetos modelo y lo devuelve en memoria.
    """
    packet = io.BytesIO()
    c = canvas.Canvas(packet, pagesize=A4)

    fonttype_default = "Helvetica"
    sizefont_default = 10

    c.setFont(fonttype_default, sizefont_default)

    # ==========================================
    #  PÁGINA 1: Secciones 1, 2, 3 y 4
    # ==========================================

    # --- 1. INFORMACIÓN DEL PREDIO ---
    c.drawString(18, 482, mi_predio.direccion)
    c.drawString(18, 454, mi_predio.departamento)
    c.drawString(215, 454, mi_predio.provincia)
    c.drawString(419, 454, mi_predio.distrito)
    c.drawString(18, 427, mi_predio.manzana)
    c.drawString(115, 427, mi_predio.lote)
    c.drawString(215, 427, mi_predio.sublote)
    c.drawString(317, 427, mi_predio.centro_poblado)
    c.drawString(419, 427, mi_predio.referencia)

    # --- 2. JEFE DE FAMILIA ---
    c.drawString(18, 364, mi_jefe.nombres)
    c.drawString(155, 364, mi_jefe.ap_paterno)
    c.drawString(290, 364, mi_jefe.ap_materno)
    # --- RADIO BUTTONS: SITUACIÓN LABORAL JEFE ---
    c.setFont("Helvetica", 9)
    if (mi_jefe.sit_laboral or '').upper() == 'DEPENDIENTE':
        c.drawString(429.8, 365, "X")
    elif (mi_jefe.sit_laboral or '').upper() == 'INDEPENDIENTE':
        c.drawString(508, 365, "X")
    c.setFont(fonttype_default, sizefont_default)

    c.drawString(18, 336, mi_jefe.dni)        
    # FECHA FORMATEADA
    fecha_nac_jefe_fmt = format_fecha(mi_jefe.nacimiento)
    c.drawString(155, 336, fecha_nac_jefe_fmt)
    c.drawString(290, 336, mi_jefe.estado_civil) # Select devuelve texto
    # --- RADIO BUTTONS: CONDICIÓN JEFE ---
    c.setFont("Helvetica", 9)
    if (mi_jefe.condicion_eco or '').upper() == 'FORMAL':
        c.drawString(429.8, 337, "X")
    elif (mi_jefe.condicion_eco or '').upper() == 'INFORMAL':
        c.drawString(508, 337, "X")
    c.setFont(fonttype_default, sizefont_default)

    c.drawString(18, 310, mi_jefe.grado_instruccion)
    c.drawString(155, 310, mi_jefe.ocupacion)
    # --- RADIO BUTTONS: DISCAPACIDAD JEFE (Aquí está la lógica de la X) ---
    c.setFont("Helvetica", 9)
    if (mi_jefe.discapacidad or '').upper() == 'PERMANENTE':
        c.drawString(300.6, 309, "X")
    elif (mi_jefe.discapacidad or '').upper() == 'SEVERA':
        c.drawString(368.6, 309, "X") 
    c.setFont(fonttype_default, sizefont_default)

    c.drawString(419, 310, mi_jefe.ingreso_mensual)

    # --- 3. CÓNYUGE ---
    c.drawString(18, 243, mi_conyuge.nombres)
    c.drawString(155, 243, mi_conyuge.ap_paterno)
    c.drawString(290, 243, mi_conyuge.ap_materno)
    # --- RADIO BUTTONS: SITUACIÓN LABORAL CÓNYUGE ---
    c.setFont("Helvetica", 9)
    if (mi_conyuge.sit_laboral or '').upper() == 'DEPENDIENTE':
        c.drawString(429.8, 244, "X")
    elif (mi_conyuge.sit_laboral or '').upper() == 'INDEPENDIENTE':
        c.drawString(508, 244, "X")
    c.setFont(fonttype_default, sizefont_default)

    c.drawString(18, 215, mi_conyuge.dni)
    # Usamos la función format_fecha para que salga DD/MM/YYYY
    fecha_nac_conyuge_fmt = format_fecha(mi_conyuge.nacimiento)
    c.drawString(155, 215, fecha_nac_conyuge_fmt)
    c.drawString(290, 215, mi_conyuge.estado_civil)
    # Radios Cónyuge
    # --- RADIO BUTTONS: CONDICIÓN ECONÓMICA CÓNYUGE ---
    c.setFont("Helvetica", 9)
    if (mi_conyuge.condicion_eco or '').upper() == 'FORMAL':
        c.drawString(429.8, 216, "X")
    elif (mi_conyuge.condicion_eco or '').upper() == 'INFORMAL':
        c.drawString(508, 216, "X")
    c.setFont(fonttype_default, sizefont_default)
    
    # Fila 3: Instrucción y Ocupación
    c.drawString(18, 187, mi_conyuge.grado_instruccion)
    c.drawString(155, 187, mi_conyuge.ocupacion)

    # Discapacidad Cónyuge
    c.setFont("Helvetica", 9)
    if (mi_conyuge.discapacidad or '').upper() == 'PERMANENTE':
        c.drawString(300.6, 188, "X")
    elif (mi_conyuge.discapacidad or '').upper() == 'SEVERA':
        c.drawString(368.6, 188, "X")
    c.setFont(fonttype_default, sizefont_default)

    # Ingreso Mensual
    c.drawString(419, 187, mi_conyuge.ingreso_mensual)

    # --- 4. CARGA FAMILIAR  ---

    # Fila 1
    c.drawString(38, 117, carga_1.nombres)
    c.drawString(230, 117, carga_1.dni)
    c.drawString(288, 117, format_fecha(carga_1.nacimiento))

    c.setFont("Helvetica", 7.5)
    c.drawString(365, 117, carga_1.vinculo)

    c.setFont("Helvetica", 6.9)

    inst_1 = carga_1.instruccion.strip().upper()
    if inst_1 in ["SIN INSTRUCCION", "SIN INSTRUCCIÓN"]:
        c.drawString(405, 122, "SIN")         
        c.drawString(405, 114, "INSTRUCCIÓN") 
    else:
        c.drawString(405, 117, inst_1)
    
    c.setFont(fonttype_default, sizefont_default)

    c.setFont("Helvetica", 9)
    if (carga_1.discapacidad or '').upper() == 'PERMANENTE':
        c.drawString(469.8, 121, "X")
    elif (carga_1.discapacidad or '').upper() == 'SEVERA':
        c.drawString(538, 121, "X")
    c.setFont(fonttype_default, sizefont_default)
    
    # Fila 2
    c.drawString(38, 88, carga_2.nombres)
    c.drawString(230, 88, carga_2.dni)
    c.drawString(288, 88, format_fecha(carga_2.nacimiento))

    c.setFont("Helvetica", 7.5)
    c.drawString(365, 88, carga_2.vinculo)

    c.setFont("Helvetica", 6.9)

    inst_2 = carga_2.instruccion.strip().upper()
    if inst_2 in ["SIN INSTRUCCION", "SIN INSTRUCCIÓN"]:
        c.drawString(405, 92, "SIN")         
        c.drawString(405, 84, "INSTRUCCIÓN") 
    else:
        c.drawString(405, 88, inst_2)
    
    c.setFont(fonttype_default, sizefont_default)

    c.setFont("Helvetica", 9)
    if (carga_2.discapacidad or '').upper() == 'PERMANENTE':
        c.drawString(469.8, 95.5, "X")
    elif (carga_2.discapacidad or '').upper() == 'SEVERA':
        c.drawString(538, 95.5, "X")
    c.setFont(fonttype_default, sizefont_default)

    # Fila 3
    c.drawString(38, 61, carga_3.nombres)
    c.drawString(230, 61, carga_3.dni)
    c.drawString(288, 61, format_fecha(carga_3.nacimiento))

    c.setFont("Helvetica", 7.5)
    c.drawString(365, 61, carga_3.vinculo)

    c.setFont("Helvetica", 6.9)

    inst_3 = carga_3.instruccion.strip().upper()
    if inst_3 in ["SIN INSTRUCCION", "SIN INSTRUCCIÓN"]:
        c.drawString(405, 69, "SIN")         
        c.drawString(405, 61, "INSTRUCCIÓN") 
    else:
        c.drawString(405, 61, inst_3)

    c.setFont(fonttype_default, sizefont_default)

    c.setFont("Helvetica", 9)
    if (carga_3.discapacidad or '').upper() == 'PERMANENTE':
        c.drawString(469.8, 66.5, "X")
    elif (carga_3.discapacidad or '').upper() == 'SEVERA':
        c.drawString(538, 66.5, "X")
    c.setFont(fonttype_default, sizefont_default)

    # ==========================================
    #  CAMBIO DE PÁGINA (Aquí ocurre la magia)
    # ==========================================
    c.showPage() 

    c.setFont(fonttype_default, sizefont_default)
    # A partir de aquí, las coordenadas (0,0) son de la PÁGINA 2
    
    # ==========================================
    #  PÁGINA 2: Secciones 5 y 6
    # ==========================================

    # --- 5. INFORMACIÓN ADICIONAL ---
    # Recuerda: Y empieza desde abajo. 700 es arriba de la hoja 2.
    c.drawString(38, 784, familiar_adic_1.nombres)
    c.drawString(175, 784, familiar_adic_1.ap_paterno)
    c.drawString(275, 784, familiar_adic_1.ap_materno)
    c.drawString(377, 784, familiar_adic_1.dni)
    c.drawString(477, 784, familiar_adic_1.vinculo)
    # --- 6. CONTACTO ---
    c.drawString(60, 694, mi_contacto.correo)
    c.drawString(400, 694, mi_contacto.telefono)

    c.save()
    packet.seek(0)
    return packet


# ==========================================
# GESTIÓN DE ENTIDADES TÉCNICAS
# ==========================================

@app.route('/entidades')
def listar_entidades():
    entidades = get_entidades_permitidas()
    return render_template('entidades.html', entidades=entidades)

@app.route('/entidades/crear', methods=['POST'])
def crear_entidad():
    # Datos de la Entidad
    ruc = request.form.get('ruc', '').strip()
    razon_social = request.form.get('razon_social', '').strip()
    direccion = request.form.get('direccion', '').strip()
    
    # Datos Representante Legal
    rep_dni = request.form.get('rep_dni', '').strip()
    rep_nombres = request.form.get('rep_nombres', '').strip()
    rep_ap_paterno = request.form.get('rep_ap_paterno', '').strip()
    rep_ap_materno = request.form.get('rep_ap_materno', '').strip()
    
    if EntidadTecnica.query.filter_by(ruc=ruc).first():
        flash('Error: Ya existe una Entidad Técnica con este RUC.', 'danger')
        return redirect(url_for('listar_entidades'))
        
    try:
        # 1. Crear Entidad Técnica directamente
        nueva_et = EntidadTecnica(
            ruc=ruc,
            razon_social=razon_social.upper(),
            direccion=direccion.upper() if direccion else None,
            rep_dni=rep_dni,
            rep_nombres=rep_nombres.upper(),
            rep_apellido_paterno=rep_ap_paterno.upper(),
            rep_apellido_materno=rep_ap_materno.upper() if rep_ap_materno else ''
        )
        db.session.add(nueva_et)
        db.session.commit()
        
        flash(f'Entidad Técnica {razon_social} registrada exitosamente.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Ocurrió un error al guardar en base de datos: {str(e)}', 'danger')
        
    return redirect(url_for('listar_entidades'))

@app.route('/entidades/eliminar/<int:id>', methods=['POST'])
def eliminar_entidad(id):
    entidad = EntidadTecnica.query.get_or_404(id)
    try:
        db.session.delete(entidad)
        db.session.commit()
        flash(f'Entidad Técnica {entidad.razon_social} eliminada.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'No se puede eliminar la Entidad. Es posible que tenga Expedientes asociados.', 'danger')
    return redirect(url_for('listar_entidades'))


# ==========================================
# GESTIÓN DE CÓDIGOS DE REGISTRO (Registros ET)
# ==========================================

@app.route('/registros_et')
def listar_registros():
    registros = RegistroET.query.order_by(RegistroET.anio.desc()).all()
    return render_template('registros_et.html', registros=registros)

@app.route('/registros_et/crear', methods=['POST'])
def crear_registro():
    codigo_registro = request.form.get('codigo_registro')
    anio = request.form.get('anio')
    
    # Validar que no exista ese mismo código
    existe = RegistroET.query.filter_by(codigo_registro=codigo_registro).first()
    if existe:
        flash(f'El código de registro {codigo_registro} ya existe en el sistema.', 'danger')
        return redirect(url_for('listar_registros'))
        
    try:
        nuevo_registro = RegistroET(
            codigo_registro=codigo_registro.upper(),
            anio=int(anio)
        )
        db.session.add(nuevo_registro)
        db.session.commit()
        flash(f'Código de Registro {codigo_registro} añadido exitosamente.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al guardar el registro: {str(e)}', 'danger')
        
    return redirect(url_for('listar_registros'))

@app.route('/registros_et/eliminar/<int:id>', methods=['POST'])
def eliminar_registro(id):
    registro = RegistroET.query.get_or_404(id)
    
    # Validar si ya está asignado a una entidad
    if registro.id_entidad_tecnica is not None:
        flash(f'No se puede eliminar el código {registro.codigo_registro} porque está vinculado a la entidad "{registro.entidad_tecnica.razon_social}". Primero debe desvincularlo en "Asignar Códigos".', 'danger')
        return redirect(url_for('listar_registros'))
        
    try:
        db.session.delete(registro)
        db.session.commit()
        flash(f'Registro {registro.codigo_registro} eliminado correctamente.', 'success')
    except Exception as e:
        db.session.rollback()
        flash('No se pudo eliminar el registro. Es posible que tenga dependencias.', 'danger')
    return redirect(url_for('listar_registros'))

# ==========================================
# GESTIÓN DE ASIGNACIONES DE REGISTROS ET
# ==========================================

@app.route('/asignacion_registros')
def listar_asignaciones_registros():
    # Solo mostrar registros que YA están asignados
    asignaciones = RegistroET.query.filter(RegistroET.id_entidad_tecnica.isnot(None)).order_by(RegistroET.anio.desc()).all()
    
    # Entidades que ya tienen un registro asignado (para excluirlas)
    entidades_con_registro = [reg.id_entidad_tecnica for reg in asignaciones]
    
    # Mostrar en el select solo las entidades permitidas que NO estén en la lista de asignadas
    entidades_permitidas = get_entidades_permitidas()
    entidades = [e for e in entidades_permitidas if e.id_entidad_tecnica not in entidades_con_registro]
        
    # Para el desplegable, solo mostrar registros que NO están asignados aún
    registros_libres = RegistroET.query.filter(RegistroET.id_entidad_tecnica.is_(None)).order_by(RegistroET.anio.desc()).all()
    return render_template('asignacion_registros.html', asignaciones=asignaciones, entidades=entidades, registros_libres=registros_libres)

@app.route('/asignacion_registros/crear', methods=['POST'])
def crear_asignacion_registro():
    id_entidad = request.form.get('id_entidad_tecnica')
    id_registro_et = request.form.get('id_registro_et')
    
    registro = RegistroET.query.get_or_404(id_registro_et)
    
    # Python-level validation (Doble Capa) para evitar el error crudo de SQL (uk_entidad_anio)
    existente = RegistroET.query.filter_by(id_entidad_tecnica=id_entidad, anio=registro.anio).first()
    if existente:
        flash(f'La entidad seleccionada ya tiene asignado el código {existente.codigo_registro} para el año {registro.anio}. No puede tener dos códigos en el mismo año.', 'danger')
        return redirect(url_for('listar_asignaciones_registros'))
        
    try:
        # Asignar el registro a la entidad
        registro.id_entidad_tecnica = id_entidad
        db.session.commit()
        flash('Código de Registro asignado exitosamente a la Entidad Técnica.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al asignar código de registro: {str(e)}', 'danger')
        
    return redirect(url_for('listar_asignaciones_registros'))

@app.route('/asignacion_registros/eliminar/<int:id>', methods=['POST'])
def eliminar_asignacion_registro(id):
    registro = RegistroET.query.get_or_404(id)
    try:
        # Simplemente quitamos la entidad (desasignamos), NO eliminamos el código de registro
        registro.id_entidad_tecnica = None
        db.session.commit()
        flash('Asignación de Código de Registro removida correctamente. El código ahora está libre.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al desasignar registro: {str(e)}', 'danger')
        
    return redirect(url_for('listar_asignaciones_registros'))

# ==========================================
# ASIGNACIÓN DE INGENIEROS A ET
# ==========================================

@app.route('/asignacion_ingenieros')
def listar_asignaciones():
    # Solo mostramos las asignaciones de las entidades permitidas
    entidades_permitidas = get_entidades_permitidas()
    ingenieros = Ingeniero.query.all()
    return render_template('asignacion_ingenieros.html', entidades=entidades_permitidas, ingenieros=ingenieros)

@app.route('/asignacion_ingenieros/crear', methods=['POST'])
def crear_asignacion():
    id_entidad = request.form.get('id_entidad_tecnica')
    id_ingeniero = request.form.get('id_ingeniero')
    
    try:
        entidad = EntidadTecnica.query.get_or_404(id_entidad)
        entidad.id_ingeniero_vigente = id_ingeniero
        db.session.commit()
        flash('Ingeniero asignado exitosamente a la Entidad Técnica.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al asignar ingeniero: {str(e)}', 'danger')
        
    return redirect(url_for('listar_asignaciones'))

@app.route('/asignacion_ingenieros/eliminar/<int:id>', methods=['POST'])
def eliminar_asignacion(id):
    entidad = EntidadTecnica.query.get_or_404(id)
    try:
        entidad.id_ingeniero_vigente = None
        db.session.commit()
        flash('Ingeniero desvinculado de la Entidad Técnica.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al desvincular ingeniero: {str(e)}', 'danger')
        
    return redirect(url_for('listar_asignaciones'))

# ==========================================
# GESTIÓN DE INGENIEROS
# ==========================================

@app.route('/ingenieros')
def listar_ingenieros():
    ingenieros = Ingeniero.query.all()
    return render_template('ingenieros.html', ingenieros=ingenieros)

@app.route('/ingenieros/crear', methods=['POST'])
def crear_ingeniero():
    ing_dni = request.form.get('ing_dni')
    ing_nombres = request.form.get('ing_nombres')
    ing_ap_paterno = request.form.get('ing_ap_paterno')
    ing_ap_materno = request.form.get('ing_ap_materno', '')
    ing_cip = request.form.get('ing_cip')
    
    if Ingeniero.query.filter_by(cip=ing_cip).first():
        flash('Error: Ya existe un Ingeniero registrado con ese número de CIP.', 'danger')
        return redirect(url_for('listar_ingenieros'))
        
    try:
        # Crear Ingeniero directamente
        ingeniero = Ingeniero(
            cip=ing_cip,
            dni=ing_dni,
            nombres=ing_nombres.upper(),
            apellido_paterno=ing_ap_paterno.upper(),
            apellido_materno=ing_ap_materno.upper() if ing_ap_materno else ''
        )
        db.session.add(ingeniero)
        db.session.commit()
        
        flash('Ingeniero creado exitosamente.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al guardar en base de datos: {str(e)}', 'danger')
        
    return redirect(url_for('listar_ingenieros'))

@app.route('/ingenieros/eliminar/<int:id>', methods=['POST'])
def eliminar_ingeniero(id):
    ingeniero = Ingeniero.query.get_or_404(id)
    try:
        db.session.delete(ingeniero)
        db.session.commit()
        flash('Ingeniero eliminado.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'No se puede eliminar el Ingeniero porque tiene datos vinculados (Asignaciones).', 'danger')
        
    return redirect(url_for('listar_ingenieros'))

# ==========================================
# GESTIÓN DE ASIGNACIONES DE USUARIOS-ENTIDADES
# ==========================================

@app.route('/asignacion_usuarios')
def listar_asignaciones_usuarios():
    # Obtener todos los usuarios que no son super administradores del sistema (opcional)
    usuarios = Usuario.query.all()
    entidades = EntidadTecnica.query.all()
    
    # Para la tabla, enviamos la lista de usuarios y en el HTML iteramos sus entidades
    return render_template('asignacion_usuarios.html', usuarios=usuarios, entidades=entidades)

@app.route('/asignacion_usuarios/crear', methods=['POST'])
def crear_asignacion_usuario():
    id_usuario = request.form.get('id_usuario')
    id_entidad = request.form.get('id_entidad_tecnica')
    
    usuario = Usuario.query.get_or_404(id_usuario)
    entidad = EntidadTecnica.query.get_or_404(id_entidad)
    
    if entidad in usuario.entidades:
        flash(f'El usuario {usuario.username} ya tiene asignada la entidad {entidad.razon_social}.', 'warning')
        return redirect(url_for('listar_asignaciones_usuarios'))
        
    try:
        usuario.entidades.append(entidad)
        db.session.commit()
        flash(f'Entidad {entidad.razon_social} asignada a {usuario.username} con éxito.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al asignar entidad al usuario: {str(e)}', 'danger')
        
    return redirect(url_for('listar_asignaciones_usuarios'))

@app.route('/asignacion_usuarios/eliminar/<int:id_usuario>/<int:id_entidad>', methods=['POST'])
def eliminar_asignacion_usuario(id_usuario, id_entidad):
    usuario = Usuario.query.get_or_404(id_usuario)
    entidad = EntidadTecnica.query.get_or_404(id_entidad)
    
    if entidad in usuario.entidades:
        try:
            usuario.entidades.remove(entidad)
            db.session.commit()
            flash(f'Entidad {entidad.razon_social} retirada del usuario {usuario.username}.', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error al eliminar la asignación: {str(e)}', 'danger')
    
    return redirect(url_for('listar_asignaciones_usuarios'))

        

        


# ==========================================
# GESTIÓN DE FICHAS DE INSCRIPCIÓN
# ==========================================

@app.route('/fichas')
@login_requerido
def listar_fichas():
    fichas = FichaInscripcion.query.order_by(FichaInscripcion.fecha_registro.desc()).all()
    entidades = get_entidades_permitidas()
    return render_template('fichas.html', fichas=fichas, entidades=entidades)

@app.route('/fichas/nuevo')
@login_requerido
def nueva_ficha_form():
    entidades = get_entidades_permitidas()
    return render_template('formulario_fichas.html', entidades=entidades)

@app.route('/fichas/editar/<int:id_ficha>')
@login_requerido
def editar_ficha_form(id_ficha):
    ficha = FichaInscripcion.query.get_or_404(id_ficha)
    entidades = get_entidades_permitidas()
    return render_template('formulario_fichas.html', entidades=entidades, ficha=ficha)

@app.route('/fichas/actualizar/<int:id_ficha>', methods=['POST'])
@login_requerido
def actualizar_ficha(id_ficha):
    ficha = FichaInscripcion.query.get_or_404(id_ficha)
    try:
        ficha.id_entidad_tecnica = request.form.get('id_entidad_tecnica')
        ficha.correo_contacto = request.form.get('correo_contacto', '')
        ficha.telefono_contacto = request.form.get('telefono_contacto', '')

        # Predio
        if not ficha.predio:
            ficha.predio = FichaPredio(id_ficha=ficha.id_ficha)
            db.session.add(ficha.predio)
        ficha.predio.direccion = request.form.get('direccion', '').upper()
        ficha.predio.departamento = request.form.get('departamento', '').upper()
        ficha.predio.provincia = request.form.get('provincia', '').upper()
        ficha.predio.distrito = request.form.get('distrito', '').upper()
        ficha.predio.manzana = request.form.get('manzana', '').upper()
        ficha.predio.lote = request.form.get('lote', '').upper()
        ficha.predio.sublote = request.form.get('sublote', '').upper()
        ficha.predio.centro_poblado = request.form.get('centro_poblado', '').upper()
        ficha.predio.referencia = request.form.get('referencia', '').upper()

        # Jefe
        if not ficha.jefe:
            ficha.jefe = FichaJefe(id_ficha=ficha.id_ficha)
            db.session.add(ficha.jefe)
        ficha.jefe.nombres = request.form.get('nombres_jefe', '').upper()
        ficha.jefe.ap_paterno = request.form.get('ap_paterno_jefe', '').upper()
        ficha.jefe.ap_materno = request.form.get('ap_materno_jefe', '').upper()
        ficha.jefe.dni = request.form.get('dni_jefe', '').upper()
        ficha.jefe.nacimiento = request.form.get('nacimiento_jefe', '')
        ficha.jefe.estado_civil = request.form.get('estado_civil_jefe', '').upper()
        ficha.jefe.grado_instruccion = request.form.get('grado_instruccion', '').upper()
        ficha.jefe.ocupacion = request.form.get('ocupacion', '').upper()
        ficha.jefe.discapacidad = request.form.get('discapacidad', '').upper()
        ficha.jefe.sit_laboral = request.form.get('sit_laboral', '').upper()
        ficha.jefe.condicion_eco = request.form.get('condicion_eco', '').upper()
        ficha.jefe.ingreso_mensual = request.form.get('ingreso_mensual', '')

        # Conyuge
        if not ficha.conyuge:
            ficha.conyuge = FichaConyuge(id_ficha=ficha.id_ficha)
            db.session.add(ficha.conyuge)
        ficha.conyuge.tiene_conyuge = True if request.form.get('checkTieneConyuge') == 'on' or request.form.get('nombres_conyuge') else False
        ficha.conyuge.nombres = request.form.get('nombres_conyuge', '').upper()
        ficha.conyuge.ap_paterno = request.form.get('ap_paterno_conyuge', '').upper()
        ficha.conyuge.ap_materno = request.form.get('ap_materno_conyuge', '').upper()
        ficha.conyuge.dni = request.form.get('dni_conyuge', '').upper()
        ficha.conyuge.nacimiento = request.form.get('nacimiento_conyuge', '')
        ficha.conyuge.estado_civil = request.form.get('estado_civil_conyuge', '').upper()
        ficha.conyuge.grado_instruccion = request.form.get('grado_instruccion_conyuge', '').upper()
        ficha.conyuge.ocupacion = request.form.get('ocupacion_conyuge', '').upper()
        ficha.conyuge.discapacidad = request.form.get('discapacidad_conyuge', '').upper()
        ficha.conyuge.sit_laboral = request.form.get('sit_laboral_conyuge', '').upper()
        ficha.conyuge.condicion = request.form.get('condicion_conyuge', '').upper()
        ficha.conyuge.ingreso_mensual = request.form.get('ingreso_mensual_conyuge', '')

        # Cargas (borramos y re-creamos por simplicidad)
        for c in ficha.cargas:
            db.session.delete(c)
        tiene_carga = True if request.form.get('checkTieneCarga') == 'on' or request.form.get('nombres_carga_1') else False
        if tiene_carga:
            for i in range(1, 4):
                if request.form.get(f'nombres_carga_{i}'):
                    nueva_carga = FichaCarga(
                        id_ficha=ficha.id_ficha,
                        nombres=request.form.get(f'nombres_carga_{i}', '').upper(),
                        dni=request.form.get(f'dni_carga_{i}', '').upper(),
                        nacimiento=request.form.get(f'nacimiento_carga_{i}', ''),
                        vinculo=request.form.get(f'vinculo_carga_{i}', '').upper(),
                        instruccion=request.form.get(f'instruccion_carga_{i}', '').upper(),
                        discapacidad=request.form.get(f'discapacidad_carga_{i}', '').upper()
                    )
                    db.session.add(nueva_carga)

        # Adicional
        for a in ficha.adicionales:
            db.session.delete(a)
        if request.form.get('nombres_adic_1'):
            nuevo_adic = FichaAdicional(
                id_ficha=ficha.id_ficha,
                nombres=request.form.get('nombres_adic_1', '').upper(),
                ap_paterno=request.form.get('ap_paterno_adic_1', '').upper(),
                ap_materno=request.form.get('ap_materno_adic_1', '').upper(),
                dni=request.form.get('dni_adic_1', '').upper(),
                vinculo=request.form.get('vinculo_adic_1', '').upper()
            )
            db.session.add(nuevo_adic)

        db.session.commit()
        flash('Ficha de Inscripción actualizada correctamente.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al actualizar la Ficha: {str(e)}', 'danger')

    return redirect(url_for('listar_fichas'))

@app.route('/fichas/crear', methods=['POST'])
@login_requerido
def crear_ficha():
    try:
        # 1. Crear la cabecera de la ficha
        nueva_ficha = FichaInscripcion(
            id_entidad_tecnica=request.form.get('id_entidad_tecnica'),
            correo_contacto=request.form.get('correo_contacto', ''),
            telefono_contacto=request.form.get('telefono_contacto', '')
        )
        db.session.add(nueva_ficha)
        db.session.flush() # Para obtener el id_ficha

        # 2. Crear Predio
        nuevo_predio = FichaPredio(
            id_ficha=nueva_ficha.id_ficha,
            direccion=request.form.get('direccion', '').upper(),
            departamento=request.form.get('departamento', '').upper(),
            provincia=request.form.get('provincia', '').upper(),
            distrito=request.form.get('distrito', '').upper(),
            manzana=request.form.get('manzana', '').upper(),
            lote=request.form.get('lote', '').upper(),
            sublote=request.form.get('sublote', '').upper(),
            centro_poblado=request.form.get('centro_poblado', '').upper(),
            referencia=request.form.get('referencia', '').upper()
        )
        db.session.add(nuevo_predio)

        # 3. Crear Jefe
        nuevo_jefe = FichaJefe(
            id_ficha=nueva_ficha.id_ficha,
            nombres=request.form.get('nombres_jefe', '').upper(),
            ap_paterno=request.form.get('ap_paterno_jefe', '').upper(),
            ap_materno=request.form.get('ap_materno_jefe', '').upper(),
            dni=request.form.get('dni_jefe', '').upper(),
            nacimiento=request.form.get('nacimiento_jefe', ''),
            estado_civil=request.form.get('estado_civil_jefe', '').upper(),
            grado_instruccion=request.form.get('grado_instruccion', '').upper(),
            ocupacion=request.form.get('ocupacion', '').upper(),
            discapacidad=request.form.get('discapacidad', '').upper(),
            sit_laboral=request.form.get('sit_laboral', '').upper(),
            condicion_eco=request.form.get('condicion_eco', '').upper(),
            ingreso_mensual=request.form.get('ingreso_mensual', '')
        )
        db.session.add(nuevo_jefe)

        # 4. Crear Conyuge
        nuevo_conyuge = FichaConyuge(
            id_ficha=nueva_ficha.id_ficha,
            tiene_conyuge=True if request.form.get('checkTieneConyuge') == 'on' or request.form.get('nombres_conyuge') else False,
            nombres=request.form.get('nombres_conyuge', '').upper(),
            ap_paterno=request.form.get('ap_paterno_conyuge', '').upper(),
            ap_materno=request.form.get('ap_materno_conyuge', '').upper(),
            dni=request.form.get('dni_conyuge', '').upper(),
            nacimiento=request.form.get('nacimiento_conyuge', ''),
            estado_civil=request.form.get('estado_civil_conyuge', '').upper(),
            grado_instruccion=request.form.get('grado_instruccion_conyuge', '').upper(),
            ocupacion=request.form.get('ocupacion_conyuge', '').upper(),
            discapacidad=request.form.get('discapacidad_conyuge', '').upper(),
            sit_laboral=request.form.get('sit_laboral_conyuge', '').upper(),
            condicion=request.form.get('condicion_conyuge', '').upper(),
            ingreso_mensual=request.form.get('ingreso_mensual_conyuge', '')
        )
        db.session.add(nuevo_conyuge)

        # 5. Crear Cargas
        tiene_carga = True if request.form.get('checkTieneCarga') == 'on' or request.form.get('nombres_carga_1') else False
        if tiene_carga:
            for i in range(1, 4):
                if request.form.get(f'nombres_carga_{i}'):
                    nueva_carga = FichaCarga(
                        id_ficha=nueva_ficha.id_ficha,
                        nombres=request.form.get(f'nombres_carga_{i}', '').upper(),
                        dni=request.form.get(f'dni_carga_{i}', '').upper(),
                        nacimiento=request.form.get(f'nacimiento_carga_{i}', ''),
                        vinculo=request.form.get(f'vinculo_carga_{i}', '').upper(),
                        instruccion=request.form.get(f'instruccion_carga_{i}', '').upper(),
                        discapacidad=request.form.get(f'discapacidad_carga_{i}', '').upper()
                    )
                    db.session.add(nueva_carga)

        # 6. Crear Adicional
        if request.form.get('nombres_adic_1'):
            nuevo_adic = FichaAdicional(
                id_ficha=nueva_ficha.id_ficha,
                nombres=request.form.get('nombres_adic_1', '').upper(),
                ap_paterno=request.form.get('ap_paterno_adic_1', '').upper(),
                ap_materno=request.form.get('ap_materno_adic_1', '').upper(),
                dni=request.form.get('dni_adic_1', '').upper(),
                vinculo=request.form.get('vinculo_adic_1', '').upper()
            )
            db.session.add(nuevo_adic)
        
        db.session.commit()
        flash('Ficha de Inscripción guardada correctamente en BD Normalizada.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al guardar la Ficha: {str(e)}', 'danger')
        
    return redirect(url_for('listar_fichas'))

@app.route('/fichas/eliminar/<int:id>', methods=['POST'])
@login_requerido
def eliminar_ficha(id):
    ficha = FichaInscripcion.query.get_or_404(id)
    try:
        db.session.delete(ficha)
        db.session.commit()
        flash('Ficha de Inscripción eliminada correctamente.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar la ficha: {str(e)}', 'danger')
        
    return redirect(url_for('listar_fichas'))





# =======================================
# GENERADOR WEB DE ACTAS (SIN EXCEL)
# ==========================================
@app.route('/generar_actas_web/<int:id_ficha>', methods=['POST'])
@login_requerido
def generar_actas_web(id_ficha):
    ficha = FichaInscripcion.query.get_or_404(id_ficha)
    
    partida = request.form.get('partida', '')
    fecha = request.form.get('fecha', '')
    agua = request.form.get('agua') == 'on'
    saneamiento = request.form.get('saneamiento') == 'on'
    
    try:
        # 1. Guardar/Actualizar en Base de Datos (Tabla Constatacion)
        constatacion = Constatacion.query.filter_by(id_ficha=id_ficha).first()
        from datetime import datetime
        
        # Parse fecha si existe, sino utcnow
        fecha_obj = datetime.strptime(fecha, '%Y-%m-%d').date() if fecha else datetime.utcnow().date()
            
        if not constatacion:
            constatacion = Constatacion(
                id_ficha=id_ficha,
                partida_registral=partida,
                fecha_inspeccion=fecha_obj,
                tiene_agua=agua,
                tiene_saneamiento=saneamiento
            )
            db.session.add(constatacion)
        else:
            constatacion.partida_registral = partida
            constatacion.fecha_inspeccion = fecha_obj
            constatacion.tiene_agua = agua
            constatacion.tiene_saneamiento = saneamiento
            
        db.session.commit()
        
        # 2. Generar Contexto para el Word
        jefe = ficha.jefe
        predio = ficha.predio
        entidad = ficha.entidad_tecnica
        # Asumimos que toma el primer ingeniero asignado a la ficha o entidad
        ingeniero = ficha.entidad_tecnica.ingeniero_vigente if ficha.entidad_tecnica else None
        
        contexto = {
            # Datos Constatacin
            'PARTIDA': partida,
            'FECHA': fecha_obj.strftime('%d/%m/%Y'),
            'SIAGUA': 'X' if agua else '',
            'NOAGUA': '' if agua else 'X',
            'SISANEAMIENTO': 'X' if saneamiento else '',
            'NOSANEAMIENTO': '' if saneamiento else 'X',
            
            # Datos Beneficiario y Predio
            'DNIBENEFICIARIO': jefe.dni if jefe else '',
            'GRUPOFAMILIAR': f"{jefe.ap_paterno} {jefe.ap_materno} {jefe.nombres}" if jefe else '',
            'DIRECCIONPREDIO': f"{predio.direccion} {predio.manzana} {predio.lote} {predio.centro_poblado}" if predio else '',
            'DISTRITOBENE': predio.distrito if predio else '',
            
            # Datos Entidad
            'ET': entidad.razon_social if entidad else '',
            'RUC': entidad.ruc if entidad else '',
            'RL': f"{entidad.rep_nombres} {entidad.rep_apellido_paterno} {entidad.rep_apellido_materno}" if entidad else '',
            'DNIRL': entidad.rep_dni if entidad else '',
            'DOMICILIADORL': entidad.direccion if entidad else '',
            'CODIGOREGISTRO': 'NO ESPECIFICADO',  # Esto no est nativo en la ET actual
            
            # Datos Ingeniero
            'NOMBREING': f"{ingeniero.nombres} {ingeniero.apellido_paterno} {ingeniero.apellido_materno}" if ingeniero else '',
            'DNIING': ingeniero.dni if ingeniero else '',
            'CIP': ingeniero.cip if ingeniero else ''
        }
        
        # 3. Crear ZIP en memoria
        import zipfile
        import io
        from docxtpl import DocxTemplate
        
        memory_zip = io.BytesIO()
        with zipfile.ZipFile(memory_zip, 'w', zipfile.ZIP_DEFLATED) as zf:
            
            # A) Formato de Constatacin
            try:
                doc_const = DocxTemplate('FORMATO DE CONSTATACIÓN.docx')
                doc_const.render(contexto)
                doc_io_const = io.BytesIO()
                doc_const.save(doc_io_const)
                zf.writestr(f"FORMATO_CONSTATACION_{contexto['DNIBENEFICIARIO']}.docx", doc_io_const.getvalue())
            except Exception as e:
                print("Error generando constatacin:", e)
                
            # B) Informe Tcnico
            et_lower = str(contexto['ET']).lower()
            if 'coquitos' in et_lower:
                plantilla_informe = "INFORME_TECNICO_COQUITOS.docx"
            elif 'senia' in et_lower:
                plantilla_informe = "INFORME_TECNICO_SENIA.docx"
            else:
                plantilla_informe = "INFORME_TECNICO_SENIA.docx" # Por defecto Senia
                
            try:
                doc_inf = DocxTemplate(plantilla_informe)
                doc_inf.render(contexto)
                doc_io_inf = io.BytesIO()
                doc_inf.save(doc_io_inf)
                zf.writestr(f"INFORME_TECNICO_{contexto['DNIBENEFICIARIO']}.docx", doc_io_inf.getvalue())
            except Exception as e:
                print("Error generando informe:", e)
                
        memory_zip.seek(0)
        return send_file(
            memory_zip,
            mimetype='application/zip',
            as_attachment=True,
            download_name=f"ACTAS_{contexto['DNIBENEFICIARIO']}.zip"
        )
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error al generar documentos: {str(e)}', 'danger')
        return redirect(request.referrer or url_for('fichas'))



if __name__ == '__main__':
    app.run(debug=True)
# ===