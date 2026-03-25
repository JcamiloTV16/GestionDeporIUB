<script>
  import { createEventDispatcher } from "svelte";
  const dispatch = createEventDispatcher();

  export let cursos = [];
  export let deportes = [];
  export let entrenadores = [];

  function verInscritos(curso) {
    dispatch("verInscritos", curso);
  }

  function eliminarHorario(id) {
    dispatch("eliminar", id);
  }
</script>

<div class="card shadow-sm border-0 rounded-4 p-4 mt-2">
  <h5 class="fw-bold mb-3">Lista de Cursos Activos</h5>
  <div class="table-responsive">
    <table class="table table-hover align-middle mb-0">
      <thead class="bg-light text-muted">
        <tr>
          <th>ID</th><th>Deporte</th><th>Entrenador</th><th>Días</th><th
            >Hora</th
          ><th>Cupo</th><th class="text-end">Acciones</th>
        </tr>
      </thead>
      <tbody>
        {#if cursos.length === 0}
          <tr
            ><td colspan="7" class="text-center py-4 text-muted"
              >No hay cursos registrados en el momento.</td
            ></tr
          >
        {:else}
          {#each cursos as curso}
            <tr>
              <td>{curso.id}</td>
              <td
                >{deportes.find((d) => d.id === curso.deporte_id)?.nombre ||
                  "Desconocido"}</td
              >
              <td>
                {entrenadores.find((e) => e.id == curso.entrenador_id)
                  ?.nombre_usuario || `Desconocido (ID: ${curso.entrenador_id})`}
              </td>
              <td>{curso.dia_semana}</td>
              <td>{curso.hora_inicio} - {curso.hora_fin}</td>
              <td>{curso.cupo}</td>
              <td class="text-end">
                <button
                  class="btn btn-sm btn-outline-info me-2"
                  title="Ver inscritos"
                  on:click={() => verInscritos(curso)}
                >
                  <i class="bi bi-people"></i>
                </button>
                <button class="btn btn-sm btn-outline-primary me-2" on:click={() => dispatch("editar", curso)}
                  ><i class="bi bi-pencil"></i></button
                >
                <button class="btn btn-sm btn-outline-danger" on:click={() => eliminarHorario(curso.id)}
                  ><i class="bi bi-trash"></i></button
                >
              </td>
            </tr>
          {/each}
        {/if}
      </tbody>
    </table>
  </div>
</div>
