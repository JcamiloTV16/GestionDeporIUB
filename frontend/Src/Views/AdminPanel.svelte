<script>
  import { obtenerDeportes, agregarDeporte } from "../Services/Api.js";

  let deportes = [];
  let nuevoNombre = "";
  let loading = false;

  async function cargar() {
    loading = true;
    try {
      deportes = await obtenerDeportes();
    } finally {
      loading = false;
    }
  }

  async function agregar() {
    if (!nuevoNombre.trim()) return;
    await agregarDeporte({ nombre: nuevoNombre });
    nuevoNombre = "";
    cargar();
  }

  cargar();
</script>

<div class="admin-dashboard p-4 animate__animated animate__fadeIn">
  <div class="d-flex justify-content-between align-items-center mb-4">
    <h2 class="fw-bold text-dark m-0">Panel de Administración</h2>
    <span
      class="badge bg-primary-subtle text-primary border border-primary-subtle px-3 py-2 rounded-pill"
    >
      <i class="bi bi-shield-check me-1"></i> Modo Administrador
    </span>
  </div>

  <!-- Stats Cards -->
  <div class="row g-4 mb-5">
    <div class="col-md-4">
      <div
        class="card border-0 shadow-sm rounded-4 p-3 bg-white h-100 stat-card"
      >
        <div class="d-flex align-items-center">
          <div class="icon-box bg-primary-subtle text-primary rounded-3 me-3">
            <i class="bi bi-dribbble fs-4"></i>
          </div>
          <div>
            <div class="text-muted small">Deportes</div>
            <div class="fs-3 fw-bold">{deportes.length}</div>
          </div>
        </div>
      </div>
    </div>
    <div class="col-md-4">
      <div
        class="card border-0 shadow-sm rounded-4 p-3 bg-white h-100 stat-card"
      >
        <div class="d-flex align-items-center">
          <div class="icon-box bg-success-subtle text-success rounded-3 me-3">
            <i class="bi bi-people fs-4"></i>
          </div>
          <div>
            <div class="text-muted small">Usuarios</div>
            <div class="fs-3 fw-bold">--</div>
          </div>
        </div>
      </div>
    </div>
    <div class="col-md-4">
      <div
        class="card border-0 shadow-sm rounded-4 p-3 bg-white h-100 stat-card"
      >
        <div class="d-flex align-items-center">
          <div class="icon-box bg-warning-subtle text-warning rounded-3 me-3">
            <i class="bi bi-calendar-event fs-4"></i>
          </div>
          <div>
            <div class="text-muted small">Eventos Activos</div>
            <div class="fs-3 fw-bold">--</div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <div class="row">
    <!-- Form Section -->
    <div class="col-lg-4 mb-4">
      <div class="card border-0 shadow-sm rounded-4 p-4 sticky-top-custom">
        <h5 class="fw-bold mb-3">
          <i class="bi bi-plus-circle me-2 text-primary"></i>Nuevo Deporte
        </h5>
        <div class="mb-3">
          <input
            class="form-control rounded-3 py-2"
            placeholder="Nombre de la disciplina"
            bind:value={nuevoNombre}
            on:keydown={(e) => e.key === "Enter" && agregar()}
          />
        </div>
        <button
          class="btn btn-primary w-100 rounded-3 py-2 fw-bold"
          on:click={agregar}
        >
          <i class="bi bi-save me-1"></i> Guardar Deporte
        </button>
      </div>
    </div>

    <!-- List Section -->
    <div class="col-lg-8">
      <div class="card border-0 shadow-sm rounded-4 overflow-hidden">
        <div
          class="card-header bg-white border-0 py-3 px-4 d-flex justify-content-between align-items-center"
        >
          <h5 class="fw-bold mb-0">Disciplinas Registradas</h5>
          <button
            class="btn btn-sm btn-outline-secondary rounded-pill px-3"
            on:click={cargar}
          >
            <i class="bi bi-arrow-clockwise me-1"></i> Refrescar
          </button>
        </div>
        <div class="card-body p-0">
          <div class="table-responsive">
            <table class="table table-hover align-middle mb-0">
              <thead class="bg-light text-muted small">
                <tr>
                  <th class="px-4 py-3">ID</th>
                  <th class="py-3">Nombre</th>
                  <th class="py-3 text-end px-4">Acciones</th>
                </tr>
              </thead>
              <tbody>
                {#if loading}
                  <tr
                    ><td colspan="3" class="text-center py-4"
                      ><span
                        class="spinner-border spinner-border-sm text-primary"
                      ></span> Cargando...</td
                    ></tr
                  >
                {:else if deportes.length === 0}
                  <tr
                    ><td colspan="3" class="text-center py-4"
                      >No hay deportes registrados.</td
                    ></tr
                  >
                {:else}
                  {#each deportes as deporte}
                    <tr>
                      <td class="px-4 text-muted small">#{deporte.id}</td>
                      <td class="fw-semibold text-dark">{deporte.nombre}</td>
                      <td class="text-end px-4">
                        <button class="btn btn-subtle-danger btn-sm rounded-3"
                          ><i class="bi bi-trash"></i></button
                        >
                        <button class="btn btn-subtle-primary btn-sm rounded-3"
                          ><i class="bi bi-pencil"></i></button
                        >
                      </td>
                    </tr>
                  {/each}
                {/if}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>

<style>
  .icon-box {
    width: 48px;
    height: 48px;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .stat-card {
    transition: transform 0.2s ease;
  }

  .stat-card:hover {
    transform: translateY(-5px);
  }

  .sticky-top-custom {
    top: 90px;
    z-index: 10;
  }

  .btn-subtle-danger {
    color: #dc3545;
    background: transparent;
    border: none;
  }
  .btn-subtle-danger:hover {
    background: #fff5f5;
  }

  .btn-subtle-primary {
    color: #0d6efd;
    background: transparent;
    border: none;
  }
  .btn-subtle-primary:hover {
    background: #f0f7ff;
  }

  .form-control:focus {
    box-shadow: none;
    border-color: #0d6efd;
  }

  .table thead th {
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }
</style>
