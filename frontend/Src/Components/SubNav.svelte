<script>
    import { createEventDispatcher } from "svelte";
    const dispatch = createEventDispatcher();

    export let vistaActiva = "";
    export let opciones = [];

    function seleccionar(id) {
        dispatch("cambio", id);
    }
</script>

<div
    class="sub-nav-container d-flex gap-2 shadow-sm p-2 bg-white rounded-3 mb-4"
>
    {#each opciones as item}
        <button
            class="btn {vistaActiva === item.id
                ? 'btn-primary'
                : 'btn-outline-primary'}"
            on:click={() => seleccionar(item.id)}
        >
            {#if item.icono}
                <i class="{item.icono} me-2"></i>
            {/if}
            {item.texto}
        </button>
    {/each}
</div>

<style>
    .sub-nav-container {
        width: fit-content;
        border: 1px solid #eee;
    }
    .btn {
        border-radius: 8px;
        font-weight: 500;
        transition: all 0.2s;
        font-size: 0.9rem;
    }
</style>
