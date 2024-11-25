<script lang="ts">
  import "../app.css";
  import { Button } from "$lib/components/ui/button";
  import * as DropdownMenu from "$lib/components/ui/dropdown-menu";
  import { cn } from "$lib/utils";
  import { page } from "$app/stores";
  import Logo from "$lib/components/Logo.svelte";
  import HeaderBar from "$lib/components/HeaderBar.svelte";
  import Icon from "$lib/components/Icon.svelte";
</script>

<svelte:head>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link
    rel="preconnect"
    href="https://fonts.gstatic.com"
    crossorigin="anonymous"
  />
  <link
    href="https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap"
    rel="stylesheet"
  />
</svelte:head>

<div class="grid h-screen grid-cols-[14rem_1fr] grid-rows-[5rem_1fr]">
  <aside class="bg-background row-span-2">
    <div class="h-20">
      <div class="px-7 h-full flex items-center">
        <Logo class="h-9" />
      </div>
    </div>

    <nav class="space-y-2 p-4 overflow-y-auto">
      <a
        href="/"
        class={cn(
          "flex items-center gap-4 rounded-lg px-4 py-3",
          $page.url.pathname === "/"
            ? "bg-secondary text-nav-text"
            : "hover:bg-secondary/80 text-nav-muted",
          "text-base font-bold leading-6"
        )}
      >
        <Icon name="dashboard" size="md" />
        <span>Overview</span>
      </a>

      <a
        href="/gradebook"
        class={cn(
          "flex items-center gap-4 rounded-lg px-4 py-3",
          $page.url.pathname === "/gradebook"
            ? "bg-secondary text-nav-text"
            : "hover:bg-secondary/80 text-nav-muted",
          "text-base font-bold leading-6"
        )}
      >
        <Icon name="insert_chart" size="md" />
        <span>Gradebook</span>
      </a>



      <a
        href="/library"
        class={cn(
          "flex items-center gap-4 rounded-lg px-4 py-3",
          $page.url.pathname === "/library"
            ? "bg-secondary text-nav-text"
            : "hover:bg-secondary/80 text-nav-muted",
          "text-base font-bold leading-6"
        )}
      >
        <Icon name="library_books" size="md" />
        <span>Library</span>
      </a>

      <a
        href="/accounts"
        class={cn(
          "flex items-center gap-4 rounded-lg px-4 py-3",
          $page.url.pathname === "/accounts"
            ? "bg-secondary text-nav-text"
            : "hover:bg-secondary/80 text-nav-muted",
          "text-base font-bold leading-6"
        )}
      >
        <Icon name="location_city" size="md" />
        <span>Accounts</span>
      </a>

      <a
        href="/sites"
        class={cn(
          "flex items-center gap-4 rounded-lg px-4 py-3",
          $page.url.pathname === "/sites"
            ? "bg-secondary text-nav-text"
            : "hover:bg-secondary/80 text-nav-muted",
          "text-base font-bold leading-6"
        )}
      >
        <Icon name="widgets" size="md" />
        <span>Sites</span>
      </a>

      <a
        href="/licenses"
        class={cn(
          "flex items-center gap-4 rounded-lg px-4 py-3",
          $page.url.pathname === "/licenses"
            ? "bg-secondary text-nav-text"
            : "hover:bg-secondary/80 text-nav-muted",
          "text-base font-bold leading-6"
        )}
      >
        <Icon name="verified_user" size="md" />
        <span>Licenses</span>
      </a>

      <a
        href="/users"
        class={cn(
          "flex items-center gap-4 rounded-lg px-4 py-3",
          $page.url.pathname === "/users"
            ? "bg-secondary text-nav-text"
            : "hover:bg-secondary/80 text-nav-muted",
          "text-base font-bold leading-6"
        )}
      >
        <Icon name="group" size="md" />
        <span>Users</span>
      </a>

      <a
        href="/internal-users"
        class={cn(
          "flex items-center gap-4 rounded-lg px-4 py-3",
          $page.url.pathname === "/internal-users"
            ? "bg-secondary text-nav-text"
            : "hover:bg-secondary/80 text-nav-muted",
          "text-base font-bold leading-6"
        )}
      >
        <Icon name="work" size="md" />
        <span>Internal Users</span>
      </a>

      <a
        href="/help"
        class={cn(
          "flex items-center gap-4 rounded-lg px-4 py-3",
          $page.url.pathname === "/help"
            ? "bg-secondary text-nav-text"
            : "hover:bg-secondary/80 text-nav-muted",
          "text-base font-bold leading-6"
        )}
      >
        <Icon name="help" size="md" />
        <span>Help</span>
      </a>
    </nav>
  </aside>

  <HeaderBar />

  <main class="bg-secondary/80 overflow-y-auto p-6">
    <slot />
  </main>
</div>

<style>
  .ag-watermark {
    display: none !important; /* Optionally hide it if it somehow gets added */
  }
</style>

