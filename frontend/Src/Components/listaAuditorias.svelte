<script>
  import { createEventDispatcher } from "svelte";
  const dispatch = createEventDispatcher();

  export let usuariosInactivos = [];
  export let deportesInactivos = [];
  export let cursosInactivos = [];
</script>

<!-- Sección de Usuarios Inactivos -->
<div class="mb-5">
  <h4 class="fw-bold text-dark mb-3">
    <i class="bi bi-person-x-fill me-2 text-danger"></i>Usuarios Inactivos
  </h4>
  <div class="card shadow-sm border-0 rounded-4 p-4">
    <div class="table-responsive">
      <table class="table table-hover align-middle mb-0">
        <thead class="bg-light text-muted">
          <tr>
            <th>Nombre</th>
            <th>Email</th>
            <th class="text-end">Acciones</th>
          </tr>
        </thead>
        <tbody>
          {#if usuariosInactivos.length === 0}
            <tr>
              <td colspan="3" class="text-center py-4 text-muted">
                No hay usuarios inactivos en este momento.
              </td>
            </tr>
          {:else}
            {#each usuariosInactivos as user}
              <tr>
                <td>
                  <div class="fw-bold text-dark">{user.nombre}</div>
                </td>
                <td class="text-muted">{user.email}</td>
                <td class="text-end">
                  <button
                    class="btn btn-sm btn-outline-success rounded-pill px-3"
                    on:click={() => dispatch("reactivarUsuario", user.id)}
                  >
                    <i class="bi bi-arrow-repeat me-1"></i>Reactivar
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

<!-- Sección de Deportes Inactivos -->
<div class="mb-5">
  <h4 class="fw-bold text-dark mb-3">
    <i class="bi bi-tools me-2 text-warning"></i>Deportes Inactivos
  </h4>
  <div class="card shadow-sm border-0 rounded-4 p-4">
    <div class="table-responsive">
      <table class="table table-hover align-middle mb-0">
        <thead class="bg-light text-muted">
          <tr>
            <th>Nombre</th>
            <th class="text-end">Acciones</th>
          </tr>
        </thead>
        <tbody>
          {#if deportesInactivos.length === 0}
            <tr>
              <td colspan="2" class="text-center py-4 text-muted">
                No hay deportes inactivos.
              </td>
            </tr>
          {:else}
            {#each deportesInactivos as d}
              <tr>
                <td>{d.nombre}</td>
                <td class="text-end">
                  <button 
                    class="btn btn-sm btn-outline-success rounded-pill px-3"
                    on:click={() => dispatch('reactivarDeporte', d.id)}
                  >
                    <i class="bi bi-arrow-repeat me-1"></i>Reactivar
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

<!-- Sección de Cursos Inactivos -->
<div class="mb-5">
  <h4 class="fw-bold text-dark mb-3">
    <i class="bi bi-person-video3 me-2 text-info"></i>Cursos Inactivos
  </h4>
  <div class="card shadow-sm border-0 rounded-4 p-4">
    <div class="table-responsive">
      <table class="table table-hover align-middle mb-0">
        <thead class="bg-light text-muted">
          <tr>
            <th>ID</th>
            <th>Deporte</th>
            <th>Día/Hora</th>
            <th class="text-end">Acciones</th>
          </tr>
        </thead>
        <tbody>
          {#if cursosInactivos.length === 0}
            <tr>
              <td colspan="4" class="text-center py-4 text-muted">
                No hay cursos inactivos.
              </td>
            </tr>
          {:else}
            {#each cursosInactivos as c}
              <tr>
                <td>{c.id}</td>
                <td>{c.deporte_nombre || 'Deporte'}</td>
                <td>{c.dia_semana} {c.hora_inicio}-{c.hora_fin}</td>
                <td class="text-end">
                  <button 
                    class="btn btn-sm btn-outline-success rounded-pill px-3"
                    on:click={() => dispatch('reactivarHorario', c.id)}
                  >
                    <i class="bi bi-arrow-repeat me-1"></i>Reactivar
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

<hr class="my-5 opacity-25" />
