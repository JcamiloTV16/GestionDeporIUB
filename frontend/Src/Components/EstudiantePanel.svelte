<script>
  import { rol } from '../store.js'
  import Deportes from '../Deportes.svelte'
  import Inscripcion from '../Inscripcion.svelte'
  import Torneos from './Torneos.svelte'
  import Chatbot from './Chatbot.svelte'

  let vista = "deportes"

  function cerrarSesion(){
    rol.set(null)
  }
</script>

<div class="container mt-3">
  <h2>Panel Estudiante</h2>

  <button class="btn btn-danger mb-3"
          on:click={cerrarSesion}>
    Cerrar Sesión
  </button>

  <div class="mb-3">
    <button class="btn btn-primary me-2"
            on:click={()=>vista="deportes"}>
      Deportes
    </button>
    <button class="btn btn-primary me-2"
            on:click={()=>vista="inscripcion"}>
      Inscripción
    </button>
    <button class="btn btn-primary"
            on:click={()=>vista="torneos"}>
      Torneos
    </button>
  </div>

  {#if vista === "deportes"}
    <Deportes />
  {:else if vista === "inscripcion"}
    <Inscripcion />
  {:else}
    <Torneos />
  {/if}

  <Chatbot />
</div>