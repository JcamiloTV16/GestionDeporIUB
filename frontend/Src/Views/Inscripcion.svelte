<script>
  import { obtenerDeportes } from "../Services/Api.js";
  import { user } from "../Store.js";

  let nombre = "";
  let deporte = "";
  let deportes = [];
  let loading = false;
  let success = false;

  // Autocompletar nombre si el usuario está logueado
  user.subscribe((v) => {
    if (v) nombre = v.nombre;
  });

  async function cargar() {
    deportes = await obtenerDeportes();
  }

  function inscribirse() {
    if (!deporte) return;

    loading = true;
    setTimeout(() => {
      let inscripciones =
        JSON.parse(localStorage.getItem("inscripciones")) || [];
      inscripciones.push({ estudiante: nombre, deporte });
      localStorage.setItem("inscripciones", JSON.stringify(inscripciones));

      loading = false;
      success = true;
      setTimeout(() => (success = false), 3000);
    }, 800);
  }

  cargar();
</script>

<div class="inscripcion-view">
  <div class="row justify-content-center">
    <div class="col-lg-8">
      <div class="d-flex align-items-center mb-4">
        <div
          class="bg-primary text-white rounded-circle p-2 me-3 d-flex align-items-center justify-content-center"
          style="width: 40px; height: 40px;"
        >
          <i class="bi bi-pencil-square"></i>
        </div>
        <h4 class="fw-bold m-0">Formulario de Inscripción</h4>
      </div>

      {#if success}
        <div
          class="alert alert-success border-0 shadow-sm rounded-4 mb-4 animate__animated animate__fadeIn"
        >
          <i class="bi bi-check-circle-fill me-2"></i> ¡Inscripción exitosa! Ya puedes
          ver tu registro en el panel.
        </div>
      {/if}

      <div class="card border-0 bg-light rounded-4 p-4 p-md-5">
        <div class="mb-4">
          <label
            for="studentName"
            class="form-label fw-bold text-muted small text-uppercase"
            >Nombre Completo</label
          >
          <div class="input-group">
            <span class="input-group-text bg-white border-0 rounded-start-3"
              ><i class="bi bi-person text-primary"></i></span
            >
            <input
              id="studentName"
              class="form-control border-0 rounded-end-3 py-3"
              placeholder="Tu nombre artístico"
              bind:value={nombre}
              readonly={!!nombre}
            />
          </div>
        </div>

        <div class="mb-5">
          <label
            for="sportSelect"
            class="form-label fw-bold text-muted small text-uppercase"
            >Deporte de Interés</label
          >
          <div class="input-group">
            <span class="input-group-text bg-white border-0 rounded-start-3"
              ><i class="bi bi-award text-primary"></i></span
            >
            <select
              id="sportSelect"
              class="form-select border-0 rounded-end-3 py-3"
              bind:value={deporte}
            >
              <option value="">-- Selecciona una disciplina --</option>
              {#each deportes as d}
                <option value={d.nombre}>{d.nombre}</option>
              {/each}
            </select>
          </div>
        </div>

        <button
          class="btn btn-primary btn-lg w-100 rounded-3 py-3 fw-bold shadow-sm"
          on:click={inscribirse}
          disabled={loading || !deporte}
        >
          {#if loading}
            <span class="spinner-border spinner-border-sm me-2"></span> Procesando...
          {:else}
            Confirmar Inscripción
          {/if}
        </button>
      </div>
    </div>
  </div>
</div>

<style>
  .form-control:focus,
  .form-select:focus {
    box-shadow: 0 0 0 0.25rem rgba(13, 110, 253, 0.1);
  }
</style>
