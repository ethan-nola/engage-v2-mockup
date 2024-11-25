<script lang="ts">
  import {
    Card,
    CardContent,
    CardHeader,
    CardTitle,
  } from "$lib/components/ui/card";
  import * as Table from "$lib/components/ui/table";
  import Icon from "$lib/components/Icon.svelte";

  const stats = [
    { title: "Users", value: "6419", icon: "group" as const },
    { title: "Sites", value: "80", icon: "widgets" as const },
    { title: "Library Assets", value: "403", icon: "library_books" as const },
    { title: "Licenses", value: "139", icon: "verified_user" as const },
    { title: "Accounts", value: "68", icon: "location_city" as const },
  ];

  const users = [
    { name: "Aphril Clemente", role: "Teacher Admin", signUpDate: "11/19/2024", status: "Active" },
    { name: "Connor Ray", role: "Student", signUpDate: "11/20/2024", status: "Active" },
    { name: "Kyndra Penkowski", role: "Student", signUpDate: "11/20/2024", status: "Active" },
    { name: "Londyn Roberts", role: "Student", signUpDate: "11/20/2024", status: "Active" },
    { name: "Makenzie Walker", role: "Student", signUpDate: "", status: "Active" },
    { name: "Mayco Aguilar", role: "Student", signUpDate: "", status: "Active" },
    { name: "Norman Snerling", role: "Teacher", signUpDate: "", status: "Active" },
    { name: "Vernon Burton", role: "Student", signUpDate: "11/19/2024", status: "Active" },
  ];
</script>


  <!-- Stats Cards Grid -->
  <div class="grid gap-4 md:grid-cols-5">
    {#each stats as stat}
      <Card>
        <CardHeader class="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle>{stat.title}</CardTitle>
          <Icon name={stat.icon} size="lg" className="text-star-red" />
        </CardHeader>
        <CardContent>
          <div class="text-2xl font-bold">{stat.value}</div>
        </CardContent>
      </Card>
    {/each}
  </div>

  <!-- Table and Stats Layout Container -->
  <div class="flex gap-6 mt-6">
    <!-- Users Table -->
    <Card class="flex-3 flex-grow">
      <CardHeader>
        <CardTitle>New Users</CardTitle>
      </CardHeader>
      <CardContent class="flex-grow">
        <Table.Root class="h-full">
          <Table.Header>
            <Table.Row>
              <Table.Head class="w-[50px]"></Table.Head>
              <Table.Head>Name</Table.Head>
              <Table.Head>Role</Table.Head>
              <Table.Head>Sign Up Date</Table.Head>
              <Table.Head>Status</Table.Head>
            </Table.Row>
          </Table.Header>
          <Table.Body class="h-full">
            {#each users as user}
              <Table.Row>
                <Table.Cell>
                  <Icon name="person" size="md" className="text-star-blue" />
                </Table.Cell>
                <Table.Cell>{user.name}</Table.Cell>
                <Table.Cell>{user.role}</Table.Cell>
                <Table.Cell>{user.signUpDate}</Table.Cell>
                <Table.Cell>
                  <span class="inline-flex items-center rounded-full px-2 py-1 text-xs font-medium bg-green-100 text-green-700">
                    {user.status}
                  </span>
                </Table.Cell>
              </Table.Row>
            {/each}
          </Table.Body>
        </Table.Root>
      </CardContent>
    </Card>

    <!-- Stats Card -->
    <Card class="flex-1 flex-grow flex flex-col">
      <CardHeader>
        <CardTitle>Stats</CardTitle>
      </CardHeader>
      <CardContent class="flex-grow flex items-center justify-center">
        <div class="text-center">
          <img src="/images/no-data.svg" alt="No data" class="w-64 mx-auto opacity-10" />
          <p class="text-sm text-muted-foreground mt-4">No data yet to show stats</p>
        </div>
      </CardContent>
    </Card>
  </div>

