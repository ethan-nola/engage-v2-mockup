<script lang="ts">
  import { cn } from "$lib/utils";
  let className: string | undefined = undefined;
  export { className as class };
</script>

<a href="/">
  <img
    src="/images/sa-logo.svg"
    alt="Engage Logo"
    class={cn("object-contain", className)}
  />
</a> 