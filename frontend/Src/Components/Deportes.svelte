<script>
  import { obtenerDeportes } from "../Services/Api.js";
  let deportes = [];
  let loading = false;

  async function cargar() {
    loading = true;
    try {
      deportes = await obtenerDeportes();
    } finally {
      loading = false;
    }
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
    <h4 class="fw-bold m-0">Disciplinas Disponibles</h4>
  </div>

  {#if loading}
    <div class="text-center py-5">
      <div class="spinner-border text-primary" role="status"></div>
      <p class="mt-2 text-muted">Cargando disciplinas...</p>
    </div>
  {:else if deportes.length === 0}
    <div class="alert alert-light border text-center py-5 rounded-4">
      <i class="bi bi-info-circle fs-2 text-muted mb-3 d-block"></i>
      No hay deportes registrados por el momento.
    </div>
  {:else}
    <div class="row g-4">
      {#each deportes as deporte}
        <div class="col-md-6 col-lg-4">
          <div
            class="card h-100 border-0 shadow-sm rounded-4 overflow-hidden sport-card"
          >
            <div
              class="card-img-top bg-light d-flex align-items-center justify-content-center py-4 text-primary"
            >
              <i class="bi bi-dribbble display-4"></i>
            </div>
            <div class="card-body p-4">
              <h5 class="fw-bold mb-2">{deporte.nombre}</h5>
              <p class="text-muted small mb-0">
                Esta disciplina cuenta con entrenadores certificados y horarios
                flexibles para todos los estudiantes.
              </p>
            </div>
            <div class="card-footer bg-white border-0 p-4 pt-0">
              <button class="btn btn-outline-primary btn-sm rounded-pill w-100"
                >Ver Horarios</button
              >
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
