<script>
  import { rol } from './store.js'
  import Login from './components/Login.svelte'
  import AdminPanel from './components/AdminPanel.svelte'
  import EntrenadorPanel from './components/EntrenadorPanel.svelte'
  import EstudiantePanel from './components/EstudiantePanel.svelte'

  let tipoRol
  rol.subscribe(value => tipoRol = value)
</script>

{#if !tipoRol}
  <Login />
{:else if tipoRol === "admin"}
  <AdminPanel />
{:else if tipoRol === "entrenador"}
  <EntrenadorPanel />
{:else}
  <EstudiantePanel />
{/if}