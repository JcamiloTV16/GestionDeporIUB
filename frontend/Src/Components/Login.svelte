<script>
  import { rol } from '../store.js'

  let usuario = ""
  let tipoRol = ""

  function iniciarSesion(){
    if(usuario && tipoRol){
      rol.set(tipoRol)
    }
  }
</script>

<div class="container mt-5">
  <div class="card p-4 shadow">
    <h3>Iniciar Sesión</h3>

    <input class="form-control mb-3"
           placeholder="Nombre"
           bind:value={usuario}>

    <select class="form-select mb-3"
            bind:value={tipoRol}>
      <option value="">Seleccione Rol</option>
      <option value="admin">Administrador</option>
      <option value="entrenador">Entrenador</option>
      <option value="estudiante">Estudiante</option>
    </select>

    <button class="btn btn-primary"
            on:click={iniciarSesion}>
      Ingresar
    </button>
  </div>
</div>