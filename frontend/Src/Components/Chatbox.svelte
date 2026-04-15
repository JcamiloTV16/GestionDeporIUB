<script>
  import { enviarMensajeChatbot } from "../Services/Api.js";

  let mensaje = "";
  let abierto = false;
  let escribiendo = false;
  let mensajes = [
    {
      text: "¡Hola! 👋 Soy tu Asistente Virtual UniBarranquilla. ¿En qué puedo ayudarte hoy?",
      from: "bot",
    },
  ];

  async function enviar() {
    if (!mensaje.trim()) return;

    const textoUsuario = mensaje.trim();
    mensajes = [...mensajes, { text: textoUsuario, from: "user" }];
    mensaje = "";
    escribiendo = true;
    scrollAbajo();

    try {
      const res = await enviarMensajeChatbot(textoUsuario);
      mensajes = [...mensajes, { text: res.respuesta, from: "bot" }];
    } catch (e) {
      mensajes = [
        ...mensajes,
        {
          text: "⚠️ Ocurrió un error al conectar con el servidor. Intenta de nuevo más tarde.",
          from: "bot",
        },
      ];
    } finally {
      escribiendo = false;
      scrollAbajo();
    }
  }

  function scrollAbajo() {
    setTimeout(() => {
      const body = document.getElementById("chatBody");
      if (body) body.scrollTop = body.scrollHeight;
    }, 100);
  }

  function formatearTexto(texto) {
    // Convierte **texto** a <strong> y \n a <br>
    return texto
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
      .replace(/\n/g, '<br>');
  }
</script>

{#if !abierto}
  <!-- Botón flotante para abrir el chat -->
  <button class="chat-fab shadow-lg" on:click={() => (abierto = true)} title="Abrir asistente">
    <i class="bi bi-chat-dots-fill"></i>
  </button>
{:else}
  <!-- Chat abierto -->
  <div class="chat-widget shadow-lg border-0 rounded-4 overflow-hidden bg-white animate__animated animate__fadeInUp animate__faster">
    <div class="chat-header bg-primary p-3 text-white d-flex align-items-center justify-content-between">
      <div class="d-flex align-items-center">
        <div
          class="bot-avatar me-2 bg-white rounded-circle d-flex align-items-center justify-content-center"
          style="width: 32px; height: 32px;"
        >
          <i class="bi bi-robot text-primary"></i>
        </div>
        <div>
          <h6 class="m-0 fw-bold" style="font-size: 0.9rem;">Asistente Virtual</h6>
          <span class="small" style="font-size: 0.7rem; opacity: 0.8;">
            {escribiendo ? '✏️ Escribiendo...' : '🟢 En línea'}
          </span>
        </div>
      </div>
      <button class="btn btn-sm text-white p-0 minimize-btn" on:click={() => (abierto = false)} title="Minimizar">
        <i class="bi bi-dash-lg fs-5"></i>
      </button>
    </div>

    <div class="chat-body p-3" id="chatBody">
      {#each mensajes as msg}
        <div class="message-wrapper mb-3 {msg.from === 'bot' ? '' : 'text-end'}">
          {#if msg.from === 'bot'}
            <div class="d-flex align-items-start gap-2">
              <div class="bot-icon bg-primary-subtle rounded-circle d-flex align-items-center justify-content-center flex-shrink-0"
                   style="width: 26px; height: 26px;">
                <i class="bi bi-robot text-primary" style="font-size: 0.7rem;"></i>
              </div>
              <div class="message-bubble d-inline-block px-3 py-2 rounded-4 shadow-sm bg-light text-dark">
                {@html formatearTexto(msg.text)}
              </div>
            </div>
          {:else}
            <div class="message-bubble d-inline-block px-3 py-2 rounded-4 shadow-sm bg-primary text-white">
              {msg.text}
            </div>
          {/if}
        </div>
      {/each}
      {#if escribiendo}
        <div class="message-wrapper mb-3">
          <div class="d-flex align-items-start gap-2">
            <div class="bot-icon bg-primary-subtle rounded-circle d-flex align-items-center justify-content-center flex-shrink-0"
                 style="width: 26px; height: 26px;">
              <i class="bi bi-robot text-primary" style="font-size: 0.7rem;"></i>
            </div>
            <div class="message-bubble d-inline-block px-3 py-2 rounded-4 shadow-sm bg-light text-dark">
              <div class="typing-dots">
                <span></span><span></span><span></span>
              </div>
            </div>
          </div>
        </div>
      {/if}
    </div>

    <div class="chat-footer p-2 bg-light d-flex gap-2">
      <input
        id="chatInput"
        class="form-control rounded-pill border-0 shadow-none px-3"
        placeholder="Escribe algo..."
        bind:value={mensaje}
        on:keydown={(e) => e.key === "Enter" && enviar()}
        disabled={escribiendo}
      />
      <button
        class="btn btn-primary rounded-circle d-flex align-items-center justify-content-center"
        on:click={enviar}
        disabled={escribiendo}
        style="width: 38px; height: 38px;"
      >
        <i
          class="bi bi-send-fill"
          style="transform: translateX(-1px) translateY(1px)"
        ></i>
      </button>
    </div>
  </div>
{/if}

<style>
  .chat-fab {
    width: 56px;
    height: 56px;
    border-radius: 50%;
    border: none;
    background: linear-gradient(135deg, #0d6efd 0%, #0a58ca 100%);
    color: white;
    font-size: 1.4rem;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: all 0.3s ease;
  }
  .chat-fab:hover {
    transform: scale(1.1);
    box-shadow: 0 8px 25px rgba(13, 110, 253, 0.4) !important;
  }
  .chat-widget {
    border: 1px solid #eee;
    width: 100%;
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
  .minimize-btn {
    opacity: 0.8;
    transition: opacity 0.2s;
  }
  .minimize-btn:hover {
    opacity: 1;
  }
  .message-bubble {
    max-width: 85%;
    font-size: 0.85rem;
    line-height: 1.5;
    word-wrap: break-word;
  }
  .message-bubble.bg-light {
    border-bottom-left-radius: 4px !important;
    border: 1px solid #e9ecef;
  }
  .message-bubble.bg-primary {
    border-bottom-right-radius: 4px !important;
  }

  /* Typing indicator dots */
  .typing-dots {
    display: flex;
    gap: 4px;
    padding: 4px 0;
  }
  .typing-dots span {
    width: 7px;
    height: 7px;
    background-color: #adb5bd;
    border-radius: 50%;
    animation: typing 1.4s infinite ease-in-out;
  }
  .typing-dots span:nth-child(2) {
    animation-delay: 0.2s;
  }
  .typing-dots span:nth-child(3) {
    animation-delay: 0.4s;
  }
  @keyframes typing {
    0%, 60%, 100% { transform: translateY(0); opacity: 0.4; }
    30% { transform: translateY(-6px); opacity: 1; }
  }
</style>
