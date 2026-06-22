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

    draw_instruccion(c, 18, 310, mi_jefe.grado_instruccion)
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

