<script>
  import { rol } from "./Store.js";
  import Login from "./Components/Login.svelte";
  import AdminPanel from "./Components/AdminPanel.svelte";
  import EntrenadorPanel from "./Components/EntrenadorPanel.svelte";
  import EstudiantePanel from "./Components/EstudiantePanel.svelte";
  import Navbar from "./Components/Navbar.svelte";

  let tipoRol;
  rol.subscribe((value) => (tipoRol = value));
</script>

{#if !tipoRol}
  <Login />
{:else}
  <Navbar />
  {#if tipoRol === "admin"}
    <AdminPanel />
  {:else if tipoRol === "entrenador"}
    <EntrenadorPanel />
  {:else}
    <EstudiantePanel />
  {/if}
{/if}
