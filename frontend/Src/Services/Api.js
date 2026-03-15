export const API = "http://localhost:8000"

export async function obtenerDeportes() {
  const res = await fetch(`${API}/deportes`)
  return await res.json()
}

export async function agregarDeporte(deporte) {
  await fetch(`${API}/deportes`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(deporte)
  })
}

export async function eliminarDeporte(id) {
  await fetch(`${API}/deportes/${id}`, {
    method: "DELETE"
  })
}

export async function actualizarDeporte(id, deporte) {
  await fetch(`${API}/deportes/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(deporte)
  })
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

export async function obtenerHorarios(token) {
  const res = await fetch(`${API}/horarios/`, {
    headers: {
      "Authorization": `Bearer ${token}`
    }
  })
  return await res.json()
}