<script>
    import { createEventDispatcher } from "svelte";
    const dispatch = createEventDispatcher();

    export let tiposDocumento = [];
    export let facultades = [];
    export let nivelesEducativos = [];
    export let programas = [];
    export let roles = [];
    export let usuarioAEditar = null;

    let nuevoUsuario = {
        nombre: "",
        correo: "",
        contrasena: "",
        tipo_documento_id: null,
        facultad_id: null,
        nivel_educativo_id: null,
        programa_id: null,
        rol_id: null,
        numero_documento: "",
    };

    // Si recibimos un usuario para editar, poblar el formulario
    $: if (usuarioAEditar) {
        nuevoUsuario = {
            nombre: usuarioAEditar.nombre,
            correo: usuarioAEditar.email || usuarioAEditar.correo,
            contrasena: "", // No mostramos la contraseña actual por seguridad
            tipo_documento_id: usuarioAEditar.tipo_documento_id,
            facultad_id: usuarioAEditar.facultad_id,
            nivel_educativo_id: usuarioAEditar.nivel_educativo_id,
            programa_id: usuarioAEditar.programa_id,
            rol_id: usuarioAEditar.rol_id,
            numero_documento: usuarioAEditar.numero_documento,
        };
    }

    $: programasFiltrados = programas.filter(
        (p) =>
            p.facultad_id == nuevoUsuario.facultad_id &&
            p.id_nivel_edu == nuevoUsuario.nivel_educativo_id,
    );

    // Limpiar campos dependientes al cambiar facultada o nivel
    $: if (nuevoUsuario.facultad_id) {
        // Al cambiar facultad, el programa y nivel deberían resetearse? 
        // El usuario dijo: "al seleccionar facultad me debe pedir el nivel educativo despues de eso mostrarme los programas"
    }

    async function guardarUsuario() {
        try {
            if (
                !nuevoUsuario.nombre ||
                !nuevoUsuario.correo ||
                (!usuarioAEditar && !nuevoUsuario.contrasena) || // Contraseña solo obligatoria al crear
                !nuevoUsuario.rol_id ||
                !nuevoUsuario.tipo_documento_id ||
                !nuevoUsuario.facultad_id ||
                !nuevoUsuario.numero_documento
            ) {
                alert("Por favor, complete todos los campos obligatorios.");
                return;
            }

            // Preparar data para el backend (convertir strings vacíos o nulls adecuadamente)
            const dataEnviar = {
                ...nuevoUsuario,
                tipo_documento_id: Number(nuevoUsuario.tipo_documento_id),
                facultad_id: Number(nuevoUsuario.facultad_id),
                rol_id: Number(nuevoUsuario.rol_id),
                nivel_educativo_id: nuevoUsuario.nivel_educativo_id ? Number(nuevoUsuario.nivel_educativo_id) : null,
                programa_id: nuevoUsuario.programa_id ? Number(nuevoUsuario.programa_id) : null
            };

            const url = usuarioAEditar 
                ? `http://localhost:8000/usuarios/${usuarioAEditar.id}`
                : "http://localhost:8000/usuarios/";
            
            const method = usuarioAEditar ? "PUT" : "POST";

            // Si es edición y no hay contraseña, no la enviamos
            if (usuarioAEditar && !nuevoUsuario.contrasena) {
                delete dataEnviar.contrasena;
            }

            const res = await fetch(url, {
                method: method,
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(dataEnviar),
            });

            if (res.ok) {
                alert(usuarioAEditar ? "Usuario actualizado exitosamente." : "Usuario guardado exitosamente.");
                dispatch("guardado");
                if (!usuarioAEditar) {
                    nuevoUsuario = {
                        nombre: "",
                        correo: "",
                        contrasena: "",
                        tipo_documento_id: null,
                        facultad_id: null,
                        nivel_educativo_id: null,
                        programa_id: null,
                        rol_id: null,
                        numero_documento: "",
                    };
                }
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
                    placeholder={usuarioAEditar ? "Dejar en blanco para mantener actual" : "Mínimo 8 caracteres"}
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
                    on:change={() => {
                        nuevoUsuario.nivel_educativo_id = "";
                        nuevoUsuario.programa_id = "";
                    }}
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
                    for="nivel-usuario">Nivel Educativo</label
                >
                <select
                    id="nivel-usuario"
                    class="form-select rounded-3 py-2"
                    bind:value={nuevoUsuario.nivel_educativo_id}
                    disabled={!nuevoUsuario.facultad_id}
                    on:change={() => {
                        nuevoUsuario.programa_id = "";
                    }}
                >
                    <option value="">Seleccione un nivel</option>
                    {#each nivelesEducativos as nivel}
                        <option value={nivel.id}>{nivel.nombre}</option>
                    {/each}
                </select>
            </div>
            <div class="col-md-6">
                <label
                    class="form-label fw-medium text-muted small"
                    for="programa-usuario">Programa Académico</label
                >
                <select
                    id="programa-usuario"
                    class="form-select rounded-3 py-2"
                    bind:value={nuevoUsuario.programa_id}
                    disabled={!nuevoUsuario.nivel_educativo_id}
                >
                    <option value="">Seleccione un programa</option>
                    {#each programasFiltrados as prog}
                        <option value={prog.id}>{prog.nombre}</option>
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
                <i class="bi bi-person-check me-1"></i> {usuarioAEditar ? "Actualizar Usuario" : "Guardar Usuario"}
            </button>
        </div>
    </form>
</div>
