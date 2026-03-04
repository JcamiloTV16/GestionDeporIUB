<script>
  import { rol } from '../store.js'

  let inscripciones =
    JSON.parse(localStorage.getItem("inscripciones")) || []

  function cerrarSesion(){
    rol.set(null)
  }
</script>

<div class="container mt-4">
  <h2>Panel Entrenador</h2>

  <button class="btn btn-danger mb-3"
          on:click={cerrarSesion}>
    Cerrar Sesión
  </button>

  <ul class="list-group">
    {#each inscripciones as inscripcion}
      <li class="list-group-item">
        {inscripcion.estudiante} - {inscripcion.deporte}
      </li>
    {/each}
  </ul>
</div>