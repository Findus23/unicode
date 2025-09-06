import {char_array} from "./data";
import {bookdata_by_unicode, listOfData} from "./bookdata";

export function character_to_code(character: string) {
    // placeholder logic
    const char_index = char_array.indexOf(character)

    return listOfData[char_index].unicode_code


}

export function code_to_message(code: string) {
    return bookdata_by_unicode[code].full_text
}

/*

character -> code: via mph

code -> character: load list of characters and generate mapping on first run

 */
