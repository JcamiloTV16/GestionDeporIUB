<script>
  import { obtenerDeportes } from '../services/api.js'

  let nombre = ""
  let deporte = ""
  let deportes = []

  async function cargar(){
    deportes = await obtenerDeportes()
  }

  function inscribirse(){
    let inscripciones =
      JSON.parse(localStorage.getItem("inscripciones")) || []

    inscripciones.push({
      estudiante: nombre,
      deporte
    })

    localStorage.setItem(
      "inscripciones",
      JSON.stringify(inscripciones)
    )

    alert("Inscripción exitosa")
    nombre = ""
  }

  cargar()
</script>

<h3>Inscripción</h3>

<input class="form-control mb-2"
       placeholder="Nombre"
       bind:value={nombre}>

<select class="form-select mb-2"
        bind:value={deporte}>
  <option value="">Seleccione deporte</option>
  {#each deportes as d}
    <option value={d.nombre}>{d.nombre}</option>
  {/each}
</select>

<button class="btn btn-success"
        on:click={inscribirse}>
  Inscribirse
</button>