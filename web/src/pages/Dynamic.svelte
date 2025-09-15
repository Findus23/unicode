<script lang="ts">
    import {character_to_code, code_to_message} from "../data/mapping"

    export let character: string = ""

    // let code = character_to_code(slug)
    $: code = character_to_code(character)
    $: message = code_to_message(code)


</script>

<h2 id="single_character">{character}</h2>

<div class="message">{message}</div>
<p>Code: {code}</p>

<style lang="scss">

  #single_character {
    font-size: 15rem;
    font-family: Inter, system-ui, Avenir, Helvetica, Arial, sans-serif;
    margin: 0
  }

  .message {
    display: block;
    border: 1px solid lightgray;
    background: #e6e6e6;
    padding: 1em;
    margin: 1em;
    color: black;
    border-radius: 1rem;
    transition: all .2s;
  }
</style>

