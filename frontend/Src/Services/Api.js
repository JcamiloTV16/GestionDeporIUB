export const API = "http://localhost:8000"

export async function obtenerDeportes() {
  const res = await fetch(`${API}/deportes/`)
  return await res.json()
}

export async function agregarDeporte(deporte) {
  const res = await fetch(`${API}/deportes/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(deporte)
  })
  return await res.json()
}

export async function eliminarDeporte(id) {
  const res = await fetch(`${API}/deportes/${id}`, {
    method: "DELETE"
  })
  return await res.json()
}

export async function actualizarDeporte(id, deporte) {
  const res = await fetch(`${API}/deportes/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(deporte)
  })
  return await res.json()
}

export async function login(email, password) {
  const res = await fetch(`${API}/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ correo: email, contrasena: password })
  })

  if (!res.ok) {
    const error = await res.json()
    throw new Error(error.detail || "Error al iniciar sesión")
  }

  return await res.json()
}

export async function obtenerUsuarios(token) {
  const res = await fetch(`${API}/usuarios/`, {
    headers: {
      "Authorization": `Bearer ${token}`
    }
  })
  return await res.json()
}

export async function actualizarUsuario(id, usuario, token) {
  const res = await fetch(`${API}/usuarios/${id}`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${token}`
    },
    body: JSON.stringify(usuario)
  })
  return await res.json()
}

export async function eliminarUsuario(id, token) {
  const res = await fetch(`${API}/usuarios/${id}`, {
    method: "DELETE",
    headers: {
      "Authorization": `Bearer ${token}`
    }
  })
  return await res.json()
}

export async function obtenerHorarios(token) {
  const res = await fetch(`${API}/horarios/`, {
    headers: {
      "Authorization": `Bearer ${token}`
    }
  })
  return await res.json()
}

export async function obtenerInscritosPorHorario(horarioId, token) {
  const res = await fetch(`${API}/inscripciones/horario/${horarioId}`, {
    headers: {
      "Authorization": `Bearer ${token}`
    }
  })
  return await res.json()
}

export async function obtenerAuditorias(token) {
  const res = await fetch(`${API}/auditoria/`, {
    headers: {
      "Authorization": `Bearer ${token}`
    }
  })
  return await res.json()
}
