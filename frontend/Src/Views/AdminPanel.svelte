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
    obtenerUsuariosInactivos,
    reactivarUsuario,
    obtenerDeportesInactivos,
    reactivarDeporte,
    obtenerHorariosInactivos,
    reactivarHorario,
    inscribirEstudiante,
  } from "../Services/Api.js";
  import DashboardInfo from "../Components/dashboardInfo.svelte";
  import ListaUsuarios from "../Components/listaUsuarios.svelte";
  import ListaCursos from "../Components/listaCursos.svelte";
  import ListaEstudiantes from "../Components/listaEstudiantes.svelte";
  import GestionDepor from "../Components/gestionDepor.svelte";
  import ListaAuditorias from "../Components/listaAuditorias.svelte";
  import GestionTorneos from "../Components/GestionTorneos.svelte";
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
  let usuariosInactivos = [];
  let deportesInactivos = [];
  let cursosInactivos = [];
  let cursoSeleccionado = null;
  let inscritos = [];
  let cargandoInscritos = false;
  let usuarioAEditar = null;
  let cursoAEditar = null;

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

      const resNiveles = await fetch(`http://localhost:3000/niveles-educativos`);
      nivelesEducativos = await resNiveles.json();

      const resProgramas = await fetch(`http://localhost:3000/programas`);
      programas = await resProgramas.json();

      // Backend Python
      const resRoles = await fetch(`${API}/roles/`);
      const dataRoles = await resRoles.json();
      roles = dataRoles.resultado || [];

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
        
        const resInactivos = await obtenerUsuariosInactivos(currentToken);
        usuariosInactivos = resInactivos.resultado || [];

        const resDeportesInactivos = await obtenerDeportesInactivos(currentToken);
        deportesInactivos = resDeportesInactivos.resultado || [];

        const resCursosInactivos = await obtenerHorariosInactivos(currentToken);
        cursosInactivos = resCursosInactivos.resultado || [];
      }
    } catch (error) {
      console.error("Error al cargar auditorias e inactivos:", error);
    }
  }

  async function refrescarTodo() {
    try {
      const currentToken = get(token);
      if (!currentToken) return;
      
      await cargarDeportes();
      
      const resEntrenadores = await fetch(`${API}/entrenadores/`);
      entrenadores = (await resEntrenadores.json()).resultado || [];
      
      const resUsuarios = await obtenerUsuarios(currentToken);
      usuarios = resUsuarios.resultado || [];
      
      const resCursos = await obtenerHorarios(currentToken);
      cursos = resCursos.resultado || [];
      
      await cargarAuditorias();
    } catch (error) {
      console.error("Error al refrescar todos los datos:", error);
    }
  }

  async function manejarReactivarUsuario(id) {
    try {
      const currentToken = get(token);
      await reactivarUsuario(id, currentToken);
      alert("Usuario reactivado con éxito.");
      await refrescarTodo();
    } catch (error) {
      console.error("Error al reactivar usuario:", error);
      mensajeEstado = { texto: "Error al reactivar", tipo: "danger" };
      setTimeout(() => (mensajeEstado = { texto: "", tipo: "" }), 3000);
    }
  }

  async function manejarReactivarDeporte(id) {
    try {
      const currentToken = get(token);
      await reactivarDeporte(id, currentToken);
      alert("Deporte reactivado con éxito.");
      await refrescarTodo();
    } catch (error) {
      console.error("Error al reactivar deporte:", error);
      mensajeEstado = { texto: "Error al reactivar", tipo: "danger" };
      setTimeout(() => (mensajeEstado = { texto: "", tipo: "" }), 3000);
    }
  }

  async function manejarReactivarHorario(id) {
    try {
      const currentToken = get(token);
      await reactivarHorario(id, currentToken);
      alert("Curso reactivado con éxito.");
      await refrescarTodo();
    } catch (error) {
      console.error("Error al reactivar curso:", error);
      mensajeEstado = { texto: "Error al reactivar", tipo: "danger" };
      setTimeout(() => (mensajeEstado = { texto: "", tipo: "" }), 3000);
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
        alert("Deporte actualizado con éxito.");
      } else {
        await agregarDeporte(nuevoDeporte);
        alert("Deporte guardado con éxito.");
      }
      nuevoDeporte = { nombre: "", descripcion: "" };
      editandoId = null;
      subVistaInterna = "lista";
      await refrescarTodo();
    } catch (error) {
      mensajeEstado = { texto: "Error al guardar deporte", tipo: "danger" };
      setTimeout(() => (mensajeEstado = { texto: "", tipo: "" }), 3000);
    }
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
      alert("Deporte eliminado con éxito.");
      await refrescarTodo();
    } catch (error) {
      mensajeEstado = { texto: "Error al eliminar", tipo: "danger" };
      setTimeout(() => (mensajeEstado = { texto: "", tipo: "" }), 3000);
    }
  }

  async function manejarEliminarUsuario(id) {
    if (!confirm("¿Estás seguro de eliminar este usuario?")) return;
    try {
      const currentToken = get(token);
      await eliminarUsuario(id, currentToken);
      alert("Usuario eliminado con éxito.");
      await refrescarTodo();
    } catch (error) {
      console.error("Error al eliminar usuario:", error);
      mensajeEstado = { texto: "Error al eliminar usuario", tipo: "danger" };
      setTimeout(() => (mensajeEstado = { texto: "", tipo: "" }), 3000);
    }
  }

  async function manejarEliminarHorario(id) {
    if (!confirm("¿Estás seguro de desactivar este curso?")) return;
    try {
      const currentToken = get(token);
      await fetch(`${API}/horarios/${id}`, {
        method: "DELETE",
        headers: { "Authorization": `Bearer ${currentToken}` }
      });
      alert("Curso desactivado con éxito.");
      await refrescarTodo();
    } catch (error) {
      console.error("Error al desactivar curso:", error);
      mensajeEstado = { texto: "Error al desactivar", tipo: "danger" };
      setTimeout(() => (mensajeEstado = { texto: "", tipo: "" }), 3000);
    }
  }

  function prepararEdicionUsuario(usuario) {
    usuarioAEditar = usuario;
    subVistaInterna = "crear";
  }

  async function manejarInscribirEstudiante(datos) {
    try {
      const currentToken = get(token);
      await inscribirEstudiante(datos, currentToken);
      alert("Estudiante inscrito con éxito.");
      await refrescarTodo();
      if (cursoSeleccionado) {
        await verInscritos(cursoSeleccionado);
      }
    } catch (error) {
      console.error("Error al inscribir estudiante:", error);
      mensajeEstado = { texto: "Error al inscribir estudiante", tipo: "danger" };
      setTimeout(() => (mensajeEstado = { texto: "", tipo: "" }), 3000);
    }
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
    <!-- Menu Torneos -->
    <button
      class="btn-pestana {vistaActual === 'torneos' ? 'activa' : ''}"
      on:click={() => cambiarVistaPrincipal("torneos")}
    >
      <i class="bi bi-trophy me-2"></i>Torneos
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
              await refrescarTodo();
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
            on:eliminar={(e) => manejarEliminarHorario(e.detail)}
            on:editar={(e) => {
              cursoAEditar = e.detail;
              subVistaInterna = "crear";
            }}
          />
        {:else if subVistaInterna === "crear"}
          <CourseForm
            {deportes}
            {entrenadores}
            {cursoAEditar}
            on:guardado={async () => {
              cursoAEditar = null;
              subVistaInterna = "lista";
              await refrescarTodo();
            }}
            on:cancelar={() => {
              cursoAEditar = null;
              subVistaInterna = "lista";
            }}
          />
        {:else if subVistaInterna === "inscritos"}
          <ListaEstudiantes
            {cursoSeleccionado}
            {inscritos}
            {deportes}
            {usuarios}
            {programas}
            {cargandoInscritos}
            on:volver={() => {
              cursoSeleccionado = null;
              subVistaInterna = "lista";
            }}
            on:inscribir={(e) => manejarInscribirEstudiante(e.detail)}
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
        <h2 class="fw-bold text-dark mb-4">Registro de Auditoría y Usuarios Inactivos</h2>
        <ListaAuditorias 
          {auditorias} 
          {usuarios} 
          {usuariosInactivos}
          {deportesInactivos}
          {cursosInactivos}
          on:reactivarUsuario={(e) => manejarReactivarUsuario(e.detail)}
          on:reactivarDeporte={(e) => manejarReactivarDeporte(e.detail)}
          on:reactivarHorario={(e) => manejarReactivarHorario(e.detail)}
        />
      </section>
    {:else if vistaActual === "torneos"}
      <section class="animate__animated animate__fadeIn">
        <h2 class="fw-bold text-dark mb-4">Gestión de Torneos</h2>
        <GestionTorneos />
      </section>
    {/if}
  </main>
</div>