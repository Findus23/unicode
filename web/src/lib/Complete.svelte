<script lang="ts">
    import {data_by_full_text, listOfData} from "./data";
    import MiniSearch from "minisearch";

    const values = listOfData;

    const miniSearch = new MiniSearch({
        fields: ['full_text'],
        storeFields: ['unicode_code', 'full_text'] // fields to return with search results
    })
    window.search = miniSearch;
    miniSearch.addAll(listOfData)

    /* FILTERING countres DATA BASED ON INPUT */
    let searchresults: SearchResult[] = [];
    // $: console.log(filteredCountries)

    const filterCountries = () => {
        let storageArr: SearchResult[] = [];
        if (inputValue) {
            if (false) {
                values.forEach(country => {
                    if (country.full_text.toLowerCase().includes(inputValue.toLowerCase())) {
                        storageArr.push({
                            text: makeMatchBold(country.full_text),
                            data: country
                        });
                    }
                });
            } else {
                const results = miniSearch.search(inputValue, {
                    prefix: true,
                    fuzzy:0.2
                }).slice(0, 30);
                console.info(results);
                storageArr = results.map((a) => {
                    return {
                        data: data_by_full_text[a.full_text],
                        text: a.full_text
                    }
                })
                console.log(storageArr);
            }

        }
        searchresults = storageArr;
    }


    /* HANDLING THE INPUT */
    let searchInput; // use with bind:this to focus element
    let inputValue = "";

    $: if (!inputValue) {
        searchresults = [];
        hiLiteIndex = null;
    }

    const clearInput = () => {
        inputValue = "";
        searchInput.focus();
    }

    const setInputVal = (result: SearchResult) => {
        inputValue = result.data.full_text;
        searchresults = [];
        hiLiteIndex = null;
        document.querySelector('#country-input').focus();
    }

    const submitValue = () => {
        if (inputValue) {
            console.log(`${inputValue} is submitted!`);
            setTimeout(clearInput, 1000);
        } else {
            alert("You didn't type anything.")
        }
    }

    const makeMatchBold = (str: string) => {
        // replace part of (country name === inputValue) with strong tags
        let matched = str.substring(0, inputValue.length);
        let makeBold = `<strong>${matched}</strong>`;
        let boldedMatch = str.replace(matched, makeBold);
        return boldedMatch;
    }
    /* NAVIGATING OVER THE LIST OF COUNTRIES W HIGHLIGHTING */
    let hiLiteIndex = null;
    //$: console.log(hiLiteIndex);
    $: hiLitedCountry = searchresults[hiLiteIndex];

    const navigateList = (e) => {
        if (e.key === "ArrowDown" && hiLiteIndex <= searchresults.length - 1) {
            hiLiteIndex === null ? hiLiteIndex = 0 : hiLiteIndex += 1
        } else if (e.key === "ArrowUp" && hiLiteIndex !== null) {
            hiLiteIndex === 0 ? hiLiteIndex = searchresults.length - 1 : hiLiteIndex -= 1
        } else if (e.key === "Enter") {
            setInputVal(searchresults[hiLiteIndex]);
        } else {
            return;
        }
    }
</script>


<svelte:window on:keydown={navigateList}/>

<form autocomplete="off" on:submit|preventDefault={submitValue}>
    <div class="autocomplete">
        <input id="country-input"
               type="text"
               placeholder="Search Country Names"
               bind:this={searchInput}
               bind:value={inputValue}
               on:input={filterCountries}>
    </div>

    <input type="submit">

    <!-- FILTERED LIST OF COUNTRIES -->
    {#if searchresults.length > 0}
        <ul id="autocomplete-items-list">
            {#each searchresults as result, i}
                <li class="autocomplete-items" class:autocomplete-active={i === hiLiteIndex}
                    on:click={() => setInputVal(result)}>{@html result.text}</li>
            {/each}
        </ul>
    {/if}
</form>


<style>
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

    input[type=submit] {
        background-color: DodgerBlue;
        color: #fff;
    }

    #autocomplete-items-list {
        position: relative;
        margin: 0;
        padding: 0;
        top: 0;
        width: 297px;
        border: 1px solid #ddd;
        background-color: #ddd;
    }
</style>
