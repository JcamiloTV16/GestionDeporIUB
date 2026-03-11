<script>
    import { createEventDispatcher } from "svelte";
    const dispatch = createEventDispatcher();

    export let deportes = [];
    export let entrenadores = [];

    let nuevoCurso = {
        deporte_id: "",
        entrenador_id: "",
        dia_semana: "",
        hora_inicio: "",
        hora_fin: "",
        lugar: "",
        cupo: 20,
    };

    async function guardarCurso() {
        try {
            if (
                !nuevoCurso.deporte_id ||
                !nuevoCurso.entrenador_id ||
                !nuevoCurso.dia_semana ||
                !nuevoCurso.hora_inicio ||
                !nuevoCurso.hora_fin
            ) {
                alert("Por favor, complete todos los campos del curso.");
                return;
            }

            const res = await fetch("http://localhost:8000/horarios/", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(nuevoCurso),
            });

            if (res.ok) {
                alert("Curso/Horario creado exitosamente.");
                dispatch("guardado");
                nuevoCurso = {
                    deporte_id: "",
                    entrenador_id: "",
                    dia_semana: "",
                    hora_inicio: "",
                    hora_fin: "",
                    lugar: "",
                    cupo: 20,
                };
            } else {
                const err = await res.json();
                alert("Error: " + (err.detail || "No se pudo guardar"));
            }
        } catch (error) {
            alert("Error de conexión");
        }
    }
</script>

<div class="card shadow-sm border-0 rounded-4 p-4 mt-2">
    <h5 class="fw-bold mb-4">
        <i class="bi bi-plus-circle me-2 text-primary"></i>Formulario de Nuevo
        Curso
    </h5>
    <form on:submit|preventDefault={guardarCurso}>
        <div class="row g-4">
            <div class="col-md-6">
                <label
                    class="form-label fw-medium text-muted small"
                    for="disciplina-deportiva">Disciplina Deportiva</label
                >
                <select
                    id="disciplina-deportiva"
                    class="form-select rounded-3 py-2"
                    bind:value={nuevoCurso.deporte_id}
                >
                    <option value="">Seleccione un deporte</option>
                    {#each deportes as dep}
                        <option value={dep.id}>{dep.nombre}</option>
                    {/each}
                </select>
            </div>
            <div class="col-md-6">
                <label
                    class="form-label fw-medium text-muted small"
                    for="entrenador-asignado">Entrenador Asignado</label
                >
                <select
                    id="entrenador-asignado"
                    class="form-select rounded-3 py-2"
                    bind:value={nuevoCurso.entrenador_id}
                >
                    <option value="">Seleccione un entrenador</option>
                    {#each entrenadores as ent}
                        <option value={ent.id}>{ent.nombre_usuario}</option>
                    {/each}
                </select>
            </div>
            <div class="col-md-4">
                <label
                    class="form-label fw-medium text-muted small"
                    for="dias-clase">Días de Clase</label
                >
                <input
                    id="dias-clase"
                    type="text"
                    class="form-control rounded-3 py-2"
                    placeholder="Ej: Lunes - Miércoles"
                    bind:value={nuevoCurso.dia_semana}
                />
            </div>
            <div class="col-md-3">
                <label
                    class="form-label fw-medium text-muted small"
                    for="hora-inicio">Hora Inicio</label
                >
                <input
                    id="hora-inicio"
                    type="time"
                    class="form-control rounded-3 py-2"
                    bind:value={nuevoCurso.hora_inicio}
                />
            </div>
            <div class="col-md-3">
                <label
                    class="form-label fw-medium text-muted small"
                    for="hora-fin">Hora Fin</label
                >
                <input
                    id="hora-fin"
                    type="time"
                    class="form-control rounded-3 py-2"
                    bind:value={nuevoCurso.hora_fin}
                />
            </div>
            <div class="col-md-2">
                <label
                    class="form-label fw-medium text-muted small"
                    for="cupo-maximo">Cupo</label
                >
                <input
                    id="cupo-maximo"
                    type="number"
                    class="form-control rounded-3 py-2"
                    placeholder="Ej: 20"
                    min="1"
                    bind:value={nuevoCurso.cupo}
                />
            </div>
            <div class="col-md-12">
                <label
                    class="form-label fw-medium text-muted small"
                    for="lugar-curso">Lugar / Sede</label
                >
                <input
                    id="lugar-curso"
                    type="text"
                    class="form-control rounded-3 py-2"
                    placeholder="Ej: Cancha Principal"
                    bind:value={nuevoCurso.lugar}
                />
            </div>
        </div>
        <div class="mt-4 pt-2 d-flex justify-content-end">
            <button
                type="submit"
                class="btn btn-primary rounded-3 px-4 py-2 fw-bold"
            >
                <i class="bi bi-save me-1"></i> Guardar Curso
            </button>
        </div>
    </form>
</div>
