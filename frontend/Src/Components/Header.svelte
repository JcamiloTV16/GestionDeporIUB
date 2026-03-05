<script>
    export let titulo = "Gestión Deportiva IUB";
    export let subtitulo = "";
    export let rolLabel = "";
    export let rolClass =
        "bg-primary-subtle text-primary border-primary-subtle";
    export let iconClass = "bi-shield-check";
</script>

<div class="d-flex justify-content-between align-items-center mb-4">
    <div>
        <h2 class="fw-bold text-dark m-0">{titulo}</h2>
        {#if subtitulo}
            <p class="text-muted small mb-0">{subtitulo}</p>
        {/if}
    </div>
    {#if rolLabel}
        <span class="badge {rolClass} border px-3 py-2 rounded-pill">
            <i class="bi {iconClass} me-1"></i>
            {rolLabel}
        </span>
    {/if}
</div>
