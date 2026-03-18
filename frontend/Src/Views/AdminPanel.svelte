<script>
  import { onMount } from "svelte";
  import { cerrarSesion } from "../Store.js";
  import SubNav from "../Components/SubNav.svelte";
  import UserForm from "../Components/UserForm.svelte";
  import CourseForm from "../Components/CourseForm.svelte";
  import "../Styles/AdminPanel.css";
  import {
    API,
    obtenerUsuarios,
    actualizarUsuario,
    eliminarUsuario,
    obtenerHorarios,
    obtenerInscritosPorHorario,
    obtenerDeportes,
    agregarDeporte,
    eliminarDeporte,
    actualizarDeporte,
    obtenerAuditorias,
  } from "../Services/Api.js";
  import DashboardInfo from "../Components/dashboardInfo.svelte";
  import ListaUsuarios from "../Components/listaUsuarios.svelte";
  import ListaCursos from "../Components/listaCursos.svelte";
  import ListaEstudiantes from "../Components/listaEstudiantes.svelte";
  import GestionDepor from "../Components/gestionDepor.svelte";
  import ListaAuditorias from "../Components/listaAuditorias.svelte";
  import { token } from "../Store.js";
  import { get } from "svelte/store";

  let vistaActual = "dashboard";
  let subVistaInterna = "lista";

  // Datos dinámicos para pasar a los componentes
  let tiposDocumento = [];
  let facultades = [];
  let roles = [];
  let deportes = [];
  let entrenadores = [];
  let usuarios = [];
  let cursos = [];
  let programas = [];
  let nivelesEducativos = [];
  let auditorias = [];
  let cursoSeleccionado = null;
  let inscritos = [];
  let cargandoInscritos = false;
  let usuarioAEditar = null;

  let nuevoDeporte = { nombre: "", descripcion: "" };
  let editandoId = null;
  let mensajeEstado = { texto: "", tipo: "" };

  const opcionesCurso = [
    { id: "lista", texto: "Lista", icono: "bi bi-list-ul" },
    { id: "crear", texto: "Crear", icono: "bi bi-plus-circle" },
    { id: "inscritos", texto: "Inscritos", icono: "bi bi-people" },
  ];

  const opcionesUsuario = [
    { id: "lista", texto: "Lista", icono: "bi bi-list-ul" },
    { id: "crear", texto: "Crear", icono: "bi bi-person-plus" },
  ];

  const opcionesDeporte = [
    { id: "lista", texto: "Lista", icono: "bi bi-list-ul" },
    { id: "crear", texto: "Crear", icono: "bi bi-plus-circle" },
  ];

  async function cargarDeportes() {
    try {
      const res = await obtenerDeportes();
      deportes = res.resultado || [];
    } catch (error) {
      console.error("Error al cargar deportes:", error);
    }
  }

  //carga de datos y coneción con las bases de datos
  onMount(async () => {
    try {
      // backend node (Puerto 3000)
      const resTipos = await fetch(`http://localhost:3000/tipos-documento`);
      tiposDocumento = await resTipos.json();

      const resFacultades = await fetch(`http://localhost:3000/facultades`);
      facultades = await resFacultades.json();

      const resNiveles = await fetch(
        `http://localhost:3000/niveles-educativos`,
      );
      nivelesEducativos = await resNiveles.json();

      const resProgramas = await fetch(`http://localhost:3000/programas`);
      programas = await resProgramas.json();

      // Backend Python
      const resRoles = await fetch(`${API}/roles/`);
      roles = (await resRoles.json()).resultado || [];
      console.log("Roles cargados:", roles);

      await cargarDeportes();

      const resEntrenadores = await fetch(`${API}/entrenadores/`);
      entrenadores = (await resEntrenadores.json()).resultado || [];

      // tokens de usuarios
      const currentToken = get(token);
      if (currentToken) {
        const resUsuarios = await obtenerUsuarios(currentToken);
        usuarios = resUsuarios.resultado || [];

        const resCursos = await obtenerHorarios(currentToken);
        cursos = resCursos.resultado || [];
        console.log("Cursos cargados:", cursos);
        console.log("Entrenadores cargados:", entrenadores);
      }
    } catch (error) {
      console.error("Error cargando datos iniciales:", error);
    }
  });

  async function cargarAuditorias() {
    try {
      const currentToken = get(token);
      if (currentToken) {
        const res = await obtenerAuditorias(currentToken);
        auditorias = res.resultado || [];
      }
    } catch (error) {
      console.error("Error al cargar auditorias:", error);
    }
  }

  function cambiarVistaPrincipal(vista) {
    vistaActual = vista;
    subVistaInterna = "lista";
    if (vista !== "cursos") {
      cursoSeleccionado = null;
      inscritos = [];
    }
    if (vista === "auditorias") {
      cargarAuditorias();
    }
  }

  async function verInscritos(curso) {
    cursoSeleccionado = curso;
    subVistaInterna = "inscritos";
    cargandoInscritos = true;
    try {
      const currentToken = get(token);
      const res = await obtenerInscritosPorHorario(curso.id, currentToken);
      inscritos = res.resultado || [];
    } catch (error) {
      console.error("Error cargando inscritos:", error);
    } finally {
      cargandoInscritos = false;
    }
  }

  async function manejarGuardarDeporte() {
    try {
      if (editandoId) {
        await actualizarDeporte(editandoId, nuevoDeporte);
        mensajeEstado = {
          texto: "Deporte actualizado con éxito",
          tipo: "success",
        };
      } else {
        await agregarDeporte(nuevoDeporte);
        mensajeEstado = {
          texto: "Deporte guardado con éxito",
          tipo: "success",
        };
      }
      nuevoDeporte = { nombre: "", descripcion: "" };
      editandoId = null;
      await cargarDeportes();
      subVistaInterna = "lista";
    } catch (error) {
      mensajeEstado = { texto: "Error al guardar deporte", tipo: "danger" };
    }
    setTimeout(() => (mensajeEstado = { texto: "", tipo: "" }), 3000);
  }

  function prepararEdicionDeporte(deporte) {
    nuevoDeporte = { nombre: deporte.nombre, descripcion: deporte.descripcion };
    editandoId = deporte.id;
    subVistaInterna = "crear";
  }

  async function manejarEliminarDeporte(id) {
    if (!confirm("¿Estás seguro de eliminar este deporte?")) return;
    try {
      await eliminarDeporte(id);
      mensajeEstado = { texto: "Deporte eliminado", tipo: "success" };
      await cargarDeportes();
    } catch (error) {
      mensajeEstado = { texto: "Error al eliminar", tipo: "danger" };
    }
    setTimeout(() => (mensajeEstado = { texto: "", tipo: "" }), 3000);
  }

  async function manejarEliminarUsuario(id) {
    if (!confirm("¿Estás seguro de eliminar este usuario?")) return;
    try {
      const currentToken = get(token);
      await eliminarUsuario(id, currentToken);
      mensajeEstado = { texto: "Usuario eliminado", tipo: "success" };
      // Recargar lista
      const resUsuarios = await obtenerUsuarios(currentToken);
      usuarios = resUsuarios.resultado || [];
    } catch (error) {
      console.error("Error al eliminar usuario:", error);
      mensajeEstado = { texto: "Error al eliminar usuario", tipo: "danger" };
    }
    setTimeout(() => (mensajeEstado = { texto: "", tipo: "" }), 3000);
  }

  function prepararEdicionUsuario(usuario) {
    usuarioAEditar = usuario;
    subVistaInterna = "crear";
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
      <DashboardInfo />
    {:else if vistaActual === "usuarios"}
      <section class="animate__animated animate__fadeIn">
        <h2 class="fw-bold text-dark mb-4">Administrar Usuarios</h2>
        <SubNav
          opciones={opcionesUsuario}
          vistaActiva={subVistaInterna}
          on:cambio={(e) => (subVistaInterna = e.detail)}
        />

        {#if subVistaInterna === "lista"}
          <ListaUsuarios 
            {usuarios} 
            {roles} 
            {tiposDocumento} 
            on:editar={(e) => prepararEdicionUsuario(e.detail)}
            on:eliminar={(e) => manejarEliminarUsuario(e.detail)}
          />
        {:else if subVistaInterna === "crear"}
          <UserForm
            {tiposDocumento}
            {facultades}
            {nivelesEducativos}
            {programas}
            {roles}
            {usuarioAEditar}
            on:guardado={async () => {
              usuarioAEditar = null;
              subVistaInterna = "lista";
              const currentToken = get(token);
              const resUsuarios = await obtenerUsuarios(currentToken);
              usuarios = resUsuarios.resultado || [];
            }}
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
          <ListaCursos
            {cursos}
            {deportes}
            {entrenadores}
            on:verInscritos={(e) => verInscritos(e.detail)}
          />
        {:else if subVistaInterna === "crear"}
          <CourseForm
            {deportes}
            {entrenadores}
            on:guardado={() => (subVistaInterna = "lista")}
          />
        {:else if subVistaInterna === "inscritos"}
          <ListaEstudiantes
            {cursoSeleccionado}
            {inscritos}
            {deportes}
            {cargandoInscritos}
            on:volver={() => {
              cursoSeleccionado = null;
              subVistaInterna = "lista";
            }}
          />
        {/if}
      </section>
    {:else if vistaActual === "deportes"}
      <section class="animate__animated animate__fadeIn">
        <h2 class="fw-bold text-dark mb-4">Administrar Deportes</h2>
        <SubNav
          opciones={opcionesDeporte}
          vistaActiva={subVistaInterna}
          on:cambio={(e) => (subVistaInterna = e.detail)}
        />

        <GestionDepor
          {subVistaInterna}
          {deportes}
          {nuevoDeporte}
          {editandoId}
          {mensajeEstado}
          on:guardar={manejarGuardarDeporte}
          on:editar={(e) => prepararEdicionDeporte(e.detail)}
          on:eliminar={(e) => manejarEliminarDeporte(e.detail)}
          on:cancelar={() => {
            editandoId = null;
            nuevoDeporte = { nombre: "", descripcion: "" };
            subVistaInterna = "lista";
          }}
        />
      </section>
    {:else if vistaActual === "auditorias"}
      <section class="animate__animated animate__fadeIn">
        <h2 class="fw-bold text-dark mb-4">Registro de Auditoría</h2>
        <ListaAuditorias {auditorias} {usuarios} />
      </section>
    {/if}
  </main>
</div>