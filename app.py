from flask import Flask, render_template, request, send_file, redirect, url_for, session, flash
from functools import wraps
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from datetime import datetime
import io
import os
import zipfile
import pandas as pd
from models.predio import Predio
from models.jefe import Jefe
from models.conyuge import Conyuge
from models.carga_familiar import CargaFamiliar
from models.familiar_adicional import FamiliarAdicional
from models.contacto import Contacto
from models.empresa import Empresa
from models.beneficiario import Beneficiario
from docxtpl import DocxTemplate
import jinja2
from werkzeug.security import generate_password_hash, check_password_hash
from models.database import db
from models.usuario import Usuario

app = Flask(__name__)
app.secret_key = 'clave_secreta_ptp_fipi_2025'  # Clave para firmar las sesiones

# --- CONFIGURACIÓN BASE DE DATOS ---
# Pon aquí tu cadena de conexión de Development de Neon DB.
# Ejemplo: 'postgresql://usuario:contraseña@ep-tu-bd-dev.neon.tech/tu_bd_dev?sslmode=require'
url_bd = os.environ.get('DATABASE_URL', 'PEGAR_AQUI_TU_URL_DE_NEON_DB')

if url_bd.startswith("postgres://"):
    url_bd = url_bd.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = url_bd
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Como tú diseñarás y crearás las tablas directamente en Neon DB (usando el SQL que te pasé),
# ya no necesitamos que Flask intente crear las tablas por nosotros.
with app.app_context():
    # db.create_all()  <-- Comentado para evitar que Flask modifique tu esquema de Neon DB
    
    # Try-except por si la tabla usuarios aún no ha sido creada en Neon DB
    try:
        if not Usuario.query.filter_by(username='admin').first():
            hashed_pw = generate_password_hash('1234')
            admin_user = Usuario(username='admin', password_hash=hashed_pw)
            db.session.add(admin_user)
            db.session.commit()
    except Exception as e:
        print("Aún no se ha creado la tabla usuarios en Neon DB o hay un error de conexión:", e)

# --- CONFIGURACIÓN ---
NOMBRE_PLANTILLA = "FORMULARIO DE INSCRIPCION 2025 II.pdf"  # El nombre de tu archivo PDF real

# --- DECORADOR DE PROTECCIÓN DE RUTAS ---
def login_requerido(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'usuario' not in session:
            return redirect(url_for('mostrar_login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/') 
def mostrar_login():
    return render_template('login.html')

@app.route('/validar', methods=['POST'])
def login():
    if request.method == 'POST':
        usuario = request.form.get('usuario')
        password = request.form.get('password')
        
        # Validación con Base de Datos
        user = Usuario.query.filter_by(username=usuario).first()
        
        if user and check_password_hash(user.password_hash, password):
            session['usuario'] = user.username  # Registramos al usuario en la sesión
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error='Usuario o contraseña incorrectos')
    
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
    # Renderiza el formulario que hereda de base.html
    return render_template('formulario.html')

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
    session.clear()
    return redirect(url_for('mostrar_login'))

# ==========================================
# GESTIÓN DE USUARIOS
# ==========================================

@app.route('/usuarios')
@login_requerido
def listar_usuarios():
    usuarios = Usuario.query.all()
    return render_template('usuarios.html', usuarios=usuarios)

@app.route('/usuarios/crear', methods=['POST'])
@login_requerido
def crear_usuario():
    nuevo_username = request.form.get('nuevo_usuario')
    nueva_clave = request.form.get('nueva_clave')
    
    if Usuario.query.filter_by(username=nuevo_username).first():
        flash('Error: El nombre de usuario ya existe.', 'danger')
    else:
        hashed_pw = generate_password_hash(nueva_clave)
        nuevo_user = Usuario(username=nuevo_username, password_hash=hashed_pw)
        db.session.add(nuevo_user)
        db.session.commit()
        flash(f'Usuario {nuevo_username} creado exitosamente.', 'success')
        
    return redirect(url_for('listar_usuarios'))

@app.route('/usuarios/cambiar_clave/<int:id>', methods=['POST'])
@login_requerido
def cambiar_clave(id):
    usuario = Usuario.query.get_or_404(id)
    nueva_clave = request.form.get('nueva_clave')
    
    usuario.password_hash = generate_password_hash(nueva_clave)
    db.session.commit()
    flash(f'Contraseña actualizada para {usuario.username}.', 'success')
    
    return redirect(url_for('listar_usuarios'))

@app.route('/usuarios/eliminar/<int:id>', methods=['POST'])
@login_requerido
def eliminar_usuario(id):
    usuario = Usuario.query.get_or_404(id)
    
    if session.get('usuario') == usuario.username:
        flash('Error: No puedes eliminar el usuario con el que tienes sesión iniciada.', 'danger')
    else:
        db.session.delete(usuario)
        db.session.commit()
        flash(f'Usuario {usuario.username} eliminado.', 'success')
        
    return redirect(url_for('listar_usuarios'))

# 4. RUTA GENERAR PDF (La lógica pesada)
@app.route('/generar', methods=['POST'])
def generar_pdf():

# --- AGREGA ESTO AQUÍ ---
    #print("\n" + "="*30)
    #print("--- DATOS RECIBIDOS DEL FORMULARIO ---")
    #print(request.form)  # <--- ESTO ES EL CHISMOSO
    #print("="*30 + "\n")
    # ------------------------


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
            download_name=f"Ficha_{request.form.get('dni_jefe')}.pdf",
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
    if mi_jefe.sit_laboral == 'Dependiente':
        c.drawString(429.8, 365, "X")
    elif mi_jefe.sit_laboral == 'Independiente':
        c.drawString(508, 365, "X")
    c.setFont(fonttype_default, sizefont_default)

    c.drawString(18, 336, mi_jefe.dni)        
    # FECHA FORMATEADA
    fecha_nac_jefe_fmt = format_fecha(mi_jefe.nacimiento)
    c.drawString(155, 336, fecha_nac_jefe_fmt)
    c.drawString(290, 336, mi_jefe.estado_civil) # Select devuelve texto
    # --- RADIO BUTTONS: CONDICIÓN JEFE ---
    c.setFont("Helvetica", 9)
    if mi_jefe.condicion_eco == 'Formal':
        c.drawString(429.8, 337, "X")
    elif mi_jefe.condicion_eco == 'Informal':
        c.drawString(508, 337, "X")
    c.setFont(fonttype_default, sizefont_default)

    c.drawString(18, 310, mi_jefe.grado_instruccion)
    c.drawString(155, 310, mi_jefe.ocupacion)
    # --- RADIO BUTTONS: DISCAPACIDAD JEFE (Aquí está la lógica de la X) ---
    c.setFont("Helvetica", 9)
    if mi_jefe.discapacidad == 'Permanente':
        c.drawString(300.6, 309, "X")
    elif mi_jefe.discapacidad == 'Severa':
        c.drawString(368.6, 309, "X") 
    c.setFont(fonttype_default, sizefont_default)

    c.drawString(419, 310, mi_jefe.ingreso_mensual)

    # --- 3. CÓNYUGE ---
    c.drawString(18, 243, mi_conyuge.nombres)
    c.drawString(155, 243, mi_conyuge.ap_paterno)
    c.drawString(290, 243, mi_conyuge.ap_materno)
    # --- RADIO BUTTONS: SITUACIÓN LABORAL CÓNYUGE ---
    c.setFont("Helvetica", 9)
    if mi_conyuge.sit_laboral == 'Dependiente':
        c.drawString(429.8, 244, "X")
    elif mi_conyuge.sit_laboral == 'Independiente':
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
    if mi_conyuge.condicion_eco == 'Formal':
        c.drawString(429.8, 216, "X")
    elif mi_conyuge.condicion_eco == 'Informal':
        c.drawString(508, 216, "X")
    c.setFont(fonttype_default, sizefont_default)
    
    # Fila 3: Instrucción y Ocupación
    c.drawString(18, 187, mi_conyuge.grado_instruccion)
    c.drawString(155, 187, mi_conyuge.ocupacion)

    # Discapacidad Cónyuge
    c.setFont("Helvetica", 9)
    if mi_conyuge.discapacidad == 'Permanente':
        c.drawString(300.6, 188, "X")
    elif mi_conyuge.discapacidad == 'Severa':
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
    if carga_1.discapacidad == 'Permanente':
        c.drawString(469.8, 121, "X")
    elif carga_1.discapacidad == 'Severa':
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
    if carga_2.discapacidad == 'Permanente':
        c.drawString(469.8, 95.5, "X")
    elif carga_2.discapacidad == 'Severa':
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
    if carga_3.discapacidad == 'Permanente':
        c.drawString(469.8, 66.5, "X")
    elif carga_3.discapacidad == 'Severa':
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


if __name__ == '__main__':
    app.run(debug=True)