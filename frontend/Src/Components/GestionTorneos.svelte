<script>
  import { onMount } from "svelte";
  import { token, user } from "../Store.js";
  import { get } from "svelte/store";
  import { obtenerTorneos, crearTorneo, eliminarTorneo, obtenerDeportes } from "../Services/Api.js";

  let torneos = [];
  let deportes = [];
  let loading = true;
  let mostrarFormulario = false;

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
</script>

<div>
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
            <label class="form-label fw-medium text-muted small" for="torneo-estado">Estado</label>
            <select id="torneo-estado" class="form-select rounded-3 py-2" bind:value={nuevoTorneo.estado_torneo}>
              <option>Próximamente</option>
              <option>Inscripciones Abiertas</option>
              <option>En Curso</option>
              <option>Finalizado</option>
            </select>
          </div>
          <div class="col-md-6">
            <label class="form-label fw-medium text-muted small" for="torneo-lugar">Lugar</label>
            <input id="torneo-lugar" type="text" class="form-control rounded-3 py-2" placeholder="Ej: Cancha Principal" bind:value={nuevoTorneo.lugar} />
          </div>
          <div class="col-md-6">
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
              <div>
                <span class="badge {getBadgeClass(torneo.estado_torneo)} mb-2">{torneo.estado_torneo}</span>
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
              <div class="text-end">
                <div class="fw-bold text-primary small">{formatFecha(torneo.fecha_inicio)}</div>
                {#if torneo.fecha_fin}
                  <div class="text-muted" style="font-size:0.7rem">Hasta {formatFecha(torneo.fecha_fin)}</div>
                {/if}
                <button class="btn btn-outline-danger btn-sm rounded-pill mt-2 px-3" on:click={() => borrarTorneo(torneo.id)}>
                  <i class="bi bi-trash"></i>
                </button>
              </div>
            </div>
          </div>
        </div>
      {/each}
    </div>
  {/if}
</div>
