<script>
  import { cerrarSesion } from "../Store.js";
  import "../Styles/AdminPanel.css";

  let vistaActual = "dashboard";

  // -- LÓGICA: CERRAR SESIÓN --
  function manejarSalida() {
    cerrarSesion();
  }
</script>

<div class="contenedor-aplicativo">
  <div class="sub-menu-admin bg-white border-bottom px-4 d-flex gap-3">
    <button
      class="btn-pestana {vistaActual === 'dashboard' ? 'activa' : ''}"
      on:click={() => (vistaActual = "dashboard")}
    >
      <i class="bi bi-pie-chart-fill me-2"></i>Dashboard Informativo
    </button>
    <button
      class="btn-pestana {vistaActual === 'deportes' ? 'activa' : ''}"
      on:click={() => (vistaActual = "deportes")}
    >
      <i class="bi bi-tools me-2"></i>Gestión de Deportes
    </button>
    <button
      class="btn-pestana {vistaActual === 'usuarios' ? 'activa' : ''}"
      on:click={() => (vistaActual = "usuarios")}
    >
      <i class="bi bi-people me-2"></i>Gestión de Usuarios
    </button>
    <button
      class="btn-pestana {vistaActual === 'auditorias' ? 'activa' : ''}"
      on:click={() => (vistaActual = "auditorias")}
    >
      <i class="bi bi-calendar me-2"></i>Auditorias
    </button>
  </div>

  <main class="contenido-principal p-4">
    <!-- Vista dashboard -->
    {#if vistaActual === "dashboard"}
      <section class="animate__animated animate__fadeIn">
        <div class="d-flex justify-content-between align-items-center mb-4">
          <h2 class="fw-bold text-dark">Análisis de Datos (PowerBI)</h2>
          <span class="badge bg-success-subtle text-success border px-3 py-2"
            >Datos en Tiempo Real</span
          >
        </div>

        <div class="tarjeta-reporte shadow-sm rounded-4 bg-white p-2">
          <div
            class="placeholder-visual d-flex flex-column align-items-center justify-content-center"
          >
            <i class="bi bi-cpu fs-1 text-primary mb-3"></i>
            <p class="text-muted fw-medium">
              Esperando conexión con el reporte de PowerBI...
            </p>
          </div>
        </div>
      </section>
    {:else if vistaActual === "deportes"}
      <!-- Vista Gestión deportes -->
      <section class="animate__animated animate__fadeIn">
        <h2 class="fw-bold text-dark mb-4">Administrar Deportes</h2>
        <p class="text-muted">
          Utilice este módulo para agregar o editar los deportes ofrecidos por
          la IUB.
        </p>
      </section>
    {:else if vistaActual === "usuarios"}
      <!-- Vista Gestión usuarios -->
      <section class="animate__animated animate__fadeIn">
        <h2 class="fw-bold text-dark mb-4">Administrar Usuarios</h2>
        <p class="text-muted">
          Utilice este módulo para agregar o editar los usuarios de la IUB.
        </p>
      </section>
    {:else if vistaActual === "auditorias"}
      <!-- Vista Auditorias -->
      <section class="animate__animated animate__fadeIn">
        <h2 class="fw-bold text-dark mb-4">Administrar Auditorias</h2>
        <p class="text-muted">
          Utilice este módulo para agregar o editar las auditorias de la IUB.
        </p>
      </section>
    {/if}
  </main>
</div>
