<script>
  import { obtenerDeportesEstudiante } from "../Services/Api.js";
  import { user } from "../Store.js";
  import { get } from "svelte/store";

  let misDeportes = [];
  let loading = false;

  // Mapa de nombres de deporte -> icono Bootstrap + color
  const iconosDeportes = {
    "fútbol":      { icono: "bi-dribbble",          color: "#28a745" },
    "futbol":      { icono: "bi-dribbble",          color: "#28a745" },
    "baloncesto":  { icono: "bi-basketball",        color: "#ff6b35" },
    "basketball":  { icono: "bi-basketball",        color: "#ff6b35" },
    "voleibol":    { icono: "bi-volleyball",        color: "#ffc107" },
    "volleyball":  { icono: "bi-volleyball",        color: "#ffc107" },
    "tenis":       { icono: "bi-circle",            color: "#c8e600" },
    "natación":    { icono: "bi-water",             color: "#0dcaf0" },
    "natacion":    { icono: "bi-water",             color: "#0dcaf0" },
    "atletismo":   { icono: "bi-person-walking",    color: "#dc3545" },
    "ciclismo":    { icono: "bi-bicycle",           color: "#6f42c1" },
    "boxeo":       { icono: "bi-hand-thumbs-up",    color: "#dc3545" },
    "golf":        { icono: "bi-flag",              color: "#198754" },
    "ajedrez":     { icono: "bi-puzzle",            color: "#6c757d" },
    "béisbol":     { icono: "bi-bullseye",          color: "#0d6efd" },
    "beisbol":     { icono: "bi-bullseye",          color: "#0d6efd" },
    "ping pong":   { icono: "bi-disc",              color: "#e83e8c" },
    "tenis de mesa": { icono: "bi-disc",            color: "#e83e8c" },
    "karate":      { icono: "bi-hand-index-thumb",  color: "#343a40" },
    "taekwondo":   { icono: "bi-hand-index-thumb",  color: "#0d6efd" },
    "gimnasia":    { icono: "bi-person-arms-up",    color: "#e83e8c" },
    "esgrima":     { icono: "bi-lightning",          color: "#6c757d" },
    "rugby":       { icono: "bi-dribbble",          color: "#198754" },
    "hockey":      { icono: "bi-disc",              color: "#0dcaf0" },
    "softball":    { icono: "bi-bullseye",          color: "#ffc107" },
    "patinaje":    { icono: "bi-wind",              color: "#6f42c1" },
    "levantamiento de pesas": { icono: "bi-heart-pulse", color: "#dc3545" },
    "pesas":       { icono: "bi-heart-pulse",       color: "#dc3545" },
    "crossfit":    { icono: "bi-heart-pulse",       color: "#ff6b35" },
    "yoga":        { icono: "bi-yin-yang",          color: "#198754" },
  };

  const defaultIcono = { icono: "bi-trophy-fill", color: "#0d6efd" };

  function getIcono(nombreDeporte) {
    if (!nombreDeporte) return defaultIcono;
    const key = nombreDeporte.toLowerCase().trim();
    // Buscar coincidencia exacta o parcial
    if (iconosDeportes[key]) return iconosDeportes[key];
    for (const [nombre, data] of Object.entries(iconosDeportes)) {
      if (key.includes(nombre) || nombre.includes(key)) return data;
    }
    return defaultIcono;
  }

  async function cargar() {
    loading = true;
    try {
      const currentUser = get(user);
      if (currentUser && currentUser.id) {
        const res = await obtenerDeportesEstudiante(currentUser.id);
        misDeportes = res.resultado || [];
      }
    } catch (e) {
      console.error("Error cargando mis deportes:", e);
    } finally {
      loading = false;
    }
  }

  function formatHora(hora) {
    if (!hora) return "";
    return hora.slice(0, 5);
  }

  cargar();
</script>

<div class="deportes-view">
  <div class="d-flex align-items-center mb-4">
    <div
      class="bg-primary text-white rounded-circle p-2 me-3 d-flex align-items-center justify-content-center"
      style="width: 40px; height: 40px;"
    >
      <i class="bi bi-trophy-fill"></i>
    </div>
    <h4 class="fw-bold m-0">Mis Deportes</h4>
  </div>

  {#if loading}
    <div class="text-center py-5">
      <div class="spinner-border text-primary" role="status"></div>
      <p class="mt-2 text-muted">Cargando tus deportes...</p>
    </div>
  {:else if misDeportes.length === 0}
    <div class="alert alert-light border text-center py-5 rounded-4">
      <i class="bi bi-info-circle fs-2 text-muted mb-3 d-block"></i>
      No estás inscrito en ningún deporte aún. Ve a la pestaña <strong>Inscripción</strong> para registrarte.
    </div>
  {:else}
    <div class="row g-4">
      {#each misDeportes as deporte}
        {@const iconData = getIcono(deporte.nombre)}
        <div class="col-md-6 col-lg-4">
          <div class="card h-100 border-0 shadow-sm rounded-4 overflow-hidden sport-card">
            <div class="card-img-top d-flex align-items-center justify-content-center py-4"
                 style="background: linear-gradient(135deg, {iconData.color}15, {iconData.color}30);">
              <div class="sport-icon-circle d-flex align-items-center justify-content-center"
                   style="background: {iconData.color}; width: 70px; height: 70px; border-radius: 50%; box-shadow: 0 8px 20px {iconData.color}40;">
                <i class="bi {iconData.icono} text-white" style="font-size: 1.8rem;"></i>
              </div>
            </div>
            <div class="card-body p-4">
              <h5 class="fw-bold mb-3">{deporte.nombre}</h5>
              {#if deporte.dia_semana}
                <div class="d-flex align-items-center text-muted small mb-2">
                  <i class="bi bi-calendar3 me-2" style="color: {iconData.color}"></i>
                  <span>{deporte.dia_semana}</span>
                </div>
              {/if}
              {#if deporte.hora_inicio}
                <div class="d-flex align-items-center text-muted small mb-2">
                  <i class="bi bi-clock me-2" style="color: {iconData.color}"></i>
                  <span>{formatHora(deporte.hora_inicio)} - {formatHora(deporte.hora_fin)}</span>
                </div>
              {/if}
              {#if deporte.lugar}
                <div class="d-flex align-items-center text-muted small">
                  <i class="bi bi-geo-alt me-2" style="color: {iconData.color}"></i>
                  <span>{deporte.lugar}</span>
                </div>
              {/if}
            </div>
          </div>
        </div>
      {/each}
    </div>
  {/if}
</div>

<style>
  .sport-card {
    transition: all 0.3s ease;
  }
  .sport-card:hover {
    transform: translateY(-8px);
    box-shadow: 0 15px 30px rgba(0, 0, 0, 0.08) !important;
  }
  .sport-icon-circle {
    transition: transform 0.3s ease;
  }
  .sport-card:hover .sport-icon-circle {
    transform: scale(1.1);
  }
</style>
