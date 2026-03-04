<script>
    import { rol, user } from "../Store.js";

    let usuarioActual;
    user.subscribe((value) => (usuarioActual = value));

    function cerrarSesion() {
        rol.set("");
        user.set(null);
    }
</script>

<nav
    class="navbar navbar-expand-lg navbar-dark bg-primary shadow-sm sticky-top"
>
    <div class="container-fluid divider-x">
        <a class="navbar-brand fw-bold" href="/">
            <i class="bi bi-trophy-fill me-2"></i> GestionDeporIUB
        </a>

        <button
            class="navbar-toggler"
            type="button"
            data-bs-toggle="collapse"
            data-bs-target="#navbarContent"
        >
            <span class="navbar-toggler-icon"></span>
        </button>

        <div class="collapse navbar-collapse" id="navbarContent">
            <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                <!-- Enlaces dinámicos según el rol podrían ir aquí -->
            </ul>

            {#if usuarioActual}
                <div class="d-flex align-items-center text-white">
                    <div class="user-info me-3 text-end d-none d-md-block">
                        <div class="fw-bold lh-1">{usuarioActual.nombre}</div>
                        <small class="text-white-50 text-capitalize"
                            >{usuarioActual.rol}</small
                        >
                    </div>
                    <div class="dropdown">
                        <button
                            class="btn btn-light rounded-circle p-2 shadow-sm"
                            type="button"
                            data-bs-toggle="dropdown"
                        >
                            <i class="bi bi-person-circle fs-5"></i>
                        </button>
                        <ul
                            class="dropdown-menu dropdown-menu-end shadow border-0 mt-2 animate__animated animate__fadeIn"
                        >
                            <li>
                                <a class="dropdown-item" href="#/perfil"
                                    ><i class="bi bi-person me-2"></i> Mi Perfil</a
                                >
                            </li>
                            <li><hr class="dropdown-divider" /></li>
                            <li>
                                <button
                                    class="dropdown-item text-danger"
                                    on:click={cerrarSesion}
                                >
                                    <i class="bi bi-box-arrow-right me-2"></i> Cerrar
                                    Sesión
                                </button>
                            </li>
                        </ul>
                    </div>
                </div>
            {/if}
        </div>
    </div>
</nav>

<style>
    .navbar {
        padding: 0.75rem 1rem;
    }
    .navbar-brand {
        font-size: 1.4rem;
        letter-spacing: -0.5px;
    }
    .user-info small {
        font-size: 0.75rem;
    }
    .dropdown-menu {
        border-radius: 12px;
    }
    .dropdown-item {
        padding: 0.6rem 1.2rem;
        font-size: 0.9rem;
    }
    .dropdown-item:hover {
        background-color: #f8f9fa;
    }
</style>
