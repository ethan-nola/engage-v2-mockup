# Engage Learning Management System - Version 2 Mockup

Everything you need to build the next iteration of our "Engage" Learning Management System, powered by SvelteKit [`sv`](https://github.com/sveltejs/cli).

## Project Overview

The Engage Learning Management System aims to enhance the educational experience by providing a comprehensive platform for instructors and students. This project serves as a mockup for the upcoming features and functionalities that will be integrated into the system.

## Creating a Project

If you're seeing this, you've probably already done this step. Congrats!

```bash
# create a new project in the current directory
npx sv create

# create a new project in my-app
npx sv create my-app
```

## Developing

Once you've created a project and installed dependencies with `npm install` (or `pnpm install` or `yarn`), start a development server:

```bash
npm run dev

# or start the server and open the app in a new browser tab
npm run dev -- --open
```

## Building

To create a production version of your app:

```bash
npm run build
```

You can preview the production build with `npm run preview`.

> To deploy your app, you may need to install an [adapter](https://svelte.dev/docs/kit/adapters) for your target environment.

## Mock Data

This project includes mock data to simulate the functionality of the Engage Learning Management System. The mock data schema includes:

- **Districts**
  - Schools
    - School title
    - School address
    - School Administrators
    - Instructors
    - Students
    - Courses
    - Classrooms

## Next Steps

1. **Set Up the Development Environment**
   - Clone repositories, install dependencies, and configure environment variables.
2. **Database Initialization**
   - Execute the SQL script in Supabase.
   - Seed the database with sample data for development purposes.
3. **Backend Development**
   - Set up API endpoints.
   - Implement data models and business logic.
4. **Frontend Development**
   - Build out the Engage UI component.
   - Integrate AG Grid and configure data binding.
5. **Integration Testing**
   - Test the end-to-end functionality of the Engage system.
   - Ensure data consistency and UI responsiveness.
6. **Deployment Preparation**
   - Configure CI/CD pipelines if applicable.
   - Prepare for deployment to staging and production environments.

---
pushing to multiple repositories:

```bash
git push origin main  # Push to Azure DevOps
git push github main  # Push to GitHub
```
