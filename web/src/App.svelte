<script lang="ts">
  import Counter from './lib/Counter.svelte'
  import DebugDisplay from './lib/DebugDisplay.svelte'
  import Complete from "./lib/Complete.svelte";

</script>

<main>
  <div>
    <a href="https://vite.dev" target="_blank" rel="noreferrer">
<!--      <img src={viteLogo} class="logo" alt="Vite Logo" />-->
    </a>
    <a href="https://svelte.dev" target="_blank" rel="noreferrer">
<!--      <img src={svelteLogo} class="logo svelte" alt="Svelte Logo" />-->
    </a>
  </div>
  <h1>Vite + Svelte</h1>

  <Complete></Complete>

<!--  <div class="card">-->
<!--    <Counter />-->
<!--  </div>-->
  <div class="card">
      <details>
          <summary>Debug</summary>
          <DebugDisplay />
      </details>
  </div>

</main>

<style>
  .logo {
    height: 6em;
    padding: 1.5em;
    will-change: filter;
    transition: filter 300ms;
  }
  .logo:hover {
    filter: drop-shadow(0 0 2em #646cffaa);
  }
  .logo.svelte:hover {
    filter: drop-shadow(0 0 2em #ff3e00aa);
  }
  .read-the-docs {
    color: #888;
  }
</style>
