from flask import Flask, render_template, request, send_file, redirect, url_for
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from datetime import datetime
import io
import os
from models.predio import Predio
from models.jefe import Jefe
from models.conyuge import Conyuge
from models.carga_familiar import CargaFamiliar
from models.familiar_adicional import FamiliarAdicional
from models.contacto import Contacto

app = Flask(__name__)

# --- CONFIGURACIÓN ---
NOMBRE_PLANTILLA = "FORMULARIO DE INSCRIPCION 2025 II.pdf"  # El nombre de tu archivo PDF real
USUARIO_ADMIN = "admin"
CLAVE_ADMIN = "1234"

@app.route('/') 
def mostrar_login():
    return render_template('login.html')

@app.route('/validar', methods=['POST'])
def login():
    if request.method == 'POST':
        usuario = request.form.get('usuario')
        password = request.form.get('password')
        
        # Validación simple
        if usuario == USUARIO_ADMIN and password == CLAVE_ADMIN:
            # ¡Aquí está el cambio! Ahora redirige al Dashboard, no al formulario directo
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error='Usuario o contraseña incorrectos')
    
    return render_template('login.html')

# 2. RUTA DASHBOARD (La bienvenida)
@app.route('/dashboard')
def dashboard():
    # Renderiza la página de bienvenida que hereda de base.html
    return render_template('dashboard.html')

# 3. RUTA FORMULARIO (La herramienta)
@app.route('/formulario')
def formulario():
    # Renderiza el formulario que hereda de base.html
    return render_template('formulario.html')

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
        #packet = io.BytesIO()
        # 1. CREAMOS EL LIENZO (CANVAS)
        packet = io.BytesIO()
        c = canvas.Canvas(packet, pagesize=A4)

        fonttype_default = "Helvetica"
        sizefont_default = 10

        c.setFont(fonttype_default, sizefont_default)
        # ==========================================
        #  PÁGINA 1: Secciones 1, 2, 3 y 4
        # ==========================================
        
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

        # FINALIZAR
        c.save()
        packet.seek(0)

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

if __name__ == '__main__':
    app.run(debug=True)