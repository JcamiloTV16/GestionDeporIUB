<script>
  import { createEventDispatcher } from "svelte";
  import { datatable } from "../Utils/datatable.js";
  const dispatch = createEventDispatcher();

  export let cursoSeleccionado = null;
  export let inscritos = [];
  export let deportes = [];
  export let usuarios = [];
  export let programas = [];
  export let cargandoInscritos = false;

  let estudianteId = "";

  // Filtrar solo usuarios con rol de Estudiante (ID 2)
  $: estudiantesDisponibles = usuarios.filter(u => u.rol_id === 2);

  function volverALista() {
    dispatch("volver");
  }

  function inscribir() {
    if (!estudianteId) {
      alert("Por favor seleccione un estudiante.");
      return;
    }

    const est = usuarios.find(u => u.id === parseInt(estudianteId));
    if (!est || !est.programa_id) {
      alert("Este estudiante no tiene un programa académico asignado en su perfil. Por favor actualice el perfil del usuario primero.");
      return;
    }

    dispatch("inscribir", {
      estudiante_id: est.id,
      programa_id: est.programa_id,
      deporte_id: cursoSeleccionado.deporte_id,
      horario_id: cursoSeleccionado.id
    });
    estudianteId = "";
  }
</script>

{#if cursoSeleccionado}
  <div class="animate__animated animate__fadeIn">
    <!-- Header y Botón Volver -->
    <div class="card shadow-sm border-0 rounded-4 p-4 mb-4 bg-white">
      <div class="d-flex justify-content-between align-items-center">
        <div>
          <h4 class="fw-bold mb-1 text-primary">
            <i class="bi bi-people-fill me-2"></i>Gestión de Inscritos
          </h4>
          <p class="text-muted small mb-0">
            {deportes.find(d => d.id === cursoSeleccionado.deporte_id)?.nombre || "Curso"} 
            — {cursoSeleccionado.dia_semana} ({cursoSeleccionado.hora_inicio} a {cursoSeleccionado.hora_fin})
          </p>
        </div>
        <button class="btn btn-outline-secondary rounded-pill px-3" on:click={volverALista}>
          <i class="bi bi-arrow-left me-1"></i> Volver
        </button>
      </div>
    </div>

    <!-- Formulario de Inscripción Rápida (Sin Programa Selector) -->
    <div class="card shadow-sm border-0 rounded-4 p-4 mb-4 border-start border-4 border-primary">
      <h6 class="fw-bold text-dark mb-3">Nueva Inscripción Manual</h6>
      <div class="row g-3 align-items-end">
        <div class="col-md-9">
          <label class="form-label small fw-bold text-muted" for="select-estudiante">Seleccionar Estudiante para Inscribir</label>
          <select id="select-estudiante" class="form-select" bind:value={estudianteId}>
            <option value="">-- Buscar estudiante registrado --</option>
            {#each estudiantesDisponibles as est}
              <option value={est.id}>{est.nombre} ({est.email})</option>
            {/each}
          </select>
        </div>
        <div class="col-md-3">
          <button class="btn btn-primary w-100 fw-bold" on:click={inscribir}>
            <i class="bi bi-plus-lg me-1"></i> Inscribir Ahora
          </button>
        </div>
      </div>
      {#if estudianteId}
        {@const estSel = usuarios.find(u => u.id === parseInt(estudianteId))}
        {#if estSel}
          <div class="mt-2 small">
            {#if estSel.programa_id}
              <span class="text-success"><i class="bi bi-info-circle me-1"></i> El estudiante será inscrito automáticamente a su programa registrado.</span>
            {:else}
              <span class="text-danger"><i class="bi bi-exclamation-triangle-fill me-1"></i> <strong>Error:</strong> Este estudiante no tiene programa asignado en la base de datos.</span>
            {/if}
          </div>
        {/if}
      {/if}
    </div>

    <!-- Tabla de Inscritos -->
    <div class="card shadow-sm border-0 rounded-4 p-4">
      <div class="table-responsive">
        <table class="table table-hover align-middle mb-0" use:datatable={inscritos}>
          <thead class="bg-light text-muted small text-uppercase">
            <tr>
              <th>Nombre del Estudiante</th>
              <th>Correo Electrónico</th>
              <th>Fecha Registro</th>
              <th class="text-end">Estado</th>
            </tr>
          </thead>
          <tbody>
            {#if cargandoInscritos}
              <tr><td colspan="4" class="text-center py-5">
                <div class="spinner-border text-primary" role="status"></div>
                <div class="mt-2 text-muted">Cargando lista de inscritos...</div>
              </td></tr>
            {:else if inscritos.length === 0}
              <tr><td colspan="4" class="text-center py-5 text-muted">
                <i class="bi bi-info-circle fs-4 d-block mb-2"></i>
                No hay estudiantes inscritos en este grupo todavía.
              </td></tr>
            {:else}
              {#each inscritos as inscrito}
                <tr>
                  <td>
                    <div class="fw-bold text-dark">{inscrito.nombre}</div>
                  </td>
                  <td class="text-muted small">{inscrito.correo}</td>
                  <td class="text-muted small">
                    {new Date(inscrito.fecha_inscripcion).toLocaleDateString(undefined, { day: 'numeric', month: 'short', year: 'numeric' })}
                  </td>
                  <td class="text-end">
                    <span class="badge rounded-pill {inscrito.estado ? 'bg-success-subtle text-success' : 'bg-danger-subtle text-danger'} px-3">
                      {inscrito.estado ? "Activo" : "Inactivo"}
                    </span>
                  </td>
                </tr>
              {/each}
            {/if}
          </tbody>
        </table>
      </div>
    </div>
  </div>
{:else}
  <div class="card shadow-sm border-0 rounded-4 p-5 mt-2 text-center bg-light">
    <i class="bi bi-people-fill display-2 text-secondary opacity-25 mb-3"></i>
    <h4 class="fw-bold text-dark mb-2">Consulta de Inscritos</h4>
    <p class="text-muted mx-auto" style="max-width: 400px;">
      Seleccione un curso activo desde la pestaña de Lista para visualizar y gestionar la
      lista detallada de estudiantes inscritos.
    </p>
  </div>
{/if}
