<script>
  import { createEventDispatcher } from "svelte";
  const dispatch = createEventDispatcher();

  export let usuarios = [];
  export let roles = [];
  export let tiposDocumento = [];
</script>
<div class="card shadow-sm border-0 rounded-4 p-4 mt-2">
  <h5 class="fw-bold mb-3">Lista de Usuarios</h5>
  <div class="table-responsive">
    <table class="table table-hover align-middle mb-0">
      <thead class="bg-light text-muted">
        <tr>
          <th>ID</th><th>Nombre</th><th>Correo</th><th>Rol</th><th
            >Tipo Documento</th
          ><th>Documento</th><th class="text-end">Acciones</th>
        </tr>
      </thead>
      <tbody>
        {#if usuarios.length === 0}
          <tr
            ><td colspan="7" class="text-center py-4 text-muted"
              >No hay usuarios registrados en el momento.</td
            ></tr
          >
        {:else}
          {#each usuarios as usuario}
            <tr>
              <td>{usuario.id}</td>
              <td>{usuario.nombre}</td>
              <td>{usuario.email || usuario.correo}</td>
              <td
                >{roles.find((r) => r.id === usuario.rol_id)?.nombre ||
                  "Desconocido"}</td
              >
              <td
                >{tiposDocumento.find((td) => td.id === usuario.tipo_documento_id)
                  ?.nombre || "Desconocido"}</td
              >
              <td>{usuario.numero_documento}</td>
              <td class="text-end">
                <button
                  class="btn btn-sm btn-outline-primary me-2"
                  on:click={() => dispatch("editar", usuario)}
                >
                  <i class="bi bi-pencil"></i>
                </button>
                <button
                  class="btn btn-sm btn-outline-danger"
                  on:click={() => dispatch("eliminar", usuario.id)}
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
