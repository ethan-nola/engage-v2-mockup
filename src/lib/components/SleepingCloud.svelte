<script>
  export let size = 100;
  export let color = '#1e293b';
</script>

<svg width={size} height={size} viewBox="0 0 100 100" style="color: {color}">
  <path
    d="M25 45 C25 35, 35 25, 50 25 C65 25, 75 35, 75 45 C85 45, 90 55, 85 65 C80 75, 70 75, 65 75 C60 75, 40 75, 35 75 C25 75, 15 70, 15 60 C15 50, 20 45, 25 45"
    fill="currentColor"
  />
  <text x="65" y="35" font-size="14" fill="currentColor" transform="rotate(15, 65, 35)">Z</text>
  <text x="75" y="30" font-size="10" fill="currentColor" transform="rotate(15, 75, 30)">Z</text>
  <text x="83" y="25" font-size="8" fill="currentColor" transform="rotate(15, 83, 25)">Z</text>
  <path d="M40 45 C42 45, 44 45, 46 45" stroke="currentColor" stroke-width="2" fill="none"/>
  <path d="M54 45 C56 45, 58 45, 60 45" stroke="currentColor" stroke-width="2" fill="none"/>
</svg> 