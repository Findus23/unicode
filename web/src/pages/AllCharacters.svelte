<script lang="ts">
    import {char_array} from "../data/data";
    import {navigate} from "../router";

    console.log(char_array)
</script>

<h1>All Characters</h1>

{#each char_array as char (char)}
    <div class="character">
        <a href={"/"+char} on:click|preventDefault={() => navigate('/'+char)}>


            {char}
        </a>
    </div>
{/each}


<style>
    .character {
        font-family: Inter, system-ui, Avenir, Helvetica, Arial, sans-serif;
    }


</style>
