<script lang="ts">
    import {listOfData, meta} from "./bookdata";

    const meta_list = Object.entries(meta).map(([meta_key,meta_val]) => ({ meta_key,meta_val }));
    console.log(meta_list);
</script>


<table border="1">
    {#each meta_list as {meta_key,meta_val} (meta_key)}
        <tr>
        <td>{meta_key}</td>
        <td>{meta_val}</td>
        </tr>
    {/each}

</table>

{#each listOfData as data (data.unicode_code)}
    <p>{data.unicode_code}: {data.full_text}</p>
{/each}
