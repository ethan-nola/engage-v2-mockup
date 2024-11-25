<script lang="ts">
  export let title: string;
</script>

<div class="p-8">
  <h1 class="text-2xl font-semibold mb-6">{title}</h1>
  <slot />
</div> 