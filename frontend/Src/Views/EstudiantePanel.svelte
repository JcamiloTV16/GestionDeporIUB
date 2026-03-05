<script>
  import Deportes from "./Deportes.svelte";
  import Inscripcion from "./Inscripcion.svelte";
  import Torneos from "./Tornes.svelte";
  import Chatbot from "../Components/Chatbox.svelte";

  let vista = "deportes";
</script>

<div class="estudiante-dashboard p-4 animate__animated animate__fadeIn">
  <div class="d-flex justify-content-between align-items-center mb-4">
    <div>
      <h2 class="fw-bold text-dark m-0">Bienvenido Estudiante</h2>
      <p class="text-muted small mb-0">
        Gestiona tus disciplinas y registros deportivos
      </p>
    </div>
    <span
      class="badge bg-info-subtle text-info border border-info-subtle px-3 py-2 rounded-pill"
    >
      <i class="bi bi-mortarboard me-1"></i> Perfil Estudiante
    </span>
  </div>

  <!-- Navigation Tabs -->
  <div class="card border-0 shadow-sm rounded-4 mb-4">
    <div class="card-body p-2">
      <div class="nav nav-pills nav-justified gap-2" role="tablist">
        <button
          class="nav-link rounded-3 py-3 d-flex flex-column align-items-center transition-all {vista ===
          'deportes'
            ? 'active shadow-sm'
            : 'text-secondary bg-light'}"
          on:click={() => (vista = "deportes")}
        >
          <i class="bi bi-grid-fill mb-1 fs-5"></i>
          <span class="fw-bold small">Deportes</span>
        </button>
        <button
          class="nav-link rounded-3 py-3 d-flex flex-column align-items-center transition-all {vista ===
          'inscripcion'
            ? 'active shadow-sm'
            : 'text-secondary bg-light'}"
          on:click={() => (vista = "inscripcion")}
        >
          <i class="bi bi-pencil-square mb-1 fs-5"></i>
          <span class="fw-bold small">Inscripción</span>
        </button>
        <button
          class="nav-link rounded-3 py-3 d-flex flex-column align-items-center transition-all {vista ===
          'torneos'
            ? 'active shadow-sm'
            : 'text-secondary bg-light'}"
          on:click={() => (vista = "torneos")}
        >
          <i class="bi bi-trophy mb-1 fs-5"></i>
          <span class="fw-bold small">Torneos</span>
        </button>
      </div>
    </div>
  </div>

  <!-- Content Area -->
  <div class="view-content animate__animated animate__fadeInUp animate__faster">
    <div class="card border-0 shadow-sm rounded-4 p-4 min-vh-50">
      {#if vista === "deportes"}
        <Deportes />
      {:else if vista === "inscripcion"}
        <Inscripcion />
      {:else}
        <Torneos />
      {/if}
    </div>
  </div>

  <!-- Chatbot Container -->
  <div class="chatbot-wrapper">
    <Chatbot />
  </div>
</div>

<style>
  .transition-all {
    transition: all 0.2s ease;
  }

  .nav-link.active {
    background: linear-gradient(135deg, #0d6efd 0%, #0a58ca 100%);
  }

  .nav-link:not(.active):hover {
    background-color: #eef2f7 !important;
    color: #0d6efd !important;
  }

  .min-vh-50 {
    min-height: 50vh;
  }

  .chatbot-wrapper {
    position: fixed;
    bottom: 30px;
    right: 30px;
    z-index: 1000;
    max-width: 350px;
    width: 100%;
  }

  @media (max-width: 768px) {
    .chatbot-wrapper {
      position: relative;
      bottom: auto;
      right: auto;
      margin-top: 2rem;
      max-width: 100%;
    }
  }
</style>
