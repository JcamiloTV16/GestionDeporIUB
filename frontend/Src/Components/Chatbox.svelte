<script>
  let mensaje = "";
  let mensajes = [
    {
      text: "¡Hola! Soy tu Asistente Virtual UniBarranquilla. ¿En qué puedo ayudarte hoy?",
      from: "bot",
    },
  ];

  function enviar() {
    if (!mensaje.trim()) return;

    mensajes = [...mensajes, { text: mensaje, from: "user" }];

    let respuesta = "";
    const m = mensaje.toLowerCase();

    if (m.includes("inscribirme") || m.includes("inscripcion")) {
      respuesta =
        "Para inscribirte, ve a la pestaña 'Inscripción' en la parte superior, selecciona tu deporte y confirma tu registro.";
    } else if (
      m.includes("horario") ||
      m.includes("hora") ||
      m.includes("cuándo")
    ) {
      respuesta =
        "Puedes consultar los horarios haciendo clic en 'Ver Horarios' dentro de cada deporte en la pestaña 'Deportes'.";
    } else if (m.includes("torneo")) {
      respuesta =
        "En la pestaña 'Torneos' encontrarás la lista de eventos competitivos actuales y próximos.";
    } else {
      respuesta =
        "Lo siento, no comprendo tu consulta específica. ¿Deseas saber sobre inscripciones, horarios o torneos?";
    }

    mensaje = "";

    setTimeout(() => {
      mensajes = [...mensajes, { text: respuesta, from: "bot" }];
      // Scroll to bottom
      const body = document.getElementById("chatBody");
      if (body) setTimeout(() => (body.scrollTop = body.scrollHeight), 100);
    }, 500);
  }
</script>

<div
  class="chat-widget shadow-lg border-0 rounded-4 overflow-hidden bg-white animate__animated animate__fadeInUp"
>
  <div
    class="chat-header bg-primary p-3 text-white d-flex align-items-center justify-content-between"
  >
    <div class="d-flex align-items-center">
      <div
        class="bot-avatar me-2 bg-white rounded-circle d-flex align-items-center justify-content-center"
        style="width: 32px; height: 32px;"
      >
        <i class="bi bi-robot text-primary"></i>
      </div>
      <h6 class="m-0 fw-bold">Asistente Virtual</h6>
    </div>
    <div class="status-dot"></div>
  </div>

  <div class="chat-body p-3" id="chatBody">
    {#each mensajes as msg}
      <div class="message-wrapper mb-3 {msg.from === 'bot' ? '' : 'text-end'}">
        <div
          class="message-bubble d-inline-block px-3 py-2 rounded-4 shadow-sm {msg.from ===
          'bot'
            ? 'bg-light text-dark'
            : 'bg-primary text-white'}"
        >
          {msg.text}
        </div>
      </div>
    {/each}
  </div>

  <div class="chat-footer p-2 bg-light d-flex gap-2">
    <input
      id="chatInput"
      class="form-control rounded-pill border-0 shadow-none px-3"
      placeholder="Escribe algo..."
      bind:value={mensaje}
      on:keydown={(e) => e.key === "Enter" && enviar()}
    />
    <button
      class="btn btn-primary rounded-circle d-flex align-items-center justify-content-center"
      on:click={enviar}
      style="width: 38px; height: 38px;"
    >
      <i
        class="bi bi-send-fill"
        style="transform: translateX(-1px) translateY(1px)"
      ></i>
    </button>
  </div>
</div>

<style>
  .chat-widget {
    border: 1px solid #eee;
  }
  .chat-body {
    height: 300px;
    overflow-y: auto;
    background-color: #fcfcfc;
    scroll-behavior: smooth;
  }
  .chat-header {
    border-bottom: 2px solid rgba(0, 0, 0, 0.05);
  }
  .status-dot {
    width: 10px;
    height: 10px;
    background-color: #4cd964;
    border-radius: 50%;
    border: 2px solid white;
  }
  .message-bubble {
    max-width: 85%;
    font-size: 0.9rem;
    line-height: 1.4;
    word-wrap: break-word;
  }
  .message-bubble.bg-light {
    border-bottom-left-radius: 4px;
    border: 1px solid #e9ecef;
  }
  .message-bubble.bg-primary {
    border-bottom-right-radius: 4px;
  }
</style>
