<script lang="ts">
  import { icons, type IconName } from './icons';
  
  export let name: IconName;
  export let className = '';
  export let size: 'sm' | 'md' | 'lg' | 'xl' = 'md';

  const sizeMap = {
    sm: '16px',
    md: '24px',
    lg: '32px',
    xl: '48px'
  };
</script>

{@html `<svg 
  class="${className}" 
  viewBox="0 0 48 48" 
  fill="currentColor"
  preserveAspectRatio="xMidYMid meet"
  width="${sizeMap[size]}"
  height="${sizeMap[size]}"
>${icons[name]}</svg>`}

<style>
  :global(svg) {
    display: inline-block;
    vertical-align: middle;
  }
</style> 