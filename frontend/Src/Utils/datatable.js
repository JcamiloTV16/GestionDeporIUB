/**
 * Svelte action to initialize DataTables on a <table> element.
 * Usage: <table use:datatable={data}>
 * 
 * Re-initializes whenever the bound data changes length.
 */
export function datatable(node, data) {
  let dt = null;

  function init() {
    // Destroy existing instance
    if (dt) {
      dt.destroy();
      dt = null;
    }

    // Wait a tick for Svelte to finish rendering rows
    setTimeout(() => {
      if (window.jQuery && window.jQuery.fn.DataTable) {
        dt = window.jQuery(node).DataTable({
          destroy: true,
          pageLength: 10,
          lengthMenu: [5, 10, 25, 50],
          language: {
            search: "Buscar:",
            lengthMenu: "Mostrar _MENU_ registros",
            info: "Mostrando _START_ a _END_ de _TOTAL_ registros",
            infoEmpty: "Sin registros",
            infoFiltered: "(filtrado de _MAX_ registros totales)",
            zeroRecords: "No se encontraron resultados",
            emptyTable: "No hay datos disponibles",
            paginate: {
              first: "Primero",
              last: "Último",
              next: "Siguiente",
              previous: "Anterior"
            }
          },
          // Preserve the Bootstrap styling
          dom: '<"row"<"col-sm-12 col-md-6"l><"col-sm-12 col-md-6"f>>rtip',
          order: [] // No default sort to preserve original order
        });
      }
    }, 50);
  }

  // Only init if there's data
  if (data && data.length > 0) {
    init();
  }

  return {
    update(newData) {
      if (newData && newData.length > 0) {
        init();
      } else if (dt) {
        dt.destroy();
        dt = null;
      }
    },
    destroy() {
      if (dt) {
        dt.destroy();
        dt = null;
      }
    }
  };
}
