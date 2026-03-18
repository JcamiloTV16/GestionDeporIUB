<script>
  export let auditorias = [];
  export let usuarios = [];
</script>

<div class="card shadow-sm border-0 rounded-4 p-4 mt-2">
  <div class="table-responsive">
    <table class="table table-hover align-middle mb-0">
      <thead class="bg-light text-muted">
        <tr>
          <th>Fecha</th>
          <th>Administrador</th>
          <th>Tabla Afectada</th>
          <th>Acción Realizada</th>
        </tr>
      </thead>
      <tbody>
        {#if auditorias.length === 0}
          <tr>
            <td colspan="4" class="text-center py-4 text-muted">
              No se han encontrado registros de auditoría.
            </td>
          </tr>
        {:else}
          {#each auditorias as log}
            <tr>
              <td class="text-muted small">
                {new Date(log.fecha_cambio).toLocaleString()}
              </td>
              <td>
                <div class="d-flex align-items-center">
                  <i class="bi bi-person-circle me-2 text-primary"></i>
                  <span>
                    {usuarios.find((u) => u.id === log.admin_id)?.nombre ||
                      `Admin ID: ${log.admin_id}`}
                  </span>
                </div>
              </td>
              <td>
                <span class="badge bg-light text-dark border">
                  {log.tabla_afectada}
                </span>
              </td>
              <td>
                <p class="mb-0 small">{log.accion}</p>
              </td>
            </tr>
          {/each}
        {/if}
      </tbody>
    </table>
  </div>
</div>
