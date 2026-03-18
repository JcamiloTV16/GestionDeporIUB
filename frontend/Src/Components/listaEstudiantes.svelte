<script>
  import { createEventDispatcher } from "svelte";
  const dispatch = createEventDispatcher();

  export let cursoSeleccionado = null;
  export let inscritos = [];
  export let deportes = [];
  export let cargandoInscritos = false;

  function volverALista() {
    dispatch("volver");
  }
</script>

{#if cursoSeleccionado}
  <div class="card shadow-sm border-0 rounded-4 p-4 mt-2">
    <div class="d-flex justify-content-between align-items-center mb-3">
      <h5 class="fw-bold mb-0">
        Estudiantes Inscritos: {deportes.find(
          (d) => d.id === cursoSeleccionado.deporte_id,
        )?.nombre || "Curso"}
        ({cursoSeleccionado.dia_semana}
        {cursoSeleccionado.hora_inicio})
      </h5>
      <button class="btn btn-sm btn-secondary" on:click={volverALista}>
        <i class="bi bi-arrow-left me-1"></i> Volver a Lista
      </button>
    </div>

    <div class="table-responsive">
      <table class="table table-hover align-middle mb-0">
        <thead class="bg-light text-muted">
          <tr>
            <th>ID</th>
            <th>Nombre</th>
            <th>Correo</th>
            <th>Fecha Inscripción</th>
            <th class="text-end">Estado</th>
          </tr>
        </thead>
        <tbody>
          {#if cargandoInscritos}
            <tr><td colspan="5" class="text-center py-4">Cargando...</td></tr>
          {:else if inscritos.length === 0}
            <tr
              ><td colspan="5" class="text-center py-4 text-muted"
                >No hay estudiantes inscritos en este curso.</td
              ></tr
            >
          {:else}
            {#each inscritos as inscrito}
              <tr>
                <td>{inscrito.id}</td>
                <td>{inscrito.nombre}</td>
                <td>{inscrito.correo}</td>
                <td
                  >{new Date(inscrito.fecha_inscripcion).toLocaleDateString()}</td
                >
                <td class="text-end">
                  <span
                    class="badge {inscrito.estado ? 'bg-success' : 'bg-danger'}"
                  >
                    {inscrito.estado ? "Activo" : "Inactivo"}
                  </span>
                </td>
              </tr>
            {/each}
          {/if}
        </tbody>
      </table>
    </div>
  </div>
{:else}
  <div class="card shadow-sm border-0 rounded-4 p-5 mt-2 text-center bg-light">
    <i class="bi bi-people-fill display-3 text-secondary mb-3"></i>
    <h4 class="fw-bold text-dark mb-2">Consulta de Inscritos</h4>
    <p class="text-muted mx-auto" style="max-width: 400px;">
      Seleccione un curso activo desde la pestaña de Lista para visualizar la
      lista detallada de estudiantes inscritos.
    </p>
  </div>
{/if}
