<script lang="ts">
    import {bookdata_by_full_text, listOfData} from "../data/bookdata";
    import MiniSearch from "minisearch";
    import {code_to_character} from "../data/mapping";
    import {navigate} from "../router";


    const miniSearch = new MiniSearch({
        fields: ["full_text"],
        storeFields: ["unicode_code", "full_text"]
    })
    miniSearch.addAll(listOfData)

    let searchresults: SearchResult[] = []

    const filterCountries = () => {
        let storageArr: SearchResult[] = []
        if (inputValue) {
            const results = miniSearch.search(inputValue, {
                prefix: true,
                fuzzy: 0.2
            }).slice(0, 30)
            console.info(results)
            storageArr = results.map((a) => {
                const data: Data = bookdata_by_full_text[a.full_text]
                const character = code_to_character(data.unicode_code)
                return {
                    data: bookdata_by_full_text[a.full_text],
                    text: a.full_text,
                    character: character
                }
            })
        }
        searchresults = storageArr
    }


    /* HANDLING THE INPUT */
    let searchInput
    let inputValue = "when"
    filterCountries()

    $: if (!inputValue) {
        searchresults = []
    }



</script>


<form autocomplete="off" on:submit|preventDefault={submitValue}>
    <div class="autocomplete">
        <input id="country-input"
               type="text"
               placeholder="Your message"
               bind:this={searchInput}
               bind:value={inputValue}
               on:input={filterCountries}>
    </div>

    <!--    <input type="submit">-->

    {#if searchresults.length > 0}
        <p>Select a message below</p>
        <div id="results">
            {#each searchresults as result, i (result.text)}
                <a class="box" href={"/"+result.character}
                   on:click|preventDefault={() => navigate("/"+result.character)}>
                    {result.text}</a>
            {/each}
        </div>
    {/if}
</form>


<style lang="scss">
  #results {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;

    .box {
      display: block;
      border: 1px solid lightgray;
      background: #e6e6e6;
      padding: 1em;
      margin: 1em;
      color: black;
      border-radius: 1rem;
      transition: all .2s;

      &:hover {
        //background-color: lightgray;
        box-shadow: lightgray 5px 5px 5px;
      }

      &:focus, &:active {
        //background-color: lightgray;
        box-shadow: lightgray 15px 15px 15px;
      }
    }
  }

  div.autocomplete {
    /*the container must be positioned relative:*/
    position: relative;
    display: inline-block;
    width: 300px;
  }

  input {
    border: 1px solid transparent;
    background-color: #f1f1f1;
    padding: 10px;
    font-size: 16px;
    margin: 0;
  }

  input[type=text] {
    background-color: #f1f1f1;
    width: 100%;
  }

</style>
