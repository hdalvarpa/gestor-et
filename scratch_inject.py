import re

html_file = r"C:\Users\hdalv\OneDrive\gestor-et\templates\fichas.html"
with open(html_file, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Buscar la celda de acciones y meter el botn
# El patrn busca '<a href="/fichas/editar/{{ ficha.id_ficha }}"' y le pone el botn justo antes
pattern_btn = r'(<a\s+href="/fichas/editar/\{\{\s*ficha\.id_ficha\s*\}\}"[^>]*>)'

new_button = """<button type="button" class="btn btn-sm btn-outline-primary me-1" title="Generar Actas" onclick="abrirModalActas({{ ficha.id_ficha }})">
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line><polyline points="10 9 9 9 8 9"></polyline></svg> Actas
</button>
\\1"""

if "abrirModalActas" not in content:
    content = re.sub(pattern_btn, new_button, content)

# 2. Inyectar el Modal
modal_code = """
<!-- Modal Generador de Actas -->
<div class="modal fade" id="modalActas" tabindex="-1" aria-hidden="true">
  <div class="modal-dialog modal-dialog-centered">
    <div class="modal-content" style="background: rgba(15,23,42,0.95); backdrop-filter: blur(16px); border: 1px solid rgba(255,255,255,0.1); color: #f1f5f9; border-radius: 20px;">
      <div class="modal-header border-0 pb-0">
        <h5 class="modal-title fw-bold">Generar Actas y Formatos</h5>
        <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="Close"></button>
      </div>
      <form id="formGenerarActas" method="POST">
          <div class="modal-body">
            <p class="text-muted small mb-4">Se generará automáticamente el Acta de Constatación y el Informe Técnico para esta Ficha de Inscripción.</p>
            
            <div class="mb-3">
                <label class="form-label text-light opacity-75">N° de Partida Registral</label>
                <input type="text" name="partida" class="form-control bg-dark border-secondary text-light" required placeholder="Ej: P01234567">
            </div>
            
            <div class="mb-3">
                <label class="form-label text-light opacity-75">Fecha de Inspección</label>
                <input type="date" name="fecha" class="form-control bg-dark border-secondary text-light" required>
            </div>
            
            <div class="mb-3 form-check form-switch">
                <input class="form-check-input" type="checkbox" name="agua" id="checkAgua">
                <label class="form-check-label text-light opacity-75" for="checkAgua">¿Cuenta con Servicio de Agua?</label>
            </div>
            
            <div class="mb-3 form-check form-switch">
                <input class="form-check-input" type="checkbox" name="saneamiento" id="checkSaneamiento">
                <label class="form-check-label text-light opacity-75" for="checkSaneamiento">¿Cuenta con Saneamiento (Desagüe)?</label>
            </div>
            
          </div>
          <div class="modal-footer border-0 pt-0">
            <button type="button" class="btn btn-secondary rounded-pill" data-bs-dismiss="modal">Cancelar</button>
            <button type="submit" class="btn btn-primary rounded-pill px-4" style="background: linear-gradient(135deg, #6366f1, #8b5cf6); border: none;">Descargar ZIP</button>
          </div>
      </form>
    </div>
  </div>
</div>

<script>
function abrirModalActas(idFicha) {
    document.getElementById('formGenerarActas').action = '/generar_actas_web/' + idFicha;
    var modal = new bootstrap.Modal(document.getElementById('modalActas'));
    modal.show();
}
</script>
"""

if "modalActas" not in content:
    content = content.replace("{% endblock %}", modal_code + "\n{% endblock %}")

with open(html_file, "w", encoding="utf-8") as f:
    f.write(content)

print("Inyectado exitosamente.")
