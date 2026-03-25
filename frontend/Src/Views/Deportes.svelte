<script>
  import { obtenerDeportesEstudiante } from "../Services/Api.js";
  import { user } from "../Store.js";
  import { get } from "svelte/store";

  let misDeportes = [];
  let loading = false;

  async function cargar() {
    loading = true;
    try {
      const currentUser = get(user);
      if (currentUser && currentUser.id) {
        const res = await obtenerDeportesEstudiante(currentUser.id);
        misDeportes = res.resultado || [];
      }
    } catch (e) {
      console.error("Error cargando mis deportes:", e);
    } finally {
      loading = false;
    }
  }

  function formatHora(hora) {
    if (!hora) return "";
    return hora.slice(0, 5);
  }

  cargar();
</script>

<div class="deportes-view">
  <div class="d-flex align-items-center mb-4">
    <div
      class="bg-primary text-white rounded-circle p-2 me-3 d-flex align-items-center justify-content-center"
      style="width: 40px; height: 40px;"
    >
      <i class="bi bi-trophy-fill"></i>
    </div>
    <h4 class="fw-bold m-0">Mis Deportes</h4>
  </div>

  {#if loading}
    <div class="text-center py-5">
      <div class="spinner-border text-primary" role="status"></div>
      <p class="mt-2 text-muted">Cargando tus deportes...</p>
    </div>
  {:else if misDeportes.length === 0}
    <div class="alert alert-light border text-center py-5 rounded-4">
      <i class="bi bi-info-circle fs-2 text-muted mb-3 d-block"></i>
      No estás inscrito en ningún deporte aún. Ve a la pestaña <strong>Inscripción</strong> para registrarte.
    </div>
  {:else}
    <div class="row g-4">
      {#each misDeportes as deporte}
        <div class="col-md-6 col-lg-4">
          <div class="card h-100 border-0 shadow-sm rounded-4 overflow-hidden sport-card">
            <div class="card-img-top bg-light d-flex align-items-center justify-content-center py-4 text-primary">
              <i class="bi bi-dribbble display-4"></i>
            </div>
            <div class="card-body p-4">
              <h5 class="fw-bold mb-3">{deporte.nombre}</h5>
              {#if deporte.dia_semana}
                <div class="d-flex align-items-center text-muted small mb-2">
                  <i class="bi bi-calendar3 me-2 text-primary"></i>
                  <span>{deporte.dia_semana}</span>
                </div>
              {/if}
              {#if deporte.hora_inicio}
                <div class="d-flex align-items-center text-muted small mb-2">
                  <i class="bi bi-clock me-2 text-primary"></i>
                  <span>{formatHora(deporte.hora_inicio)} - {formatHora(deporte.hora_fin)}</span>
                </div>
              {/if}
              {#if deporte.lugar}
                <div class="d-flex align-items-center text-muted small">
                  <i class="bi bi-geo-alt me-2 text-primary"></i>
                  <span>{deporte.lugar}</span>
                </div>
              {/if}
            </div>
          </div>
        </div>
      {/each}
    </div>
  {/if}
</div>

<style>
  .sport-card {
    transition: all 0.3s ease;
  }
  .sport-card:hover {
    transform: translateY(-8px);
    box-shadow: 0 15px 30px rgba(0, 0, 0, 0.08) !important;
  }
</style>
