<script lang="ts">
    import {character_to_code, code_to_message} from "../data/mapping";

    export let character: string = '';

    // let code = character_to_code(slug)
    $: code = character_to_code(character);
    $: message = code_to_message(code);


</script>

<h1>Dynamic ({character})</h1>

<p>Code: {code}</p>
<p>Message: {message}</p>


