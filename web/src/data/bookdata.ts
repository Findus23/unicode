import total_data from "../assets/total_data.json"

type DataSet = Record<string, Data>


export const meta = total_data.meta

export const data_raw: Record<string, string> = total_data.data

export const bookdata_by_unicode: DataSet = {}
export const bookdata_by_full_text: DataSet = {}


export const listOfData: Data[] = []

let i = 0
for (const unicode_code in data_raw) {
    if (Object.prototype.hasOwnProperty.call(data_raw, unicode_code)) {
        const full_text = data_raw[unicode_code]
        const obj: Data = {
            unicode_code: unicode_code,
            full_text: full_text,
            id: i
        }
        bookdata_by_unicode[unicode_code] = obj
        bookdata_by_full_text[full_text] = obj
        listOfData.push(obj)
        i++
    }
}
export const num_entries = i

