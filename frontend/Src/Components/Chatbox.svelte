<script>
  let mensaje = ""
  let respuesta = ""

  function enviar(){
    if(mensaje.includes("inscribirme")){
      respuesta = "Ve a la sección Inscripción."
    } else if(mensaje.includes("horario")){
      respuesta = "Consulta la sección Deportes."
    } else {
      respuesta = "Soy el asistente virtual."
    }
    mensaje = ""
  }
</script>

<div class="card p-3 mt-4">
  <h6>Asistente Virtual</h6>

  <input class="form-control mb-2"
         bind:value={mensaje}>

  <button class="btn btn-primary btn-sm"
          on:click={enviar}>
    Enviar
  </button>

  <p class="mt-2">
    <strong>{respuesta}</strong>
  </p>
</div>