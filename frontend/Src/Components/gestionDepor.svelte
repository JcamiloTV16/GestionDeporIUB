<script>
  import { createEventDispatcher } from "svelte";
  const dispatch = createEventDispatcher();

  export let subVistaInterna = "lista";
  export let deportes = [];
  export let nuevoDeporte = { nombre: "", descripcion: "" };
  export let editandoId = null;
  export let mensajeEstado = { texto: "", tipo: "" };

  function manejarGuardarDeporte() {
    dispatch("guardar");
  }

  function prepararEdicionDeporte(deporte) {
    dispatch("editar", deporte);
  }

  function manejarEliminarDeporte(id) {
    dispatch("eliminar", id);
  }

  function cancelarEdicion() {
    dispatch("cancelar");
  }
</script>

{#if mensajeEstado.texto}
  <div
    class="alert alert-{mensajeEstado.tipo} mt-3 animate__animated animate__fadeIn"
  >
    {mensajeEstado.texto}
  </div>
{/if}

{#if subVistaInterna === "lista"}
  <div class="card shadow-sm border-0 rounded-4 p-4 mt-2">
    <h5 class="fw-bold mb-3">Lista de Deportes</h5>
    <div class="table-responsive">
      <table class="table table-hover align-middle mb-0">
        <thead class="bg-light text-muted">
          <tr>
            <th>ID</th>
            <th>Nombre</th>
            <th>Descripción</th>
            <th class="text-end">Acciones</th>
          </tr>
        </thead>
        <tbody>
          {#if deportes.length === 0}
            <tr>
              <td colspan="4" class="text-center py-4 text-muted">
                No hay deportes registrados en el momento.
              </td>
            </tr>
          {:else}
            {#each deportes as deporte}
              <tr>
                <td>{deporte.id}</td>
                <td class="fw-bold">{deporte.nombre}</td>
                <td class="text-muted small"
                  >{deporte.descripcion || "Sin descripción"}</td
                >
                <td class="text-end">
                  <button
                    class="btn btn-sm btn-outline-primary me-2"
                    on:click={() => prepararEdicionDeporte(deporte)}
                  >
                    <i class="bi bi-pencil"></i>
                  </button>
                  <button
                    class="btn btn-sm btn-outline-danger"
                    on:click={() => manejarEliminarDeporte(deporte.id)}
                  >
                    <i class="bi bi-trash"></i>
                  </button>
                </td>
              </tr>
            {/each}
          {/if}
        </tbody>
      </table>
    </div>
  </div>
{:else if subVistaInterna === "crear"}
  <div class="card shadow-sm border-0 rounded-4 p-4 mt-2">
    <h5 class="fw-bold mb-3">
      {editandoId ? "Editar Deporte" : "Registrar Nuevo Deporte"}
    </h5>
    <form on:submit|preventDefault={manejarGuardarDeporte}>
      <div class="mb-3">
        <label for="nombreDeporte" class="form-label">Nombre del Deporte</label>
        <input
          type="text"
          class="form-control"
          id="nombreDeporte"
          bind:value={nuevoDeporte.nombre}
          placeholder="Ej: Futbol, Natación..."
          required
        />
      </div>
      <div class="mb-3">
        <label for="descDeporte" class="form-label">Descripción</label>
        <textarea
          class="form-control"
          id="descDeporte"
          rows="3"
          bind:value={nuevoDeporte.descripcion}
          placeholder="Información sobre la disciplina..."
        ></textarea>
      </div>
      <div class="text-end">
        {#if editandoId}
          <button type="button" class="btn btn-secondary me-2" on:click={cancelarEdicion}
            >Cancelar</button
          >
        {/if}
        <button type="submit" class="btn btn-primary px-4"
          >{editandoId ? "Actualizar" : "Guardar"} Deporte</button
        >
      </div>
    </form>
  </div>
{/if}
