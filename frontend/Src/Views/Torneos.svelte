<script>
  import { obtenerTorneos } from "../Services/Api.js";

  let torneos = [];
  let loading = true;

  async function cargar() {
    try {
      const res = await obtenerTorneos();
      torneos = res.resultado || [];
    } catch (e) {
      console.error("Error cargando torneos:", e);
    } finally {
      loading = false;
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
              <div>
                <span class="badge {getBadgeClass(torneo.estado_torneo)} mb-2">{torneo.estado_torneo}</span>
                <h5 class="fw-bold mb-1">{torneo.nombre}</h5>
                {#if torneo.descripcion}
                  <p class="text-muted small mb-2">{torneo.descripcion}</p>
                {/if}
                {#if torneo.deporte_nombre}
                  <span class="badge bg-light text-dark border me-2">
                    <i class="bi bi-trophy me-1"></i>{torneo.deporte_nombre}
                  </span>
                {/if}
                {#if torneo.lugar}
                  <span class="text-muted small">
                    <i class="bi bi-geo-alt me-1"></i>{torneo.lugar}
                  </span>
                {/if}
              </div>
              <div class="text-end">
                <div class="fw-bold text-primary">{formatFecha(torneo.fecha_inicio)}</div>
                {#if torneo.fecha_fin}
                  <div class="text-muted x-small">Hasta {formatFecha(torneo.fecha_fin)}</div>
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
