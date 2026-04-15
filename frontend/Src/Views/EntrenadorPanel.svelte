<script>
  import { onMount } from "svelte";
  import { token, user } from "../Store.js";
  import { get } from "svelte/store";
  import {
    obtenerEntrenadores,
    obtenerHorariosPorEntrenador,
    obtenerInscritosPorHorario,
  } from "../Services/Api.js";
  import { cerrarSesion } from "../Store.js";
  import GestionTorneos from "../Components/GestionTorneos.svelte";
  import { datatable } from "../Utils/datatable.js";

  let vista = "grupos";

  let entrenador = null;
  let grupos = [];
  let grupoSeleccionado = null;
  let inscritos = [];
  let cargandoInscritos = false;
  let cargando = true;
  let totalInscritos = 0;

  onMount(async () => {
    try {
      const currentToken = get(token);
      const currentUser = get(user);

      // 1. Buscar el entrenador que corresponde al usuario logueado
      const resEntrenadores = await obtenerEntrenadores();
      const entrenadores = resEntrenadores.resultado || [];
      // Usar == para manejar posibles diferencias de tipo (number vs string)
      entrenador = entrenadores.find((e) => e.usuario_id == currentUser.id);

      if (entrenador) {
        // 2. Cargar los grupos/horarios del entrenador
        const resGrupos = await obtenerHorariosPorEntrenador(
          entrenador.id,
          currentToken
        );
        grupos = resGrupos.resultado || [];

        // 3. Calcular total de inscritos sumando de cada grupo
        let total = 0;
        for (const grupo of grupos) {
          const res = await obtenerInscritosPorHorario(grupo.id, currentToken);
          const inscs = res.resultado || [];
          grupo._total_inscritos = inscs.length;
          total += inscs.length;
        }
        totalInscritos = total;
      }
    } catch (error) {
      console.error("Error cargando datos del entrenador:", error);
    } finally {
      cargando = false;
    }
  });

  async function verInscritos(grupo) {
    grupoSeleccionado = grupo;
    cargandoInscritos = true;
    inscritos = [];
    try {
      const currentToken = get(token);
      const res = await obtenerInscritosPorHorario(grupo.id, currentToken);
      inscritos = res.resultado || [];
    } catch (error) {
      console.error("Error cargando inscritos:", error);
    } finally {
      cargandoInscritos = false;
    }
  }

  function volverAGrupos() {
    grupoSeleccionado = null;
    inscritos = [];
  }

  function formatHora(hora) {
    if (!hora) return "";
    return hora.slice(0, 5); // HH:MM
  }
</script>

<div class="entrenador-dashboard p-4 animate__animated animate__fadeIn">
  <div class="d-flex justify-content-between align-items-center mb-4">
    <h2 class="fw-bold text-dark m-0">Panel de Entrenador</h2>
    <span
      class="badge bg-success-subtle text-success border border-success-subtle px-3 py-2 rounded-pill"
    >
      <i class="bi bi-award me-1"></i> Sesión Entrenador
    </span>
  </div>

  {#if cargando}
    <div class="text-center py-5">
      <div class="spinner-border text-primary" role="status"></div>
      <p class="text-muted mt-3">Cargando tus datos...</p>
    </div>
  {:else if !entrenador}
    <div class="alert alert-warning rounded-4">
      <i class="bi bi-exclamation-triangle me-2"></i>
      No se encontró un perfil de entrenador asociado a tu cuenta.
    </div>
  {:else}
    <!-- Tabs de navegación -->
    <div class="card border-0 shadow-sm rounded-4 mb-4">
      <div class="card-body p-2">
        <div class="nav nav-pills nav-justified gap-2" role="tablist">
          <button class="nav-link rounded-3 py-3 d-flex flex-column align-items-center {vista === 'grupos' ? 'active shadow-sm' : 'text-secondary bg-light'}" on:click={() => (vista = 'grupos')}>
            <i class="bi bi-calendar-week mb-1 fs-5"></i>
            <span class="fw-bold small">Mis Grupos</span>
          </button>
          <button class="nav-link rounded-3 py-3 d-flex flex-column align-items-center {vista === 'torneos' ? 'active shadow-sm' : 'text-secondary bg-light'}" on:click={() => (vista = 'torneos')}>
            <i class="bi bi-trophy mb-1 fs-5"></i>
            <span class="fw-bold small">Torneos</span>
          </button>
        </div>
      </div>
    </div>

    {#if vista === 'torneos'}
      <GestionTorneos />
    {:else}
    <!-- Tarjetas de resumen -->
    <div class="row g-4 mb-4">
      <div class="col-md-6">
        <div class="card border-0 shadow-sm rounded-4 p-4 bg-white h-100">
          <div class="d-flex align-items-center mb-2">
            <div class="icon-box bg-info-subtle text-info rounded-3 me-3">
              <i class="bi bi-person-check fs-4"></i>
            </div>
            <div>
              <div class="text-muted small">Total Alumnos Inscritos</div>
              <div class="fs-2 fw-bold">{totalInscritos}</div>
            </div>
          </div>
          <div class="progress mt-3" style="height: 6px;">
            <div
              class="progress-bar bg-info"
              role="progressbar"
              style="width: {Math.min(totalInscritos * 10, 100)}%"
            ></div>
          </div>
        </div>
      </div>
      <div class="col-md-6">
        <div class="card border-0 shadow-sm rounded-4 p-4 bg-white h-100">
          <div class="d-flex align-items-center mb-2">
            <div class="icon-box bg-primary-subtle text-primary rounded-3 me-3">
              <i class="bi bi-calendar3 fs-4"></i>
            </div>
            <div>
              <div class="text-muted small">Grupos / Horarios Activos</div>
              <div class="fs-2 fw-bold">{grupos.length}</div>
            </div>
          </div>
          <div class="progress mt-3" style="height: 6px;">
            <div
              class="progress-bar bg-primary"
              role="progressbar"
              style="width: {Math.min(grupos.length * 20, 100)}%"
            ></div>
          </div>
        </div>
      </div>
    </div>

    <!-- Vista de grupos o de inscritos -->
    {#if !grupoSeleccionado}
      <!-- Tabla de grupos -->
      <div class="card border-0 shadow-sm rounded-4 overflow-hidden">
        <div class="card-header bg-white border-bottom py-3 px-4">
          <h5 class="fw-bold mb-0">
            <i class="bi bi-calendar-week me-2 text-primary"></i>Mis Grupos
          </h5>
        </div>
        <div class="card-body p-0">
          <div class="table-responsive">
            <table class="table table-hover align-middle mb-0" use:datatable={grupos}>
              <thead>
                <tr>
                  <th class="px-4 py-3">Deporte</th>
                  <th class="py-3">Día</th>
                  <th class="py-3">Horario</th>
                  <th class="py-3">Lugar</th>
                  <th class="py-3 text-center">Inscritos</th>
                  <th class="py-3 text-end px-4">Acciones</th>
                </tr>
              </thead>
              <tbody>
                {#if grupos.length === 0}
                  <tr>
                    <td colspan="6" class="text-center py-5">
                      <i class="bi bi-calendar-x fs-1 text-muted d-block mb-3"
                      ></i>
                      <span class="text-muted"
                        >No tienes grupos asignados aún.</span
                      >
                    </td>
                  </tr>
                {:else}
                  {#each grupos as grupo}
                    <tr>
                      <td class="px-4">
                        <span class="fw-semibold"
                          >{grupo.deporte_nombre || "Sin deporte"}</span
                        >
                      </td>
                      <td>
                        <span class="badge bg-light text-dark border rounded-pill px-3"
                          >{grupo.dia_semana}</span
                        >
                      </td>
                      <td class="text-muted small">
                        {formatHora(grupo.hora_inicio)} - {formatHora(grupo.hora_fin)}
                      </td>
                      <td class="text-muted small">
                        {grupo.lugar || "—"}
                      </td>
                      <td class="text-center">
                        <span class="badge bg-info-subtle text-info border rounded-pill px-3">
                          {grupo._total_inscritos || 0}
                        </span>
                      </td>
                      <td class="text-end px-4">
                        <button
                          class="btn btn-outline-primary btn-sm rounded-pill px-3"
                          on:click={() => verInscritos(grupo)}
                        >
                          <i class="bi bi-people me-1"></i> Ver estudiantes
                        </button>
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
      <!-- Vista de inscritos de un grupo -->
      <div class="card border-0 shadow-sm rounded-4 overflow-hidden">
        <div
          class="card-header bg-white border-bottom py-3 px-4 d-flex align-items-center gap-3"
        >
          <button
            class="btn btn-sm btn-light rounded-circle"
            on:click={volverAGrupos}
            title="Volver"
          >
            <i class="bi bi-arrow-left"></i>
          </button>
          <h5 class="fw-bold mb-0">
            Estudiantes — {grupoSeleccionado.deporte_nombre}
            <span class="text-muted fw-normal fs-6 ms-2">
              {grupoSeleccionado.dia_semana}
              {formatHora(grupoSeleccionado.hora_inicio)}-{formatHora(grupoSeleccionado.hora_fin)}
            </span>
          </h5>
        </div>
        <div class="card-body p-0">
          {#if cargandoInscritos}
            <div class="text-center py-5">
              <div class="spinner-border text-primary" role="status"></div>
            </div>
          {:else}
            <div class="table-responsive">
              <table class="table table-hover align-middle mb-0" use:datatable={inscritos}>
                <thead>
                  <tr>
                    <th class="px-4 py-3">Estudiante</th>
                    <th class="py-3">Correo</th>
                    <th class="py-3">Fecha Inscripción</th>
                  </tr>
                </thead>
                <tbody>
                  {#if inscritos.length === 0}
                    <tr>
                      <td colspan="3" class="text-center py-5">
                        <i class="bi bi-inbox fs-1 text-muted d-block mb-3"
                        ></i>
                        <span class="text-muted"
                          >No hay estudiantes inscritos en este grupo.</span
                        >
                      </td>
                    </tr>
                  {:else}
                    {#each inscritos as inscrito}
                      <tr>
                        <td class="px-4">
                          <div class="d-flex align-items-center">
                            <div
                              class="avatar-sm bg-primary-subtle rounded-circle me-3 d-flex align-items-center justify-content-center"
                            >
                              <i class="bi bi-person text-primary"></i>
                            </div>
                            <span class="fw-semibold"
                              >{inscrito.nombre || inscrito.usuario_nombre || "—"}</span
                            >
                          </div>
                        </td>
                        <td class="text-muted small"
                          >{inscrito.correo || inscrito.email || "—"}</td
                        >
                        <td class="text-muted small">
                          {inscrito.create_
                            ? new Date(inscrito.create_).toLocaleDateString("es-CO")
                            : "—"}
                        </td>
                      </tr>
                    {/each}
                  {/if}
                </tbody>
              </table>
            </div>
          {/if}
        </div>
      </div>
    {/if}
    {/if}
    {/if}
</div>

<style>
  .icon-box {
    width: 48px;
    height: 48px;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
  }

  .avatar-sm {
    width: 32px;
    height: 32px;
    flex-shrink: 0;
  }
</style>
