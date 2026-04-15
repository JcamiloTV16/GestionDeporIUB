<script>
  import { recoverPassword } from "../Services/Api.js";
  import "../Styles/Login.css";

  let email = "";
  let loading = false;
  let errorMessage = "";
  let resultado = null;

  async function recuperar() {
    if (!email) {
      errorMessage = "Por favor, ingresa tu correo electrónico";
      return;
    }

    loading = true;
    errorMessage = "";
    resultado = null;

    try {
      const data = await recoverPassword(email);
      resultado = data;
    } catch (error) {
      errorMessage = error.message;
    } finally {
      loading = false;
    }
  }

  function volver() {
    window.location.hash = "#/";
  }
</script>

<div class="login-page">
  <div class="container d-flex justify-content-center align-items-center min-vh-100">
    <div class="card p-5 shadow-lg border-0 login-card animate__animated animate__fadeIn">
      <div class="text-center mb-4">
        <div class="logo-circle mx-auto mb-3">
          <i class="bi bi-key-fill text-white fs-1"></i>
        </div>
        <h2 class="fw-bold text-primary">
          Recuperar <span class="text-dark">Contraseña</span>
        </h2>
        <p class="text-muted">Ingresa tu correo electrónico para recuperar tu contraseña</p>
      </div>

      {#if errorMessage}
        <div class="alert alert-danger text-center py-2 animate__animated animate__shakeX">
          <i class="bi bi-exclamation-triangle-fill me-2"></i>{errorMessage}
        </div>
      {/if}

      {#if resultado}
        <div class="alert alert-success border-0 shadow-sm rounded-4 mb-4 animate__animated animate__fadeIn">
          <div class="text-center">
            <i class="bi bi-check-circle-fill fs-3 d-block mb-2"></i>
            <p class="fw-bold mb-1">¡Hola, {resultado.nombre}!</p>
            <p class="mb-2 text-muted small">Tu contraseña es:</p>
            <div class="bg-light rounded-3 p-3 d-flex align-items-center justify-content-center gap-2">
              <code class="fs-5 text-dark fw-bold user-select-all">{resultado.password}</code>
            </div>
            <p class="mt-2 mb-0 text-muted" style="font-size: 0.75rem;">
              <i class="bi bi-info-circle me-1"></i>Copia tu contraseña y regresa al inicio de sesión
            </p>
          </div>
        </div>
      {:else}
        <div class="form-floating mb-4">
          <input
            type="email"
            class="form-control"
            id="recoverEmail"
            placeholder="Correo Electrónico"
            bind:value={email}
            on:keydown={(e) => e.key === "Enter" && recuperar()}
          />
          <label for="recoverEmail">Correo Electrónico</label>
        </div>

        <button
          class="btn btn-primary btn-lg w-100 shadow-sm py-3 fw-bold transition-all"
          on:click={recuperar}
          disabled={loading}
        >
          {#if loading}
            <span class="spinner-border spinner-border-sm me-2"></span> Buscando...
          {:else}
            <i class="bi bi-search me-2"></i>Recuperar Contraseña
          {/if}
        </button>
      {/if}

      <div class="text-center mt-4">
        <button
          class="btn btn-link text-decoration-none text-muted small p-0"
          on:click={volver}
        >
          <i class="bi bi-arrow-left me-1"></i>Volver al inicio de sesión
        </button>
      </div>
    </div>
  </div>
</div>
