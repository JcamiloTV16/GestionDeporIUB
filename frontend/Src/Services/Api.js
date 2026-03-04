const API = "http://localhost:3000"

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