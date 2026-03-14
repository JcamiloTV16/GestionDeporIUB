<script>
  import { rol, user, token } from "../Store.js";
  import { login } from "../Services/Api.js";

  let email = "";
  let password = "";
  let loading = false;
  let errorMessage = "";

  async function iniciarSesion() {
    if (!email || !password) {
      errorMessage = "Por favor, ingresa tus credenciales";
      return;
    }

    loading = true;
    errorMessage = "";

    try {
      const data = await login(email, password);
      // Actualizar stores
      user.set(data.user);
      token.set(data.access_token);

      // Normalizar el rol para que coincida con App.svelte
      let userRol = data.user.rol.toLowerCase();
      if (userRol.includes("admin")) userRol = "admin";
      else if (userRol.includes("entrenador")) userRol = "entrenador";
      else if (userRol.includes("estudiante")) userRol = "estudiante";

      rol.set(userRol);
    } catch (error) {
      errorMessage = error.message;
    } finally {
      loading = false;
    }
  }
</script>

<div class="login-page">
  <div
    class="container d-flex justify-content-center align-items-center min-vh-100"
  >
    <div
      class="card p-5 shadow-lg border-0 login-card animate__animated animate__fadeIn"
    >
      <div class="text-center mb-4">
        <div class="logo-circle mx-auto mb-3">
          <i class="bi bi-person-badge-fill text-white fs-1"></i>
        </div>
        <h2 class="fw-bold text-primary">
          GestionDepor<span class="text-dark">IUB</span>
        </h2>
        <p class="text-muted">Inicia sesión para acceder a tu panel</p>
      </div>

      {#if errorMessage}
        <div
          class="alert alert-danger text-center py-2 animate__animated animate__shakeX"
        >
          {errorMessage}
        </div>
      {/if}

      <div class="form-floating mb-3">
        <input
          type="email"
          class="form-control"
          id="emailInput"
          placeholder="Correo Electrónico"
          bind:value={email}
        />
        <label for="emailInput">Correo Electrónico</label>
      </div>

      <div class="form-floating mb-4">
        <input
          type="password"
          class="form-control"
          id="passwordInput"
          placeholder="Contraseña"
          bind:value={password}
          on:keydown={(e) => e.key === "Enter" && iniciarSesion()}
        />
        <label for="passwordInput">Contraseña</label>
      </div>

      <button
        class="btn btn-primary btn-lg w-100 shadow-sm py-3 fw-bold transition-all"
        on:click={iniciarSesion}
        disabled={loading}
      >
        {#if loading}
          <span class="spinner-border spinner-border-sm me-2"></span> Cargando...
        {:else}
          Ingresar
        {/if}
      </button>

      <div class="text-center mt-4">
        <a href="#/recover" class="text-decoration-none text-muted small"
          >¿Olvidaste tu contraseña?</a
        >
      </div>
    </div>
  </div>
</div>

<style>
  :global(body) {
    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    min-height: 100vh;
  }

  .login-card {
    max-width: 450px;
    width: 100%;
    border-radius: 20px;
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(10px);
  }

  .logo-circle {
    width: 80px;
    height: 80px;
    background: linear-gradient(45deg, #0d6efd, #0dcaf0);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 10px 20px rgba(13, 110, 253, 0.3);
  }

  .form-control {
    border-radius: 12px;
    border: 1px solid #dee2e6;
    padding: 1rem 0.75rem;
  }

  .form-control:focus {
    box-shadow: 0 0 0 0.25rem rgba(13, 110, 253, 0.15);
    border-color: #0d6efd;
  }

  .btn-primary {
    border-radius: 12px;
    background: linear-gradient(45deg, #0d6efd, #0b5ed7);
    border: none;
  }

  .btn-primary:hover:not(:disabled) {
    transform: translateY(-2px);
    box-shadow: 0 10px 20px rgba(13, 110, 253, 0.25);
  }

  .transition-all {
    transition: all 0.3s ease;
  }
</style>
