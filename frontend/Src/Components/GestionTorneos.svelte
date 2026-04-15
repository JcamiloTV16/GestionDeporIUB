<script>
  import { onMount } from "svelte";
  import { token, user } from "../Store.js";
  import { get } from "svelte/store";
  import {
    obtenerTorneos,
    crearTorneo,
    eliminarTorneo,
    obtenerDeportes,
    cambiarEstadoTorneo,
    obtenerInscritosTorneo,
    cambiarEstadoInscripcionTorneo
  } from "../Services/Api.js";
  import { datatable } from "../Utils/datatable.js";

  let torneos = [];
  let deportes = [];
  let loading = true;
  let mostrarFormulario = false;

  // Vista de inscritos
  let torneoSeleccionado = null;
  let inscritos = [];
  let cargandoInscritos = false;

  const ESTADOS = ["Próximamente", "Inscripciones Abiertas", "En Curso", "Finalizado"];

  let nuevoTorneo = {
    nombre: "",
    descripcion: "",
    deporte_id: "",
    fecha_inicio: "",
    fecha_fin: "",
    lugar: "",
    estado_torneo: "Próximamente"
  };

  onMount(async () => {
    await cargarTodo();
  });

  async function cargarTodo() {
    loading = true;
    try {
      const [resTorneos, resDeportes] = await Promise.all([
        obtenerTorneos(),
        obtenerDeportes()
      ]);
      torneos = resTorneos.resultado || [];
      deportes = resDeportes.resultado || [];
    } catch (e) {
      console.error("Error cargando datos:", e);
    } finally {
      loading = false;
    }
  }

  async function guardarTorneo() {
    if (!nuevoTorneo.nombre || !nuevoTorneo.fecha_inicio) {
      alert("Por favor completa al menos el nombre y la fecha de inicio.");
      return;
    }

    try {
      const currentToken = get(token);
      const currentUser = get(user);
      const datos = {
        ...nuevoTorneo,
        deporte_id: nuevoTorneo.deporte_id ? parseInt(nuevoTorneo.deporte_id) : null,
        creado_por: currentUser?.id || null
      };
      await crearTorneo(datos, currentToken);
      alert("Torneo creado exitosamente.");
      mostrarFormulario = false;
      nuevoTorneo = { nombre: "", descripcion: "", deporte_id: "", fecha_inicio: "", fecha_fin: "", lugar: "", estado_torneo: "Próximamente" };
      await cargarTodo();
    } catch (e) {
      alert("Error al crear el torneo.");
    }
  }

  async function borrarTorneo(id) {
    if (!confirm("¿Deseas eliminar este torneo?")) return;
    try {
      const currentToken = get(token);
      await eliminarTorneo(id, currentToken);
      alert("Torneo eliminado exitosamente.");
      await cargarTodo();
    } catch (e) {
      alert("Error al eliminar.");
    }
  }

  async function avanzarEstado(torneo) {
    const idx = ESTADOS.indexOf(torneo.estado_torneo);
    if (idx === -1 || idx >= ESTADOS.length - 1) {
      alert("Este torneo ya está en su estado final.");
      return;
    }
    const siguiente = ESTADOS[idx + 1];
    if (!confirm(`¿Cambiar estado de "${torneo.estado_torneo}" a "${siguiente}"?`)) return;

    try {
      const currentToken = get(token);
      await cambiarEstadoTorneo(torneo.id, siguiente, currentToken);
      alert(`Estado actualizado a "${siguiente}".`);
      await cargarTodo();
    } catch (e) {
      alert("Error al cambiar el estado del torneo.");
    }
  }

  function getSiguienteEstado(estadoActual) {
    const idx = ESTADOS.indexOf(estadoActual);
    if (idx === -1 || idx >= ESTADOS.length - 1) return null;
    return ESTADOS[idx + 1];
  }

  async function verInscritos(torneo) {
    torneoSeleccionado = torneo;
    cargandoInscritos = true;
    inscritos = [];
    try {
      const currentToken = get(token);
      const res = await obtenerInscritosTorneo(torneo.id, currentToken);
      inscritos = res.resultado || [];
    } catch (e) {
      console.error("Error cargando inscritos:", e);
    } finally {
      cargandoInscritos = false;
    }
  }

  function volverALista() {
    torneoSeleccionado = null;
    inscritos = [];
  }

  async function manejarEstadoInscripcion(inscripcionId, nuevoEstado) {
    const accion = nuevoEstado === "Aprobada" ? "aprobar" : "rechazar";
    if (!confirm(`¿Deseas ${accion} esta inscripción?`)) return;
    try {
      const currentToken = get(token);
      await cambiarEstadoInscripcionTorneo(inscripcionId, nuevoEstado, currentToken);
      alert(`Inscripción ${nuevoEstado.toLowerCase()} exitosamente.`);
      await verInscritos(torneoSeleccionado);
    } catch (e) {
      alert("Error al actualizar la inscripción.");
    }
  }

  function formatFecha(fecha) {
    if (!fecha) return "";
    return new Date(fecha).toLocaleDateString("es-CO", { day: "numeric", month: "short", year: "numeric" });
  }

  function getBadgeClass(estado) {
    switch (estado) {
      case "Inscripciones Abiertas": return "bg-success";
      case "En Curso": return "bg-primary";
      case "Finalizado": return "bg-secondary";
      default: return "bg-warning text-dark";
    }
  }

  function getInscripcionBadge(estado) {
    switch (estado) {
      case "Aprobada": return "bg-success";
      case "Rechazada": return "bg-danger";
      default: return "bg-warning text-dark";
    }
  }

  function getEstadoIcono(estado) {
    switch (estado) {
      case "Próximamente": return "bi-clock";
      case "Inscripciones Abiertas": return "bi-door-open";
      case "En Curso": return "bi-play-circle";
      case "Finalizado": return "bi-flag";
      default: return "bi-circle";
    }
  }
</script>

<div>
  {#if torneoSeleccionado}
    <!-- Vista de inscritos del torneo -->
    <div class="animate__animated animate__fadeIn">
      <div class="d-flex align-items-center gap-3 mb-4">
        <button class="btn btn-sm btn-light rounded-circle shadow-sm" on:click={volverALista} title="Volver">
          <i class="bi bi-arrow-left"></i>
        </button>
        <div>
          <h5 class="fw-bold mb-0">
            <i class="bi bi-people me-2 text-primary"></i>Inscritos — {torneoSeleccionado.nombre}
          </h5>
          <span class="text-muted small">
            <span class="badge {getBadgeClass(torneoSeleccionado.estado_torneo)} me-2">{torneoSeleccionado.estado_torneo}</span>
            {#if torneoSeleccionado.deporte_nombre}
              <i class="bi bi-trophy me-1"></i>{torneoSeleccionado.deporte_nombre}
            {/if}
          </span>
        </div>
      </div>

      <div class="card border-0 shadow-sm rounded-4 overflow-hidden">
        <div class="card-body p-0">
          {#if cargandoInscritos}
            <div class="text-center py-5">
              <div class="spinner-border text-primary" role="status"></div>
            </div>
          {:else if inscritos.length === 0}
            <div class="text-center py-5">
              <i class="bi bi-inbox fs-1 text-muted d-block mb-3"></i>
              <span class="text-muted">No hay estudiantes inscritos en este torneo.</span>
            </div>
          {:else}
            <div class="table-responsive">
              <table class="table table-hover align-middle mb-0" use:datatable={inscritos}>
                <thead>
                  <tr>
                    <th class="px-4 py-3">Estudiante</th>
                    <th class="py-3">Correo</th>
                    <th class="py-3">Fecha Inscripción</th>
                    <th class="py-3 text-center">Estado</th>
                    <th class="py-3 text-end px-4">Acciones</th>
                  </tr>
                </thead>
                <tbody>
                  {#each inscritos as inscrito}
                    <tr>
                      <td class="px-4">
                        <div class="d-flex align-items-center">
                          <div class="avatar-sm bg-primary-subtle rounded-circle me-3 d-flex align-items-center justify-content-center">
                            <i class="bi bi-person text-primary"></i>
                          </div>
                          <span class="fw-semibold">{inscrito.estudiante_nombre || "—"}</span>
                        </div>
                      </td>
                      <td class="text-muted small">{inscrito.estudiante_correo || "—"}</td>
                      <td class="text-muted small">
                        {inscrito.fecha_inscripcion ? new Date(inscrito.fecha_inscripcion).toLocaleDateString("es-CO") : "—"}
                      </td>
                      <td class="text-center">
                        <span class="badge {getInscripcionBadge(inscrito.estado_inscripcion)} rounded-pill px-3">
                          {inscrito.estado_inscripcion}
                        </span>
                      </td>
                      <td class="text-end px-4">
                        {#if inscrito.estado_inscripcion === "Pendiente"}
                          <button
                            class="btn btn-sm btn-outline-success rounded-pill px-3 me-1"
                            on:click={() => manejarEstadoInscripcion(inscrito.id, "Aprobada")}
                            title="Aprobar"
                          >
                            <i class="bi bi-check-lg me-1"></i>Aprobar
                          </button>
                          <button
                            class="btn btn-sm btn-outline-danger rounded-pill px-3"
                            on:click={() => manejarEstadoInscripcion(inscrito.id, "Rechazada")}
                            title="Rechazar"
                          >
                            <i class="bi bi-x-lg me-1"></i>Rechazar
                          </button>
                        {:else}
                          <span class="text-muted small">—</span>
                        {/if}
                      </td>
                    </tr>
                  {/each}
                </tbody>
              </table>
            </div>
          {/if}
        </div>
      </div>
    </div>
  {:else}
    <!-- Vista principal: lista de torneos -->
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h5 class="fw-bold mb-0"><i class="bi bi-calendar-event me-2 text-primary"></i>Gestión de Torneos</h5>
      <button class="btn btn-primary btn-sm rounded-pill px-3" on:click={() => (mostrarFormulario = !mostrarFormulario)}>
        <i class="bi bi-plus-lg me-1"></i>{mostrarFormulario ? "Cancelar" : "Nuevo Torneo"}
      </button>
    </div>

    {#if mostrarFormulario}
      <div class="card border-0 shadow-sm rounded-4 p-4 mb-4 animate__animated animate__fadeIn">
        <h6 class="fw-bold mb-3"><i class="bi bi-plus-circle me-2 text-primary"></i>Crear Torneo</h6>
        <form on:submit|preventDefault={guardarTorneo}>
          <div class="row g-3">
            <div class="col-md-6">
              <label class="form-label fw-medium text-muted small" for="torneo-nombre">Nombre del Torneo</label>
              <input id="torneo-nombre" type="text" class="form-control rounded-3 py-2" placeholder="Ej: Copa Universitaria" bind:value={nuevoTorneo.nombre} />
            </div>
            <div class="col-md-6">
              <label class="form-label fw-medium text-muted small" for="torneo-deporte">Deporte</label>
              <select id="torneo-deporte" class="form-select rounded-3 py-2" bind:value={nuevoTorneo.deporte_id}>
                <option value="">General (todos)</option>
                {#each deportes as d}
                  <option value={d.id}>{d.nombre}</option>
                {/each}
              </select>
            </div>
            <div class="col-md-4">
              <label class="form-label fw-medium text-muted small" for="torneo-inicio">Fecha Inicio</label>
              <input id="torneo-inicio" type="date" class="form-control rounded-3 py-2" bind:value={nuevoTorneo.fecha_inicio} />
            </div>
            <div class="col-md-4">
              <label class="form-label fw-medium text-muted small" for="torneo-fin">Fecha Fin</label>
              <input id="torneo-fin" type="date" class="form-control rounded-3 py-2" bind:value={nuevoTorneo.fecha_fin} />
            </div>
            <div class="col-md-4">
              <label class="form-label fw-medium text-muted small" for="torneo-lugar">Lugar</label>
              <input id="torneo-lugar" type="text" class="form-control rounded-3 py-2" placeholder="Ej: Cancha Principal" bind:value={nuevoTorneo.lugar} />
            </div>
            <div class="col-12">
              <label class="form-label fw-medium text-muted small" for="torneo-desc">Descripción</label>
              <input id="torneo-desc" type="text" class="form-control rounded-3 py-2" placeholder="Breve descripción..." bind:value={nuevoTorneo.descripcion} />
            </div>
          </div>
          <div class="mt-3 text-end">
            <button type="submit" class="btn btn-primary rounded-3 px-4 py-2 fw-bold">
              <i class="bi bi-save me-1"></i>Guardar Torneo
            </button>
          </div>
        </form>
      </div>
    {/if}

    {#if loading}
      <div class="text-center py-5">
        <div class="spinner-border text-primary" role="status"></div>
      </div>
    {:else if torneos.length === 0}
      <div class="alert alert-light border text-center py-5 rounded-4">
        <i class="bi bi-calendar-x fs-2 text-muted mb-3 d-block"></i>
        No hay torneos registrados. ¡Crea el primero!
      </div>
    {:else}
      <div class="list-group list-group-flush">
        {#each torneos as torneo}
          <div class="list-group-item bg-transparent border-0 px-0 mb-3">
            <div class="card border-0 shadow-sm rounded-4 p-3">
              <div class="d-flex justify-content-between align-items-start">
                <div class="flex-grow-1">
                  <div class="d-flex align-items-center gap-2 mb-2">
                    <span class="badge {getBadgeClass(torneo.estado_torneo)}">
                      <i class="bi {getEstadoIcono(torneo.estado_torneo)} me-1"></i>{torneo.estado_torneo}
                    </span>
                    {#if torneo.total_inscritos > 0}
                      <span class="badge bg-info-subtle text-info border border-info-subtle rounded-pill">
                        <i class="bi bi-people me-1"></i>{torneo.total_inscritos} inscrito{torneo.total_inscritos !== 1 ? 's' : ''}
                      </span>
                    {/if}
                  </div>
                  <h5 class="fw-bold mb-1">{torneo.nombre}</h5>
                  {#if torneo.descripcion}
                    <p class="text-muted small mb-2">{torneo.descripcion}</p>
                  {/if}
                  <div class="d-flex gap-2 flex-wrap">
                    {#if torneo.deporte_nombre}
                      <span class="badge bg-light text-dark border"><i class="bi bi-trophy me-1"></i>{torneo.deporte_nombre}</span>
                    {/if}
                    {#if torneo.lugar}
                      <span class="badge bg-light text-dark border"><i class="bi bi-geo-alt me-1"></i>{torneo.lugar}</span>
                    {/if}
                  </div>
                </div>
                <div class="text-end d-flex flex-column align-items-end gap-2">
                  <div>
                    <div class="fw-bold text-primary small">{formatFecha(torneo.fecha_inicio)}</div>
                    {#if torneo.fecha_fin}
                      <div class="text-muted" style="font-size:0.7rem">Hasta {formatFecha(torneo.fecha_fin)}</div>
                    {/if}
                  </div>
                  <div class="d-flex gap-1 flex-wrap justify-content-end">
                    {#if getSiguienteEstado(torneo.estado_torneo)}
                      <button
                        class="btn btn-outline-primary btn-sm rounded-pill px-3"
                        on:click={() => avanzarEstado(torneo)}
                        title="Avanzar a: {getSiguienteEstado(torneo.estado_torneo)}"
                      >
                        <i class="bi bi-arrow-right-circle me-1"></i>{getSiguienteEstado(torneo.estado_torneo)}
                      </button>
                    {/if}
                    <button
                      class="btn btn-outline-info btn-sm rounded-pill px-3"
                      on:click={() => verInscritos(torneo)}
                      title="Ver inscritos"
                    >
                      <i class="bi bi-people me-1"></i>Inscritos
                    </button>
                    <button class="btn btn-outline-danger btn-sm rounded-pill px-2" on:click={() => borrarTorneo(torneo.id)} title="Eliminar">
                      <i class="bi bi-trash"></i>
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        {/each}
      </div>
    {/if}
  {/if}
</div>

<style>
  .avatar-sm {
    width: 32px;
    height: 32px;
    flex-shrink: 0;
  }
</style>
