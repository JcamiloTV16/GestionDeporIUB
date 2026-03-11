<script>
  import { onMount } from "svelte";
  import { cerrarSesion } from "../Store.js";
  import SubNav from "../Components/SubNav.svelte";
  import UserForm from "../Components/UserForm.svelte";
  import CourseForm from "../Components/CourseForm.svelte";
  import "../Styles/AdminPanel.css";

  let vistaActual = "dashboard";
  let subVistaInterna = "lista";

  // Datos dinámicos para pasar a los componentes
  let tiposDocumento = [];
  let facultades = [];
  let roles = [];
  let deportes = [];
  let entrenadores = [];

  const opcionesCurso = [
    { id: "lista", texto: "Lista", icono: "bi bi-list-ul" },
    { id: "crear", texto: "Crear", icono: "bi bi-plus-circle" },
    { id: "inscritos", texto: "Inscritos", icono: "bi bi-people" },
  ];

  const opcionesUsuario = [
    { id: "lista", texto: "Lista", icono: "bi bi-list-ul" },
    { id: "crear", texto: "Crear", icono: "bi bi-person-plus" },
  ];

  onMount(async () => {
    try {
      // Fetch desde Node Backend (Puerto 3000)
      const resTipos = await fetch("http://localhost:3000/tipos-documento");
      tiposDocumento = await resTipos.json();

      const resFacultades = await fetch("http://localhost:3000/facultades");
      facultades = await resFacultades.json();

      // Fetch desde Python Backend (Puerto 8000)
      const resRoles = await fetch("http://localhost:8000/roles/");
      roles = (await resRoles.json()).resultado || [];

      const resDeportes = await fetch("http://localhost:8000/deportes/");
      deportes = (await resDeportes.json()).resultado || [];

      const resEntrenadores = await fetch(
        "http://localhost:8000/entrenadores/",
      );
      entrenadores = (await resEntrenadores.json()).resultado || [];
    } catch (error) {
      console.error("Error cargando datos iniciales:", error);
    }
  });

  function cambiarVistaPrincipal(vista) {
    vistaActual = vista;
    subVistaInterna = "lista";
  }

  function manejarSalida() {
    cerrarSesion();
  }
</script>

<div class="contenedor-aplicativo">
  <div class="sub-menu-admin bg-white border-bottom px-4 d-flex gap-3">
    <!-- Menu Dashboard -->
    <button
      class="btn-pestana {vistaActual === 'dashboard' ? 'activa' : ''}"
      on:click={() => cambiarVistaPrincipal("dashboard")}
    >
      <i class="bi bi-pie-chart-fill me-2"></i>Dashboard Informativo
    </button>
    <!-- Menu Usuarios -->
    <button
      class="btn-pestana {vistaActual === 'usuarios' ? 'activa' : ''}"
      on:click={() => cambiarVistaPrincipal("usuarios")}
    >
      <i class="bi bi-people me-2"></i>Gestión de Usuarios
    </button>
    <!-- Menu Cursos -->
    <button
      class="btn-pestana {vistaActual === 'cursos' ? 'activa' : ''}"
      on:click={() => cambiarVistaPrincipal("cursos")}
    >
      <i class="bi bi-person-video3 me-2"></i>Gestión de Cursos o Grupos
    </button>
    <!-- Menu Deportes -->
    <button
      class="btn-pestana {vistaActual === 'deportes' ? 'activa' : ''}"
      on:click={() => cambiarVistaPrincipal("deportes")}
    >
      <i class="bi bi-tools me-2"></i>Gestión de Deportes
    </button>
    <!-- Menu Auditorias -->
    <button
      class="btn-pestana {vistaActual === 'auditorias' ? 'activa' : ''}"
      on:click={() => cambiarVistaPrincipal("auditorias")}
    >
      <i class="bi bi-calendar me-2"></i>Auditorias
    </button>
  </div>

  <main class="contenido-principal p-4">
    {#if vistaActual === "dashboard"}
      <section class="animate__animated animate__fadeIn">
        <div class="d-flex justify-content-between align-items-center mb-4">
          <h2 class="fw-bold text-dark">Análisis de Datos (PowerBI)</h2>
          <span class="badge bg-success-subtle text-success border px-3 py-2"
            >Datos en Tiempo Real</span
          >
        </div>
        <div class="tarjeta-reporte shadow-sm rounded-4 bg-white p-2">
          <div
            class="placeholder-visual d-flex flex-column align-items-center justify-content-center"
          >
            <i class="bi bi-cpu fs-1 text-primary mb-3"></i>
            <p class="text-muted fw-medium">
              Esperando conexión con el reporte de PowerBI...
            </p>
          </div>
        </div>
      </section>
    {:else if vistaActual === "usuarios"}
      <section class="animate__animated animate__fadeIn">
        <h2 class="fw-bold text-dark mb-4">Administrar Usuarios</h2>
        <SubNav
          opciones={opcionesUsuario}
          vistaActiva={subVistaInterna}
          on:cambio={(e) => (subVistaInterna = e.detail)}
        />

        {#if subVistaInterna === "lista"}
          <div class="card shadow-sm border-0 rounded-4 p-4 mt-2">
            <h5 class="fw-bold mb-3">Lista de Usuarios</h5>
            <div class="table-responsive">
              <table class="table table-hover align-middle mb-0">
                <thead class="bg-light text-muted">
                  <tr>
                    <th>ID</th><th>Nombre</th><th>Correo</th><th>Rol</th><th
                      >Tipo Documento</th
                    ><th>Documento</th><th class="text-end">Acciones</th>
                  </tr>
                </thead>
                <tbody>
                  <tr
                    ><td colspan="7" class="text-center py-4 text-muted"
                      >No hay usuarios registrados en el momento.</td
                    ></tr
                  >
                </tbody>
              </table>
            </div>
          </div>
        {:else if subVistaInterna === "crear"}
          <UserForm
            {tiposDocumento}
            {facultades}
            {roles}
            on:guardado={() => (subVistaInterna = "lista")}
          />
        {/if}
      </section>
    {:else if vistaActual === "cursos"}
      <section class="animate__animated animate__fadeIn">
        <h2 class="fw-bold text-dark mb-4">Administrar Cursos</h2>
        <SubNav
          opciones={opcionesCurso}
          vistaActiva={subVistaInterna}
          on:cambio={(e) => (subVistaInterna = e.detail)}
        />

        {#if subVistaInterna === "lista"}
          <div class="card shadow-sm border-0 rounded-4 p-4 mt-2">
            <h5 class="fw-bold mb-3">Lista de Cursos Activos</h5>
            <div class="table-responsive">
              <table class="table table-hover align-middle mb-0">
                <thead class="bg-light text-muted">
                  <tr>
                    <th>ID</th><th>Deporte</th><th>Entrenador</th><th>Días</th
                    ><th>Hora</th><th>Cupo</th><th class="text-end">Acciones</th
                    >
                  </tr>
                </thead>
                <tbody>
                  <tr
                    ><td colspan="7" class="text-center py-4 text-muted"
                      >No hay cursos registrados en el momento.</td
                    ></tr
                  >
                </tbody>
              </table>
            </div>
          </div>
        {:else if subVistaInterna === "crear"}
          <CourseForm
            {deportes}
            {entrenadores}
            on:guardado={() => (subVistaInterna = "lista")}
          />
        {:else if subVistaInterna === "inscritos"}
          <div
            class="card shadow-sm border-0 rounded-4 p-5 mt-2 text-center bg-light"
          >
            <i class="bi bi-people-fill display-3 text-secondary mb-3"></i>
            <h4 class="fw-bold text-dark mb-2">Consulta de Inscritos</h4>
            <p class="text-muted mx-auto" style="max-width: 400px;">
              Seleccione un curso activo desde la pestaña de Lista para
              visualizar la lista detallada de estudiantes inscritos.
            </p>
          </div>
        {/if}
      </section>

      <!-- Vista Gestión deportes -->
    {:else if vistaActual === "deportes"}
      <section class="animate__animated animate__fadeIn">
        <h2 class="fw-bold text-dark mb-4">Administrar Deportes</h2>
        <p class="text-muted">
          Utilice este módulo para agregar o editar los deportes ofrecidos por
          la IUB.
        </p>
      </section>

      <!-- Vista Auditorias -->
    {:else if vistaActual === "auditorias"}
      <section class="animate__animated animate__fadeIn">
        <h2 class="fw-bold text-dark mb-4">Administrar Auditorias</h2>
        <p class="text-muted">
          Utilice este módulo para agregar o editar las auditorias de la IUB.
        </p>
      </section>
    {/if}
  </main>
</div>
