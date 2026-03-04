<script>
  let inscripciones = JSON.parse(localStorage.getItem("inscripciones")) || [];
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

  <div class="row g-4 mb-4">
    <div class="col-md-6">
      <div class="card border-0 shadow-sm rounded-4 p-4 bg-white h-100">
        <div class="d-flex align-items-center mb-2">
          <div class="icon-box bg-info-subtle text-info rounded-3 me-3">
            <i class="bi bi-person-check fs-4"></i>
          </div>
          <div>
            <div class="text-muted small">Alumnos Inscritos</div>
            <div class="fs-2 fw-bold">{inscripciones.length}</div>
          </div>
        </div>
        <div class="progress mt-3" style="height: 6px;">
          <div
            class="progress-bar bg-info"
            role="progressbar"
            style="width: 75%"
            aria-valuenow="75"
            aria-valuemin="0"
            aria-valuemax="100"
          ></div>
        </div>
      </div>
    </div>
    <div class="col-md-6">
      <div class="card border-0 shadow-sm rounded-4 p-4 bg-white h-100">
        <div class="d-flex align-items-center mb-2">
          <div class="icon-box bg-primary-subtle text-primary rounded-3 me-3">
            <i class="bi bi-star fs-4"></i>
          </div>
          <div>
            <div class="text-muted small">Promedio de Rendimiento</div>
            <div class="fs-2 fw-bold">4.8</div>
          </div>
        </div>
        <div class="progress mt-3" style="height: 6px;">
          <div
            class="progress-bar bg-primary"
            role="progressbar"
            style="width: 85%"
            aria-valuenow="85"
            aria-valuemin="0"
            aria-valuemax="100"
          ></div>
        </div>
      </div>
    </div>
  </div>

  <div class="card border-0 shadow-sm rounded-4 overflow-hidden">
    <div class="card-header bg-white border-bottom py-3 px-4">
      <h5 class="fw-bold mb-0">Gestión de Alumnos</h5>
    </div>
    <div class="card-body p-0">
      <div class="table-responsive">
        <table class="table table-hover align-middle mb-0">
          <thead class="bg-light text-muted small">
            <tr>
              <th class="px-4 py-3 text-uppercase">Estudiante</th>
              <th class="py-3 text-uppercase">Disciplina</th>
              <th class="py-3 text-uppercase">Fecha Registro</th>
              <th class="py-3 text-uppercase text-end px-4">Acciones</th>
            </tr>
          </thead>
          <tbody>
            {#if inscripciones.length === 0}
              <tr>
                <td colspan="4" class="text-center py-5">
                  <i class="bi bi-inbox fs-1 text-muted d-block mb-3"></i>
                  <span class="text-muted"
                    >No hay estudiantes inscritos actualmente.</span
                  >
                </td>
              </tr>
            {:else}
              {#each inscripciones as inscripcion}
                <tr>
                  <td class="px-4">
                    <div class="d-flex align-items-center">
                      <div
                        class="avatar-sm bg-light rounded-circle me-3 d-flex align-items-center justify-content-center"
                      >
                        <i class="bi bi-person text-secondary"></i>
                      </div>
                      <span class="fw-semibold">{inscripcion.estudiante}</span>
                    </div>
                  </td>
                  <td>
                    <span
                      class="badge bg-light text-dark border rounded-pill px-3"
                      >{inscripcion.deporte}</span
                    >
                  </td>
                  <td class="text-muted small">Hoy</td>
                  <td class="text-end px-4">
                    <button
                      class="btn btn-outline-primary btn-sm rounded-pill px-3"
                    >
                      <i class="bi bi-eye me-1"></i> Perfil
                    </button>
                    <button class="btn btn-light btn-sm rounded-circle ms-2">
                      <i class="bi bi-three-dots-vertical"></i>
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
</div>

<style>
  .icon-box {
    width: 48px;
    height: 48px;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .avatar-sm {
    width: 32px;
    height: 32px;
  }

  .table thead th {
    font-size: 0.7rem;
    letter-spacing: 1px;
    font-weight: 700;
  }
</style>
