<script>
  import { rol } from '../store.js'
  import { obtenerDeportes, agregarDeporte } from '../services/api.js'

  let deportes = []
  let nuevoNombre = ""

  async function cargar(){
    deportes = await obtenerDeportes()
  }

  async function agregar(){
    await agregarDeporte({ nombre: nuevoNombre })
    nuevoNombre = ""
    cargar()
  }

  function cerrarSesion(){
    rol.set(null)
  }

  cargar()
</script>

<div class="container mt-4">
  <h2>Panel Administrador</h2>

  <button class="btn btn-danger mb-3"
          on:click={cerrarSesion}>
    Cerrar Sesión
  </button>

  <div class="card p-3 mb-3">
    <input class="form-control mb-2"
           placeholder="Nuevo deporte"
           bind:value={nuevoNombre}>
    <button class="btn btn-success"
            on:click={agregar}>
      Agregar
    </button>
  </div>

  <ul class="list-group">
    {#each deportes as deporte}
      <li class="list-group-item">
        {deporte.nombre}
      </li>
    {/each}
  </ul>
</div>