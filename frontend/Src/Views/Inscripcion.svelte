<script>
  import { obtenerDeportes, obtenerHorariosPorDeporte, inscribirEstudiante } from "../Services/Api.js";
  import { user, token } from "../Store.js";
  import { get } from "svelte/store";

  let nombre = "";
  let estudiante_id = null;
  let programa_id = null;
  let deporte_id = "";
  let horario_id = "";
  let deportes = [];
  let horarios = [];
  let loading = false;
  let cargandoHorarios = false;
  let success = false;
  let errorMsg = "";

  // Recuperar datos del usuario logueado
  user.subscribe((v) => {
    if (v) {
      nombre = v.nombre;
      estudiante_id = v.id;
      programa_id = v.programa_id;
    }
  });

  async function cargar() {
    try {
      const res = await obtenerDeportes();
      deportes = res.resultado || [];
    } catch (e) {
      console.error("Error cargando deportes:", e);
    }
  }

  async function onDeporteChange() {
    horario_id = "";
    horarios = [];
    if (!deporte_id) return;

    cargandoHorarios = true;
    try {
      const res = await obtenerHorariosPorDeporte(deporte_id);
      horarios = res.resultado || [];
    } catch (e) {
      console.error("Error cargando horarios:", e);
    } finally {
      cargandoHorarios = false;
    }
  }

  function formatHora(hora) {
    if (!hora) return "";
    return hora.slice(0, 5);
  }

  async function inscribirse() {
    if (!deporte_id || !horario_id) return;
    if (!programa_id) {
       errorMsg = "Tu perfil no tiene un programa académico asignado. Contacta al administrador.";
       return;
    }

    loading = true;
    errorMsg = "";
    try {
      const currentToken = get(token);
      const datos = {
        estudiante_id: estudiante_id,
        deporte_id: parseInt(deporte_id),
        programa_id: programa_id,
        horario_id: parseInt(horario_id)
      };
      
      const res = await inscribirEstudiante(datos, currentToken);
      if (res.id) {
        success = true;
        deporte_id = "";
        horario_id = "";
        horarios = [];
        setTimeout(() => (success = false), 5000);
      } else {
        errorMsg = res.detail || "No se pudo completar la inscripción.";
      }
    } catch (e) {
      errorMsg = "Error de conexión con el servidor.";
    } finally {
      loading = false;
    }
  }

  cargar();
</script>

<div class="inscripcion-view">
  <div class="row justify-content-center">
    <div class="col-lg-8">
      <div class="d-flex align-items-center mb-4">
        <div
          class="bg-primary text-white rounded-circle p-2 me-3 d-flex align-items-center justify-content-center"
          style="width: 40px; height: 40px;"
        >
          <i class="bi bi-pencil-square"></i>
        </div>
        <h4 class="fw-bold m-0 text-dark">Formulario de Inscripción</h4>
      </div>

      {#if success}
        <div
          class="alert alert-success border-0 shadow-sm rounded-4 mb-4 animate__animated animate__fadeIn"
        >
          <i class="bi bi-check-circle-fill me-2"></i> ¡Inscripción exitosa! Ya puedes
          ver tu registro en el panel.
        </div>
      {/if}

      {#if errorMsg}
        <div
          class="alert alert-danger border-0 shadow-sm rounded-4 mb-4 animate__animated animate__shakeX"
        >
          <i class="bi bi-exclamation-triangle-fill me-2"></i> {errorMsg}
        </div>
      {/if}

      <div class="card border-0 bg-white shadow-sm rounded-4 p-4 p-md-5">
        <div class="mb-4">
          <label
            for="studentName"
            class="form-label fw-bold text-muted small text-uppercase"
            >Nombre Completo</label
          >
          <div class="input-group">
            <span class="input-group-text bg-light border-0 rounded-start-3"
              ><i class="bi bi-person text-primary"></i></span
            >
            <input
              id="studentName"
              class="form-control border-light bg-light rounded-end-3 py-3"
              bind:value={nombre}
              readonly
            />
          </div>
        </div>

        <div class="mb-4">
          <label
            for="sportSelect"
            class="form-label fw-bold text-muted small text-uppercase"
            >Disciplina Deportiva</label
          >
          <div class="input-group">
            <span class="input-group-text bg-light border-0 rounded-start-3"
              ><i class="bi bi-award text-primary"></i></span
            >
            <select
              id="sportSelect"
              class="form-select border-light bg-light rounded-end-3 py-3"
              bind:value={deporte_id}
              on:change={onDeporteChange}
            >
              <option value="">-- Selecciona una disciplina --</option>
              {#each deportes as d}
                <option value={d.id}>{d.nombre}</option>
              {/each}
            </select>
          </div>
        </div>

        <!-- Selector de Horario/Grupo -->
        {#if deporte_id}
          <div class="mb-5">
            <label
              for="horarioSelect"
              class="form-label fw-bold text-muted small text-uppercase"
              >Grupo / Horario</label
            >
            {#if cargandoHorarios}
              <div class="text-center py-3">
                <div class="spinner-border spinner-border-sm text-primary" role="status"></div>
                <span class="ms-2 text-muted small">Cargando grupos...</span>
              </div>
            {:else if horarios.length === 0}
              <div class="alert alert-light border rounded-4 mb-0">
                <i class="bi bi-info-circle me-1"></i> No hay grupos disponibles para esta disciplina.
              </div>
            {:else}
              <div class="input-group">
                <span class="input-group-text bg-light border-0 rounded-start-3"
                  ><i class="bi bi-calendar3 text-primary"></i></span
                >
                <select
                  id="horarioSelect"
                  class="form-select border-light bg-light rounded-end-3 py-3"
                  bind:value={horario_id}
                >
                  <option value="">-- Selecciona un grupo --</option>
                  {#each horarios as h}
                    <option value={h.id}>
                      {h.dia_semana} | {formatHora(h.hora_inicio)} - {formatHora(h.hora_fin)} | {h.lugar || "Sin lugar"}
                    </option>
                  {/each}
                </select>
              </div>
            {/if}
          </div>
        {/if}

        <button
          class="btn btn-primary btn-lg w-100 rounded-3 py-3 fw-bold shadow-sm"
          on:click={inscribirse}
          disabled={loading || !deporte_id || !horario_id}
        >
          {#if loading}
            <span class="spinner-border spinner-border-sm me-2"></span> Procesando...
          {:else}
            Confirmar Inscripción
          {/if}
        </button>
      </div>
    </div>
  </div>
</div>

<style>
  .form-control:focus,
  .form-select:focus {
    box-shadow: 0 0 0 0.25rem rgba(13, 110, 253, 0.1);
  }
</style>
