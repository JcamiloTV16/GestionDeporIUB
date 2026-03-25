<script>
  import { createEventDispatcher } from "svelte";
  import { user, token } from "../Store.js";
  import { get } from "svelte/store";
  import { actualizarUsuario } from "../Services/Api.js";

  const dispatch = createEventDispatcher();

  let currentUser = null;
  let formData = {};
  let loading = false;
  let success = false;
  let errorMsg = "";
  let editandoPassword = false;
  let newPassword = "";

  user.subscribe(v => {
    if (v) {
      currentUser = v;
      formData = {
        nombre: v.nombre || "",
        email: v.email || "",
        numero_documento: v.numero_documento || "",
      };
    }
  });

  async function guardarPerfil() {
    if (!formData.nombre || !formData.email) {
      errorMsg = "El nombre y correo son obligatorios.";
      return;
    }

    loading = true;
    errorMsg = "";
    success = false;

    try {
      const currentToken = get(token);
      const datos = { ...formData };
      if (editandoPassword && newPassword) {
        datos.password = newPassword;
      }

      await actualizarUsuario(currentUser.id, datos, currentToken);

      // Actualizar el store con los nuevos datos
      user.update(u => ({
        ...u,
        nombre: formData.nombre,
        email: formData.email,
        numero_documento: formData.numero_documento,
      }));

      success = true;
      editandoPassword = false;
      newPassword = "";
      setTimeout(() => (success = false), 4000);
    } catch (e) {
      errorMsg = "Error al actualizar el perfil.";
    } finally {
      loading = false;
    }
  }

  function volver() {
    dispatch("volver");
  }
</script>

<div class="p-4 animate__animated animate__fadeIn">
  <div class="row justify-content-center">
    <div class="col-lg-7">
      <div class="d-flex align-items-center mb-4 gap-3">
        <button class="btn btn-sm btn-light rounded-circle" on:click={volver} title="Volver">
          <i class="bi bi-arrow-left"></i>
        </button>
        <div class="bg-primary text-white rounded-circle p-2 d-flex align-items-center justify-content-center" style="width:40px;height:40px">
          <i class="bi bi-person-gear"></i>
        </div>
        <h4 class="fw-bold m-0">Mi Perfil</h4>
      </div>

      {#if success}
        <div class="alert alert-success border-0 shadow-sm rounded-4 mb-4">
          <i class="bi bi-check-circle-fill me-2"></i> Perfil actualizado correctamente.
        </div>
      {/if}
      
      {#if errorMsg}
        <div class="alert alert-danger border-0 shadow-sm rounded-4 mb-4">
          <i class="bi bi-exclamation-triangle-fill me-2"></i> {errorMsg}
        </div>
      {/if}

      <div class="card border-0 shadow-sm rounded-4 p-4 p-md-5">
        <form on:submit|preventDefault={guardarPerfil}>
          <div class="mb-4">
            <label for="perfilNombre" class="form-label fw-bold text-muted small text-uppercase">Nombre Completo</label>
            <div class="input-group">
              <span class="input-group-text bg-light border-0 rounded-start-3"><i class="bi bi-person text-primary"></i></span>
              <input id="perfilNombre" type="text" class="form-control border-light bg-light rounded-end-3 py-3" bind:value={formData.nombre} />
            </div>
          </div>

          <div class="mb-4">
            <label for="perfilEmail" class="form-label fw-bold text-muted small text-uppercase">Correo Electrónico</label>
            <div class="input-group">
              <span class="input-group-text bg-light border-0 rounded-start-3"><i class="bi bi-envelope text-primary"></i></span>
              <input id="perfilEmail" type="email" class="form-control border-light bg-light rounded-end-3 py-3" bind:value={formData.email} />
            </div>
          </div>

          <div class="mb-4">
            <label for="perfilDoc" class="form-label fw-bold text-muted small text-uppercase">Número de Documento</label>
            <div class="input-group">
              <span class="input-group-text bg-light border-0 rounded-start-3"><i class="bi bi-card-text text-primary"></i></span>
              <input id="perfilDoc" type="text" class="form-control border-light bg-light rounded-end-3 py-3" bind:value={formData.numero_documento} />
            </div>
          </div>

          <!-- Cambiar contraseña -->
          <div class="mb-4">
            {#if !editandoPassword}
              <button type="button" class="btn btn-outline-secondary btn-sm rounded-pill" on:click={() => (editandoPassword = true)}>
                <i class="bi bi-key me-1"></i> Cambiar Contraseña
              </button>
            {:else}
              <label for="perfilPass" class="form-label fw-bold text-muted small text-uppercase">Nueva Contraseña</label>
              <div class="input-group">
                <span class="input-group-text bg-light border-0 rounded-start-3"><i class="bi bi-lock text-primary"></i></span>
                <input id="perfilPass" type="password" class="form-control border-light bg-light rounded-end-3 py-3" placeholder="Escribe la nueva contraseña" bind:value={newPassword} />
              </div>
              <button type="button" class="btn btn-link btn-sm text-muted mt-1" on:click={() => { editandoPassword = false; newPassword = ""; }}>
                Cancelar cambio de contraseña
              </button>
            {/if}
          </div>

          <button type="submit" class="btn btn-primary btn-lg w-100 rounded-3 py-3 fw-bold shadow-sm" disabled={loading}>
            {#if loading}
              <span class="spinner-border spinner-border-sm me-2"></span> Guardando...
            {:else}
              <i class="bi bi-save me-2"></i> Guardar Cambios
            {/if}
          </button>
        </form>
      </div>
    </div>
  </div>
</div>

<style>
  .form-control:focus, .form-select:focus {
    box-shadow: 0 0 0 0.25rem rgba(13, 110, 253, 0.1);
  }
</style>
