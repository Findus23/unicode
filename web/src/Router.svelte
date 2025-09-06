<script lang="ts">
    import {onMount} from "svelte"

    import Home from "./pages/Home.svelte"
    import About from "./pages/About.svelte"
    import AllCharacters from "./pages/AllCharacters.svelte"
    import Dynamic from "./pages/Dynamic.svelte"
    import NotFound from "./pages/NotFound.svelte"

    type ComponentType = Home | About | AllCharacters | Dynamic | NotFound

    let Component: ComponentType = $state(Home)
    let params: Record<string, string> = $state({})

    function normalize(path?: string): string {
        if (!path) return "/"
        return (path.replace(/\/+$/, "") || "/")
    }

    function updateRoute(): void {
        const path = normalize(window.location.pathname)
        console.log(path)
        if (path === "/" || path === "") {
            Component = Home
            params = {}
            return
        }

        if (path === "/about") {
            Component = About
            params = {}
            return
        }
        if (path === "/all") {
            Component = AllCharacters
            params = {}
            return
        }

        const segments = path.split("/").filter(Boolean)
        if (segments.length === 1) {
            Component = Dynamic
            params = {character: decodeURIComponent(segments[0])}

            return
        }

        Component = NotFound

        params = {}
    }

    // programmatic navigation helper
    export function navigate(to: string): void {
        const dest = normalize(to)
        if (dest === window.location.pathname) return

        history.pushState({}, "", dest)
        updateRoute()
    }

    onMount(() => {
        updateRoute()
        const onPop = (): void => updateRoute()
        window.addEventListener("popstate", onPop)
        window.addEventListener("app:navigate", onPop)
        return () => {
            window.removeEventListener("popstate", onPop)
            window.removeEventListener("app:navigate", onPop)
        }
    })
</script>

<nav style="display:flex;gap:1rem;margin-bottom:1rem;">
    <a href="/" on:click|preventDefault={() => navigate("/")}>Home</a>
    <a href="/about" on:click|preventDefault={() => navigate("/about")}>About</a>
    <a href="/all" on:click|preventDefault={() => navigate("/all")}>All</a>
    <a href="/A" on:click|preventDefault={() => navigate("/A")}>A</a>
    <a href="/B" on:click|preventDefault={() => navigate("/B")}>B</a>
</nav>

{#if Component}
    <Component {...params}/>
{:else}
    <div>Loading...</div>
{/if}
