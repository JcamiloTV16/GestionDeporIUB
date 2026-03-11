<script>
    import { createEventDispatcher } from "svelte";
    const dispatch = createEventDispatcher();

    export let tiposDocumento = [];
    export let facultades = [];
    export let roles = [];

    let nuevoUsuario = {
        nombre: "",
        correo: "",
        contrasena: "",
        tipo_documento_id: "",
        facultad_id: "",
        rol_id: "",
        numero_documento: "",
    };

    async function guardarUsuario() {
        try {
            if (
                !nuevoUsuario.nombre ||
                !nuevoUsuario.correo ||
                !nuevoUsuario.contrasena ||
                !nuevoUsuario.rol_id
            ) {
                alert("Por favor, complete los campos obligatorios.");
                return;
            }

            const res = await fetch("http://localhost:8000/usuarios/", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(nuevoUsuario),
            });

            if (res.ok) {
                alert("Usuario guardado exitosamente.");
                dispatch("guardado");
                nuevoUsuario = {
                    nombre: "",
                    correo: "",
                    contrasena: "",
                    tipo_documento_id: "",
                    facultad_id: "",
                    rol_id: "",
                    numero_documento: "",
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
        <i class="bi bi-person-plus me-2 text-primary"></i>Formulario de Nuevo
        Usuario
    </h5>
    <form on:submit|preventDefault={guardarUsuario}>
        <div class="row g-4">
            <div class="col-md-6">
                <label
                    class="form-label fw-medium text-muted small"
                    for="nombre-usuario">Nombre Completo</label
                >
                <input
                    id="nombre-usuario"
                    type="text"
                    class="form-control rounded-3 py-2"
                    placeholder="Ej: Juan Pérez"
                    bind:value={nuevoUsuario.nombre}
                />
            </div>
            <div class="col-md-6">
                <label
                    class="form-label fw-medium text-muted small"
                    for="correo-usuario">Correo Institucional</label
                >
                <input
                    id="correo-usuario"
                    type="email"
                    class="form-control rounded-3 py-2"
                    placeholder="Ej: juan@iub.edu.co"
                    bind:value={nuevoUsuario.correo}
                />
            </div>
            <div class="col-md-6">
                <label
                    class="form-label fw-medium text-muted small"
                    for="password-usuario">Contraseña</label
                >
                <input
                    id="password-usuario"
                    type="password"
                    class="form-control rounded-3 py-2"
                    placeholder="Mínimo 8 caracteres"
                    bind:value={nuevoUsuario.contrasena}
                />
            </div>
            <div class="col-md-3">
                <label
                    class="form-label fw-medium text-muted small"
                    for="tipo-doc-usuario">Tipo Documento</label
                >
                <select
                    id="tipo-doc-usuario"
                    class="form-select rounded-3 py-2"
                    bind:value={nuevoUsuario.tipo_documento_id}
                >
                    <option value="">Seleccione un tipo</option>
                    {#each tiposDocumento as tipo}
                        <option value={tipo.id}>{tipo.nombre}</option>
                    {/each}
                </select>
            </div>
            <div class="col-md-3">
                <label
                    class="form-label fw-medium text-muted small"
                    for="documento-usuario">Número Documento</label
                >
                <input
                    id="documento-usuario"
                    type="text"
                    class="form-control rounded-3 py-2"
                    placeholder="Ej: 1234567890"
                    bind:value={nuevoUsuario.numero_documento}
                />
            </div>
            <div class="col-md-6">
                <label
                    class="form-label fw-medium text-muted small"
                    for="facultad-usuario">Facultad</label
                >
                <select
                    id="facultad-usuario"
                    class="form-select rounded-3 py-2"
                    bind:value={nuevoUsuario.facultad_id}
                >
                    <option value="">Seleccione una facultad</option>
                    {#each facultades as fac}
                        <option value={fac.id}>{fac.nombre}</option>
                    {/each}
                </select>
            </div>
            <div class="col-md-6">
                <label
                    class="form-label fw-medium text-muted small"
                    for="rol-usuario">Rol Asignado</label
                >
                <select
                    id="rol-usuario"
                    class="form-select rounded-3 py-2"
                    bind:value={nuevoUsuario.rol_id}
                >
                    <option value="">Seleccione un rol</option>
                    {#each roles as rol}
                        <option value={rol.id}>{rol.nombre}</option>
                    {/each}
                </select>
            </div>
        </div>
        <div class="mt-4 pt-2 d-flex justify-content-end">
            <button
                type="submit"
                class="btn btn-primary rounded-3 px-4 py-2 fw-bold"
            >
                <i class="bi bi-person-check me-1"></i> Guardar Usuario
            </button>
        </div>
    </form>
</div>
