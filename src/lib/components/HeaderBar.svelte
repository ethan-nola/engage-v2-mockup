<script lang="ts">
    import { page } from "$app/stores";
    import { Button } from "$lib/components/ui/button";
    import * as DropdownMenu from "$lib/components/ui/dropdown-menu";
    import { cn } from "$lib/utils";

    // Map route paths to display names
    const routeNames: Record<string, string> = {
        "/": "Overview",
        "/gradebook": "Gradebook",
        "/library": "Library",
        "/accounts": "Accounts",
        "/sites": "Sites",
        "/licenses": "Licenses",
        "/users": "Users",
        "/internal-users": "Internal Users",
        "/help": "Help"
    };
</script>

<header class="bg-[#1b2655] px-6 flex items-center justify-between">
    <h1 class="text-white text-[28px] font-semibold">
        {routeNames[$page.url.pathname] || "Not Found"}
    </h1>
    
    <div class="flex items-center gap-4">
        <DropdownMenu.Root>
            <DropdownMenu.Trigger asChild let:builder>
                <Button
                    variant="ghost"
                    class={cn(
                        "gap-2 text-sm transition-colors",
                        "h-auto font-normal text-white hover:bg-white/10",
                        "[&>div>span:last-child]:!text-white"
                    )}
                    builders={[builder]}
                >
                    <div class="flex items-center gap-2">
                        <span class="h-8 w-8 rounded-full bg-white/10 flex items-center justify-center text-white">
                            KG
                        </span>
                        <span>Ken Goode</span>
                    </div>
                </Button>
            </DropdownMenu.Trigger>
            <DropdownMenu.Content 
                
                class="w-56 bg-white rounded-md shadow-lg border border-gray-200"
            >
                <DropdownMenu.Item class="cursor-pointer hover:bg-gray-100">Profile</DropdownMenu.Item>
                <DropdownMenu.Item class="cursor-pointer hover:bg-gray-100">Settings</DropdownMenu.Item>
                <DropdownMenu.Separator />
                <DropdownMenu.Item class="cursor-pointer hover:bg-gray-100">Log out</DropdownMenu.Item>
            </DropdownMenu.Content>
        </DropdownMenu.Root>
    </div>
</header> 