import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

export default defineConfig({
	plugins: [
		sveltekit({
			hot: {
				preserveLocalState: true,
				noDispose: true,
			}
		})
	],
	assetsInclude: ['**/*.svg'],
});
