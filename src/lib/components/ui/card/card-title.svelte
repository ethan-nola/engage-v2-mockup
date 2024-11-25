<script lang="ts">
	import { cn } from "$lib/utils";
	import type { HTMLAttributes } from "svelte/elements";

	type $$Props = HTMLAttributes<HTMLHeadingElement>;

	let className: $$Props["class"] = undefined;
	export { className as class };
</script>

<h3
	class={cn("text-lg font-semibold leading-none tracking-tight text-star-blue", className)}
	{...$$restProps}
>
	<slot />
</h3>
