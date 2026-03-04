<script>
  import { obtenerDeportes } from '../services/api.js'
  let deportes = []

  async function cargar(){
    deportes = await obtenerDeportes()
  }

  cargar()
</script>

<h3>Deportes Disponibles</h3>

<ul class="list-group">
  {#each deportes as deporte}
    <li class="list-group-item">
      {deporte.nombre}
    </li>
  {/each}
</ul>