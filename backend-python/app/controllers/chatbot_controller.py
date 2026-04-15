import unicodedata
import re

def limpiar_texto(texto: str) -> str:
    """Convierte a minúsculas y elimina tildes/acentos para facilitar búsqueda."""
    texto = texto.lower().strip()
    # Eliminar tildes/acentos
    nfkd = unicodedata.normalize('NFKD', texto)
    texto_limpio = ''.join(c for c in nfkd if not unicodedata.combining(c))
    # Eliminar caracteres especiales excepto espacios
    texto_limpio = re.sub(r'[^\w\s]', '', texto_limpio)
    return texto_limpio

def contiene_alguna(texto: str, palabras: list) -> bool:
    """Verifica si el texto contiene alguna de las palabras clave."""
    for palabra in palabras:
        if palabra in texto:
            return True
    return False

def detectar_intencion(mensaje_original: str) -> dict:
    """
    Detecta la intención del usuario usando palabras clave y devuelve
    una respuesta contextual de Bienestar Universitario.
    """
    texto = limpiar_texto(mensaje_original)

    # --- SALUDOS ---
    palabras_saludo = ["hola", "buenas", "que tal", "buenos dias", "buenas tardes",
                       "buenas noches", "hey", "saludos", "ey", "hi", "hello"]
    if contiene_alguna(texto, palabras_saludo):
        return {
            "intencion": "saludo",
            "respuesta": (
                "¡Hola! 👋 Soy el Asistente Virtual de Bienestar Universitario de la "
                "Universidad de Barranquilla (IUB). Estoy aquí para ayudarte con información "
                "sobre deportes, inscripciones, horarios y torneos. ¿En qué puedo ayudarte?"
            )
        }

    # --- DESPEDIDA ---
    palabras_despedida = ["adios", "chao", "hasta luego", "nos vemos", "bye", "gracias", "muchas gracias"]
    if contiene_alguna(texto, palabras_despedida):
        return {
            "intencion": "despedida",
            "respuesta": (
                "¡Hasta pronto! 😊 Fue un gusto ayudarte. Si necesitas algo más, "
                "no dudes en escribirme. ¡Éxitos en tus actividades deportivas!"
            )
        }

    # --- INSCRIPCIONES ---
    palabras_inscripcion = ["inscribir", "inscripcion", "registro", "registrar", "entrar",
                            "como me inscribo", "quiero inscribirme", "unirme", "apuntar",
                            "matricular", "anotarme", "participar"]
    if contiene_alguna(texto, palabras_inscripcion):
        return {
            "intencion": "inscripcion",
            "respuesta": (
                "📋 Para inscribirte en un deporte, sigue estos pasos:\n\n"
                "1. Ve a la pestaña **'Inscripción'** en el menú superior de tu panel.\n"
                "2. Selecciona la **disciplina deportiva** que te interese.\n"
                "3. Escoge el **grupo/horario** disponible.\n"
                "4. Haz clic en **'Confirmar Inscripción'**.\n\n"
                "¡Y listo! Quedarás inscrito automáticamente. Si tienes algún problema, "
                "contacta a la Coordinación de Deportes."
            )
        }

    # --- HORARIOS ---
    palabras_horario = ["horario", "hora", "horas", "cuando", "dias", "dia",
                        "que dia", "a que hora", "calendario", "programacion",
                        "lunes", "martes", "miercoles", "jueves", "viernes", "sabado"]
    if contiene_alguna(texto, palabras_horario):
        return {
            "intencion": "horarios",
            "respuesta": (
                "🕐 Los horarios varían según el deporte y el grupo seleccionado. "
                "Para consultar los horarios disponibles:\n\n"
                "1. Ve a la pestaña **'Inscripción'** en tu panel.\n"
                "2. Selecciona un **deporte**.\n"
                "3. Se mostrarán los **grupos con sus horarios** (día, hora inicio/fin y lugar).\n\n"
                "Los entrenamientos generalmente se realizan de lunes a sábado en las "
                "instalaciones deportivas de la universidad."
            )
        }

    # --- DEPORTES DISPONIBLES ---
    palabras_deportes = ["que deportes", "deportes disponibles", "disciplinas", "que hay",
                         "deportes hay", "ofrecen", "opciones deportivas", "actividades",
                         "que puedo practicar", "lista de deportes"]
    if contiene_alguna(texto, palabras_deportes):
        return {
            "intencion": "deportes",
            "respuesta": (
                "⚽ La Universidad de Barranquilla ofrece diversas disciplinas deportivas, "
                "entre las que puedes encontrar:\n\n"
                "🏈 **Fútbol** — ⛹️ **Baloncesto** — 🏐 **Voleibol**\n"
                "🏊 **Natación** — 🏃 **Atletismo** — 🚴 **Ciclismo**\n\n"
                "Para ver la lista completa y actualizada de deportes, visita la pestaña "
                "**'Deportes'** en tu panel de estudiante. Allí encontrarás todos los deportes "
                "en los que estás inscrito."
            )
        }

    # --- TORNEOS ---
    palabras_torneos = ["torneo", "campeonato", "competencia", "copa", "competicion",
                        "interuniversitario", "interfacultades", "evento deportivo"]
    if contiene_alguna(texto, palabras_torneos):
        return {
            "intencion": "torneos",
            "respuesta": (
                "🏆 Para información sobre torneos:\n\n"
                "1. Ve a la pestaña **'Torneos'** en tu panel.\n"
                "2. Allí verás los torneos programados con su **estado actual**.\n"
                "3. Si un torneo tiene **'Inscripciones Abiertas'**, podrás inscribirte "
                "haciendo clic en el botón **'Inscribirme'**.\n"
                "4. Tu inscripción quedará **pendiente** hasta que un administrador la apruebe.\n\n"
                "¡No te pierdas las competencias universitarias!"
            )
        }

    # --- CONTACTO / UBICACIÓN ---
    palabras_contacto = ["contacto", "telefono", "correo", "email", "donde queda",
                         "ubicacion", "direccion", "oficina", "coordinacion"]
    if contiene_alguna(texto, palabras_contacto):
        return {
            "intencion": "contacto",
            "respuesta": (
                "📍 **Coordinación de Deportes - Bienestar Universitario**\n\n"
                "Puedes contactarnos a través de:\n"
                "• 📧 Correo: deportes@unibarranquilla.edu.co\n"
                "• 📞 Extensión: 1234\n"
                "• 🏢 Ubicación: Bloque de Bienestar Universitario, 2do piso\n\n"
                "Horario de atención: Lunes a Viernes, 8:00 AM - 5:00 PM"
            )
        }

    # --- PERFIL / CUENTA ---
    palabras_perfil = ["perfil", "mi cuenta", "datos personales", "cambiar contrasena",
                       "password", "mis datos", "actualizar datos", "editar perfil"]
    if contiene_alguna(texto, palabras_perfil):
        return {
            "intencion": "perfil",
            "respuesta": (
                "👤 Para ver o editar tu perfil:\n\n"
                "1. Haz clic en el **ícono de usuario** o en **'Mi Perfil'** "
                "en la barra de navegación superior.\n"
                "2. Desde allí podrás ver tus datos personales.\n\n"
                "Si necesitas actualizar tu información (correo, documento, etc.), "
                "contacta a la Coordinación de Deportes."
            )
        }

    # --- AYUDA ---
    palabras_ayuda = ["ayuda", "help", "que puedes hacer", "funciones",
                      "como funciona", "que sabes", "opciones", "menu"]
    if contiene_alguna(texto, palabras_ayuda):
        return {
            "intencion": "ayuda",
            "respuesta": (
                "🤖 ¡Puedo ayudarte con lo siguiente!\n\n"
                "• 📋 **Inscripciones** — Cómo inscribirte en un deporte\n"
                "• 🕐 **Horarios** — Consultar horarios de entrenamientos\n"
                "• ⚽ **Deportes** — Disciplinas deportivas disponibles\n"
                "• 🏆 **Torneos** — Información sobre competencias\n"
                "• 📍 **Contacto** — Datos de la Coordinación de Deportes\n"
                "• 👤 **Perfil** — Información sobre tu cuenta\n\n"
                "Escribe tu pregunta y haré lo posible por ayudarte. 😊"
            )
        }

    # --- INTENCIÓN NO RECONOCIDA ---
    return {
        "intencion": "desconocido",
        "respuesta": (
            "🤔 Disculpa, no logré entender tu consulta. Soy un asistente en "
            "entrenamiento y aún estoy aprendiendo.\n\n"
            "Intenta preguntar sobre:\n"
            "• **Inscripciones** a deportes\n"
            "• **Horarios** de entrenamiento\n"
            "• **Deportes** disponibles\n"
            "• **Torneos** y competencias\n\n"
            "Si necesitas ayuda personalizada, contacta a la "
            "**Coordinación de Deportes** de Bienestar Universitario."
        )
    }
