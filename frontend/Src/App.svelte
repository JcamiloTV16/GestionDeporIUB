<script>
  import { rol } from "./Store.js";
  import Header from "./Components/Header.svelte";
  import Login from "./Views/Login.svelte";
  import OlvidoContra from "./Views/OlvidoContra.svelte";
  import AdminPanel from "./Views/AdminPanel.svelte";
  import EntrenadorPanel from "./Views/EntrenadorPanel.svelte";
  import EstudiantePanel from "./Views/EstudiantePanel.svelte";
  import Navbar from "./Components/Navbar.svelte";
  import Footer from "./Components/Footer.svelte";
  import Perfil from "./Views/Perfil.svelte";
  import { onMount, onDestroy } from "svelte";

  let currentHash = "";

  let tipoRol;
  rol.subscribe((value) => (tipoRol = value));

  function handleHashChange() {
    currentHash = window.location.hash;
  }

  onMount(() => {
    handleHashChange();
    window.addEventListener("hashchange", handleHashChange);
  });

  onDestroy(() => {
    window.removeEventListener("hashchange", handleHashChange);
  });
</script>

<div class="app-container min-vh-100 d-flex flex-column">
  {#if currentHash === "#/recover"}
    <OlvidoContra />
  {:else if !tipoRol}
    <Login />
  {:else}
    <Navbar />
    <main class="flex-grow-1">
      {#if currentHash === "#/perfil"}
        <Perfil on:volver={() => window.location.hash = ""} />
      {:else if tipoRol === "admin"}
        <AdminPanel />
      {:else if tipoRol === "entrenador"}
        <EntrenadorPanel />
      {:else}
        <EstudiantePanel />
      {/if}
    </main>
    <Footer />
  {/if}
</div>

<style>
  .app-container {
    background-color: #f8f9fa;
  }
</style>
