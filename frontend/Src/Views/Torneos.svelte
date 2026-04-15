<script>
  import { obtenerTorneos, inscribirseEnTorneo, obtenerMisTorneos, cancelarInscripcionTorneo } from "../Services/Api.js";
  import { token, user } from "../Store.js";
  import { get } from "svelte/store";

  let torneos = [];
  let misInscripciones = {};
  let loading = true;
  let procesando = {};

  async function cargar() {
    try {
      const currentUser = get(user);
      const currentToken = get(token);

      const [resTorneos, resMios] = await Promise.all([
        obtenerTorneos(),
        currentUser && currentToken
          ? obtenerMisTorneos(currentUser.id, currentToken)
          : Promise.resolve({ resultado: [] })
      ]);

      torneos = resTorneos.resultado || [];

      // Crear un mapa de torneo_id -> inscripción
      const mis = resMios.resultado || [];
      misInscripciones = {};
      for (const insc of mis) {
        misInscripciones[insc.torneo_id] = insc;
      }
    } catch (e) {
      console.error("Error cargando torneos:", e);
    } finally {
      loading = false;
    }
  }

  async function inscribirme(torneoId) {
    const currentUser = get(user);
    const currentToken = get(token);
    if (!currentUser || !currentToken) {
      alert("Debes iniciar sesión para inscribirte.");
      return;
    }

    procesando[torneoId] = true;
    procesando = procesando;
    try {
      await inscribirseEnTorneo(
        { torneo_id: torneoId, estudiante_id: currentUser.id },
        currentToken
      );
      alert("¡Inscripción enviada! Tu solicitud está pendiente de aprobación.");
      await cargar();
    } catch (e) {
      alert("Error al inscribirse. Es posible que ya estés inscrito.");
    } finally {
      procesando[torneoId] = false;
      procesando = procesando;
    }
  }

  async function cancelarMiInscripcion(inscripcionId, torneoId) {
    if (!confirm("¿Deseas cancelar tu inscripción en este torneo?")) return;
    const currentToken = get(token);
    procesando[torneoId] = true;
    procesando = procesando;
    try {
      await cancelarInscripcionTorneo(inscripcionId, currentToken);
      alert("Inscripción cancelada.");
      await cargar();
    } catch (e) {
      alert("Error al cancelar la inscripción.");
    } finally {
      procesando[torneoId] = false;
      procesando = procesando;
    }
  }

  function formatFecha(fecha) {
    if (!fecha) return "";
    return new Date(fecha).toLocaleDateString("es-CO", {
      day: "numeric", month: "short", year: "numeric"
    });
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

  cargar();
</script>

<div class="torneos-view">
  <div class="d-flex align-items-center mb-4">
    <div
      class="bg-primary text-white rounded-circle p-2 me-3 d-flex align-items-center justify-content-center"
      style="width: 40px; height: 40px;"
    >
      <i class="bi bi-calendar-check"></i>
    </div>
    <h4 class="fw-bold m-0">Próximos Torneos</h4>
  </div>

  {#if loading}
    <div class="text-center py-5">
      <div class="spinner-border text-primary" role="status"></div>
      <p class="mt-2 text-muted">Cargando torneos...</p>
    </div>
  {:else if torneos.length === 0}
    <div class="alert alert-light border text-center py-5 rounded-4">
      <i class="bi bi-calendar-x fs-2 text-muted mb-3 d-block"></i>
      No hay torneos programados por el momento.
    </div>
  {:else}
    <div class="list-group list-group-flush border-0">
      {#each torneos as torneo, i}
        <div
          class="list-group-item bg-transparent border-0 px-0 mb-3 animate__animated animate__fadeIn"
          style="animation-delay: {i * 0.1}s;"
        >
          <div class="card border-0 shadow-sm rounded-4 p-3">
            <div class="d-flex justify-content-between align-items-start">
              <div class="flex-grow-1">
                <div class="d-flex align-items-center gap-2 mb-2">
                  <span class="badge {getBadgeClass(torneo.estado_torneo)}">
                    <i class="bi {getEstadoIcono(torneo.estado_torneo)} me-1"></i>{torneo.estado_torneo}
                  </span>
                </div>
                <h5 class="fw-bold mb-1">{torneo.nombre}</h5>
                {#if torneo.descripcion}
                  <p class="text-muted small mb-2">{torneo.descripcion}</p>
                {/if}
                <div class="d-flex gap-2 flex-wrap mb-2">
                  {#if torneo.deporte_nombre}
                    <span class="badge bg-light text-dark border">
                      <i class="bi bi-trophy me-1"></i>{torneo.deporte_nombre}
                    </span>
                  {/if}
                  {#if torneo.lugar}
                    <span class="badge bg-light text-dark border">
                      <i class="bi bi-geo-alt me-1"></i>{torneo.lugar}
                    </span>
                  {/if}
                </div>

                <!-- Estado de inscripción del estudiante -->
                {#if misInscripciones[torneo.id]}
                  <div class="mt-2 d-flex align-items-center gap-2">
                    <span class="badge {getInscripcionBadge(misInscripciones[torneo.id].estado_inscripcion)} rounded-pill px-3">
                      <i class="bi {misInscripciones[torneo.id].estado_inscripcion === 'Aprobada' ? 'bi-check-circle' : misInscripciones[torneo.id].estado_inscripcion === 'Rechazada' ? 'bi-x-circle' : 'bi-hourglass-split'} me-1"></i>
                      {misInscripciones[torneo.id].estado_inscripcion}
                    </span>
                    {#if misInscripciones[torneo.id].estado_inscripcion === "Pendiente"}
                      <button
                        class="btn btn-sm btn-outline-danger rounded-pill px-3"
                        disabled={procesando[torneo.id]}
                        on:click={() => cancelarMiInscripcion(misInscripciones[torneo.id].inscripcion_id, torneo.id)}
                      >
                        {#if procesando[torneo.id]}
                          <span class="spinner-border spinner-border-sm me-1" role="status"></span>
                        {/if}
                        <i class="bi bi-x-lg me-1"></i>Cancelar
                      </button>
                    {/if}
                  </div>
                {/if}
              </div>
              <div class="text-end d-flex flex-column align-items-end gap-2">
                <div>
                  <div class="fw-bold text-primary">{formatFecha(torneo.fecha_inicio)}</div>
                  {#if torneo.fecha_fin}
                    <div class="text-muted x-small">Hasta {formatFecha(torneo.fecha_fin)}</div>
                  {/if}
                </div>

                <!-- Botón inscribirme -->
                {#if torneo.estado_torneo === "Inscripciones Abiertas" && !misInscripciones[torneo.id]}
                  <button
                    class="btn btn-success btn-sm rounded-pill px-3 fw-bold shadow-sm"
                    disabled={procesando[torneo.id]}
                    on:click={() => inscribirme(torneo.id)}
                  >
                    {#if procesando[torneo.id]}
                      <span class="spinner-border spinner-border-sm me-1" role="status"></span>
                    {:else}
                      <i class="bi bi-pencil-square me-1"></i>
                    {/if}
                    Inscribirme
                  </button>
                {/if}
              </div>
            </div>
          </div>
        </div>
      {/each}
    </div>
  {/if}
</div>

<style>
  .x-small {
    font-size: 0.7rem;
  }
</style>
