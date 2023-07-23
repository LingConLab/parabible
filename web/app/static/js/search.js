////////////////////////////
// --- Initialisation --- //
////////////////////////////

const rootEndPoint = "/nginx_root/parabible";
//const rootEndPoint = "";
const host = window.location.protocol + "//" + window.location.host + rootEndPoint;
// Verse selection containers
const bookSelect = document.querySelector('#book_select');
const chapterSelect = document.querySelector('#chapter_select');
const verseSelect = document.querySelector('#verse_select');
const verseTagBox = document.querySelector('#verse_tag_box');
// Translation selection containers
const langFormatSelect = document.querySelector('#lang_format_select');
const langSelect = document.querySelector('#lang_select');
const translationSelect = document.querySelector('#translation_select');
const translationTagBox = document.querySelector('#verse_translations_box');
// Add buttons
const addVerseButton = document.querySelector('#add_verse_btn');
const addTranslationButton = document.querySelector('#add_translation_btn');
// Raw request text box
const requestTextBox = document.querySelector('#request_text_box');
// Table container
const tableContainer = document.querySelector('#result_table_container');
// Error containers 
const globalErrorBox = document.querySelector('#global_error_box');
const verseErrorBox = document.querySelector('#verse_error_box');
const translationErrorBox = document.querySelector('#translation_error_box');
const rawReqestErrorBox = document.querySelector('#raw_request_error_box');

let langFormatValue = null;
let addedVerses = [];
let addedTranslations = [];

let bookAbbriviations = null;
loadBookAbbrivs();

let tableCellElements = null;

function logRegular(prefx, msg) {
    console.log(`[${prefx}] ${msg}`);
}
function logRequest(url) {
    logRegular('Request', url);
}
/**
 * This func just resets `tableCellElements`. No args no returns.
 */
function resetTableCellElements() {
    tableCellElements ={
        "col_heads": [],
        "row_heads": [],
        "cells": []
    };
}
/**
 * Sets desired message and style to specific error box. Available error boxes are stored in global variables that end with "ErrorBox". For an example, `globalErrorBox`.
 * @param {Object} box HTML object (div) that represents error box to be modified and shown.
 * @param {String} message Text that will be displayed in error box.
 * @param {String} type It only affects the color of error box. Possible types are 'info' (blue), 'warn' (orange), 'error' (red).
 */
function displayInfoBox(box, message, type='info') {
    let classes = {
        'info': 'alert-info',
        'warn': 'alert-warning',
        'error': 'alert-danger'
    };

    for (let key in classes)
        box.classList.remove(classes[key]);
    box.classList.add(classes[type]);
    
    box.textContent = message;
    box.classList.remove('d-none');
}
/**
 * Hides desired error box element (adds 'd-none' bootstrap class, which sets 'display' to none). Available error boxes are stored in global variables that end with "ErrorBox". For an example, `globalErrorBox`.
 * @param {Object} box HTML object (div) that represents error box to be hidden.
 */
function hideErrorBox(box) {
    box.classList.add('d-none');
}
///////////////////////////////////
// --- Select boxes managing --- //
///////////////////////////////////

// general select boxes funcs
/**
 * Adds an option to select html element. Available select elements are stored in global variables that end with "Select". For an example, `bookSelect`.
 * @param {Object} parent HTML object (select) that represents select element.
 * @param {String} label Label that user will see (text node value).
 * @param {String} value Value of select option.
 * @param {Boolean} disable_option If this option must be disabled (non clickable). Default is false.
 * @param {Boolean} preselect_option if this option must be preselected. Default is false.
 */
function addOption(parent, label, value, disable_option=false, preselect_option=false) {
    node = document.createElement("option");
    node.value = value;
    textNode = document.createTextNode(label);
    if (disable_option) node.setAttribute('disabled', '');
    if (preselect_option) node.setAttribute('selected', '');
    node.appendChild(textNode);
    parent.appendChild(node);
}
/**
 * Helper func that removes all children of a given element.
 * @param {Object} parent HTML object (any).
 */
function wipeAllChildren(parent) {
    while (parent.hasChildNodes()) {
        parent.removeChild(parent.lastChild);
    }
}
/**
 * Removes all option elements from select element.
 * @param {Object} parent HTML object (select). It's children will be removed!
 * @param {Boolean} disable_menu If select menu must be disabled (non clickable).
 */
function wipeOptions(parent, disable_menu=false) {
    wipeAllChildren(parent);
    addOption(parent, " -- select an option -- ", "", true, true);
    if (disable_menu) parent.setAttribute('disabled', 'disabled');
}
/**
 * Sets visual state of select menu to loading. Removes all options and adds a temp option with loading text.
 * @param {Object} parent HTML object (select).
 */
function selectLoadingState(parent) {
    wipeAllChildren(parent);
    addOption(parent, " -- Loading ... -- ", "", disable_option=true, preselect_option=true);
}
/**
 * Sets visual state of select menu to error. Removes all options and adds a temp option with error text.
 * @param {Object} parent HTML object (select).
 */
function errorSelect(parent) {
    wipeAllChildren(parent);
    addOption(parent, " -- Error -- ", "");
}
// listeners
/**
 * New book selected ->
 * -> load it's chapters from api and populate chapter select with chapter options -> 
 * -> clear and reset verse select (since it's 'parent' (previous select menu) is changed) ->
 * -> disable addVerse button
 */
bookSelect.addEventListener('change', () => {
    updateChapterSelect(bookSelect.value);
    wipeOptions(verseSelect, disable=true);
    addVerseButton.setAttribute('disabled', 'disabled');
});
/**
 * New chapter selected ->
 * -> load it's verses from api and populate verse select with verse options ->
 * -> (skipped) nothing to clear (since it has no following select menus) ->
 * -> disable addVerse button
 */
chapterSelect.addEventListener('change', () => {
    updateVerseSelect(bookSelect.value, chapterSelect.value);   
    addVerseButton.setAttribute('disabled', 'disabled');
});
/**
 * New verse selected ->
 * -> enable addVerse button
 */
verseSelect.addEventListener('change', () => {
    addVerseButton.removeAttribute('disabled');
});

/**
 * New format selected ->
 * -> load langs in selected format from api and populate lang select with it -> 
 * -> wipe options of translations select (since its select that follows lang select that just changed) ->
 * -> disable addTranslation button
 */
langFormatSelect.addEventListener('change', () => {
    updateLangSelect(langFormatSelect.value);
    wipeOptions(translationSelect, disable=true);
    addTranslationButton.setAttribute('disabled', 'disabled');
});
/**
 * New lang selected ->
 * -> load translations from api and populate translations select with it ->
 * -> disable addTranslation button
 */
langSelect.addEventListener('change', () => {
    updateTranslationSelect(langSelect.value);
    addTranslationButton.setAttribute('disabled', 'disabled');
});
/**
 * New translation selected ->
 * -> enable addTranslation button
 */
translationSelect.addEventListener('change', () => {
    addTranslationButton.removeAttribute('disabled');
});

/**
 * 
 */
requestTextBox.addEventListener('input', () => {
    parseRawRequest();
})

///////////////////////////////////////
// --------    API calls    -------- //
///////////////////////////////////////
/**
 * Calls an API and returns JSON promise.
 * 
 * It DOES NOT catch exceptions! Exceptions are being caught outside of this function so they can
 * be handled individually depending on outer context.
 * @param {String} endpoint Endpoint and args. Example "/api/get/something?arg1=val1&arg2=val2"
 * @returns {Promise} JSON 
 */
function getJson(endpoint) {
    const url = host + endpoint;
    logRequest(url);
    return fetch(url)
    .then((response) => {
        if (!response.ok)
            return response.text().then(text => { 
                let notFoundHint = `Make sure that the site is hosted on "${host}"
                and most importantly that site's root endpoint is "${rootEndPoint}".
                If root endpoint is different, set the correct root to \`rootEndPoint\` variable in search.js`;
                notFoundHint = `[ !!! 404 HINT !!! ] ${notFoundHint}`;
                if (response.status != 404) notFoundHint = "";
                throw new Error(`Request url: ${url}\nHTTP error:\n${text}${notFoundHint}`); 
            })
        return response.json();
    });
}
/**
 * Gets ids of chapters by book id from api, populates chapter select with chapter id options.
 * @param {any} book_id id of a book. Integer or string
 */
function updateChapterSelect(book_id) {
    selectLoadingState(chapterSelect);

    getJson(`/api/get/chapter_ids?book_id=${book_id}`)
    .then((json) => {
        wipeOptions(chapterSelect);
        for (let i = 0; i < json['chapters'].length; i++) {
            addOption(chapterSelect, json['chapters'][i], json['chapters'][i]);
        }
    })
    .catch((error) => {
        displayInfoBox(verseErrorBox, `Could not fetch chapters: ${error}`, 'error');
        errorSelect(chapterSelect);
    });

    chapterSelect.removeAttribute('disabled');
}
/**
 * Gets ids of verses by book id and chapter id from api, populates verse select with verse id options.
 * @param {any} book_id id of a book. Integer or string
 * @param {any} chapter_id id of a chapter. Integer or string
 */
function updateVerseSelect(book_id, chapter_id) {
    selectLoadingState(verseSelect);

    getJson(`/api/get/verse_ids?book_id=${book_id}&chapter_id=${chapter_id}`)
    .then((json) => {
        wipeOptions(verseSelect);
        for (let i = 0; i < json['verses'].length; i++) {
            addOption(verseSelect, json['verses'][i], json['verses'][i]);
        }
    })
    .catch((error) => {
        displayInfoBox(verseErrorBox, `Could not fetch verses: ${error}`, 'error');
        errorSelect(verseSelect);
    });

    verseSelect.removeAttribute('disabled');
}
/**
 * Gets translations by lang format and by lang from api, populates translation select with translation options.
 * 
 * Example: format = 'closest_iso_639_3', lang = 'eng'.
 * Available formats are listed in API backend docstrings.
 * @param {String} lang Language name in current format. Format is taken from global variable `langFormatValue`
 * that is set during `updateLangSelect()`
 */
function updateTranslationSelect(lang) {
    selectLoadingState(translationSelect);
    
    getJson(`/api/get/translations_by_lang?format=${langFormatValue}&lang=${lang}`)
    .then((json) => {
        wipeOptions(translationSelect);
        for (let i = 0; i < json['translations_list'].length; i++) {
            t_id = json['translations_list'][i][0];
            t_iso = json['translations_list'][i][1];
            t_name = (json['translations_list'][i][2] ? json['translations_list'][i][2] : "no title");
            t_year = json['translations_list'][i][3];
            t_string = `[${t_iso} | ${t_year}] ${t_name}`;
            addOption(translationSelect, t_string, t_id);
        }
    })
    .catch((error) => {
        displayInfoBox(translationErrorBox, `Could not fetch translations: ${error}`, 'error');
        errorSelect(langSelect);
    });

    translationSelect.removeAttribute('disabled');
}
/**
 * Gets langs by lang format from api, populates language select with language options.
 * 
 * Api returns lang already in requested format. 
 * @param {String} langFormat Name of the format
 */
function updateLangSelect(langFormat) {
    selectLoadingState(langSelect);
    
    getJson(`/api/get/langs?format=${langFormat}`)
    .then((json) => {
        langFormatValue = json['val_format'];
        wipeOptions(langSelect);
        for (let i = 0; i < json['lang_list'].length; i++) {
            addOption(langSelect, json['lang_list'][i]['label'], json['lang_list'][i]['val']);
        }
    })
    .catch((error) => {
        displayInfoBox(translationErrorBox, `Could not fetch langs: ${error}`, 'error');
        errorSelect(langSelect);
    });

    langSelect.removeAttribute('disabled');
}
/**
 * Gets book abbriviations from api. Puts it in `bookAbbriviations` object. 
 * 
 * Object contains key: value where key is book's id and value is abbriviation.
 */
function loadBookAbbrivs() {
    getJson(`/api/get/book_title_abbrs`)
    .then((json) => {
        bookAbbriviations = json;
    })
    .catch((error) => {
        displayInfoBox(globalErrorBox, `Could not fetch book abbriviations: ${error}`, 'error');
        bookAbbriviations = null;
    });
}
/**
 * Gets verse line by book id, chapter number, verse number and by translation from api.
 * @param {*} book_id Book id. Integer or string
 * @param {*} chapter Chapter number. Integer or string
 * @param {*} verse Verse number. Integer or string
 * @param {*} translation_id Translation id. Integer or string
 * @returns JSON promise or null. Verse line is contained in json["verse"].
 * Returns null on exception, json["verse"] is null if requested verse is missing in requested translation.
 */
function getVerseLine(book_id, chapter, verse, translation_id) {
    return getJson(`/api/get/verse?book_id=${book_id}&chapter=${chapter}&verse=${verse}&translation_id=${translation_id}`)
    .then((json) => {
        return json;
    })
    .catch((error) => {
        displayInfoBox(globalErrorBox, `Could not fetch verse line: ${error}`, 'error');
        return null;
    });
}
/**
 * Gets translation meta by translation id from api. 
 * @param {*} translation_id Translation id. Integer or string
 * @returns JSON promise. For returned JSON structure see docstrings of API's backend.
 */
function getTranslationMeta(translation_id) {
    return getJson(`/api/get/translation_meta?id=${translation_id}`)
    .then((json) => {
        return json;
    })
    .catch((error) => {
        displayInfoBox(globalErrorBox, `Could not fetch translation meta: ${error}`, 'error');
    });
}

/////////////////////////////////////////
// --- Text field content handling --- //
/////////////////////////////////////////
/**
 * Forms translation label to display to user. Example: "[eng 2000] Translation name here"
 * @param {*} metaObj Object with meta. They come from `getTranslationMeta()`
 * @returns {String} formed label
 */
function formTranslationLabelFromMeta(metaObj) {
    let title = "No title";
    if (metaObj['vernacular_title'])
        title = metaObj['vernacular_title'];
    else if (metaObj['english_title'])
        title = metaObj['english_title'];

    let iso_639 = metaObj['closest_iso_639_3'];
    let year = metaObj['year_short'];

    return `[${iso_639} ${year}] ${title}`;
}
/**
 * Same as `formVerseLabel()` but takes verse object.
 * Just handy func since we store verses in such objects form.
 * @param {*} obj Object with 'book_id', 'chapter_id' and 'verse_id' keys.
 * @returns {String} A label
 */
function formVerseLabelFromObj(obj) {
    return formVerseLabel(obj['book_id'], obj['chapter_id'], obj['verse_id']);
}
/**
 * Form verse label to display to user. Example: "John 7:4"
 * @param {*} book_id Id of the book. It is used to get book name abbriviation.
 * @param {*} chapter Chapter number
 * @param {*} verse Verse number
 * @returns {String} A label
 */
function formVerseLabel(book_id, chapter, verse) {
    var bookAbbriv = bookAbbriviations[book_id];
    return `${bookAbbriv} ${chapter}:${verse}`;
}
/**
 * Shorten label if it exceeds lenght of `maxLength` and add "..." to the end to indicate that it was cut.
 * 
 * Note: After the cut the lenght of the label will be exactly `maxLength`. It cuts 3 more characters before
 * appending "..." suffix.
 * 
 * Example: '[abc 1234] Very long name of a very long translation that will take too much space' -> '[abc 1234] Very long n...'
 * @param {String} label Label 
 * @param {Integer} maxLength Max length. Default is 25
 * @returns {String} Shortened label if it's lenght is greater than `maxLength`, unedited label otherwise
 */
function shortenTranslationLabel(label, maxLength = 25) {
    return `${label.length > maxLength ? label.slice(0, maxLength - 3) + "..." : label}`;
}
/**
 * Updates text box's content. Takes data from global `addedVerses` and `addedTranslations`
 */
function updateRequestTextBox() {
    let versesString = "";
    let translationsString = "";
    let delimeter = ":";
    for (var i = 0; i < addedVerses.length; i++) {
        bookAbbriv = bookAbbriviations[addedVerses[i]["book_id"]];
        bookAbbriv = bookAbbriv.replace(/ /g, "_");
        versesString += `${bookAbbriv}${delimeter}${addedVerses[i]["chapter_id"]}${delimeter}${addedVerses[i]["verse_id"]} `;
    }
    for (var i = 0; i < addedTranslations.length; i++) {
        translationsString += `${addedTranslations[i]["id"]} `;
    }
    versesString = versesString.trim();
    translationsString = translationsString.trim();

    var result = `${versesString}\n---\n${translationsString}`;
    requestTextBox.value = result;
    logRegular('updateRequestTextBox', result);
}
/**
 * Callback of addVerse button. Takes data from verse select elements,
 * adds new verse to global `addedVerses` list,
 * updates verse tags and reqest text box.
 * 
 * Ignores dublicates. Nothing happens if element to be added already exists in `addedVerses`.
 */
function addVerse() {
    var objToAdd = {
        "book_id": book_select[book_select.selectedIndex].value,
        "chapter_id": chapter_select[chapter_select.selectedIndex].value,
        "verse_id": verse_select[verse_select.selectedIndex].value
    };
    // going through all the items to check the dubs
    for (var i = 0; i < addedVerses.length; i++) {
        if (JSON.stringify(addedVerses[i]) === JSON.stringify(objToAdd)) {
            logRegular('addVerse', 'Dublicate met');
            return;
        }
    }

    // add to global list and refresh raw request and tags
    addedVerses.push(objToAdd);
    updateVerseTags();
    updateRequestTextBox();
}
/**
 * Callback of addTranslation button. Takes data from translation select elements,
 * adds new translation to global `addedTranslations` list,
 * updates translation tags and reqest text box.
 * 
 * Ignores dublicates. Nothing happens if element to be added already exists in `addedTranslations`.
 */
function addTranslation() {
    var objToAdd = {
        "id": translationSelect[translationSelect.selectedIndex].value,
        "label": translationSelect[translationSelect.selectedIndex].text
    };
    // going through all the items to check the dubs
    for (var i = 0; i < addedTranslations.length; i++)
        if (JSON.stringify(addedTranslations[i]) === JSON.stringify(objToAdd)) {
            // we met a dublicate => skip it
            logRegular('addTranslation', 'Dublicate met');
            return;
        }

    // add to global list and refresh raw request and tags
    addedTranslations.push(objToAdd);
    updateTranslationTags();
    updateRequestTextBox();
}

///////////////////////////
// --- Tags handling --- //
///////////////////////////
/**
 * Updates verse tags up to date with `addedVerses`.
 * Removes all tags and creates new ones from `addedVerses`.
 * 
 * All tags have callback on deletion. 
 * Callbacks depend on verse indexes in `addedVerses` list.
 * So unfortunately call this function every time you alter `addedVerses` list. 
 * Otherwise indexes in callbacks will be out of date and tag deletion will not work.
 */
function updateVerseTags() {
    wipeAllChildren(verseTagBox);
    for (var i = 0; i < addedVerses.length; i++) {
        let label = formVerseLabelFromObj(addedVerses[i]);
        let index = i; // bc we dont want to create a link to `i`
        let deleteCallback = () => {
            addedVerses.splice(index, 1);
            updateVerseTags();
            updateRequestTextBox();
        };
        let tag = createTag(label, deleteCallback);

        verseTagBox.appendChild(tag);
    }
}
/**
 * Updates translation tags up to date with `addedTranslations`.
 * Removes all tags and creates new ones from `addedTranslations`.
 * 
 * All tags have callback on deletion. 
 * Callbacks depend on translation indexes in `addedTranslations` list.
 * So unfortunately call this function every time you alter `addedTranslations` list. 
 * Otherwise indexes in callbacks will be out of date and tag deletion will not work.
 */
function updateTranslationTags() {
    wipeAllChildren(translationTagBox);
    for (var i = 0; i < addedTranslations.length; i++) {
        let label = shortenTranslationLabel(addedTranslations[i]["label"]);
        let index = i; // bc we dont want to create a link to `i`
        let deleteCallback = () => {
            addedTranslations.splice(index, 1);
            updateTranslationTags();
            updateRequestTextBox();
        };
        let tag = createTag(label, deleteCallback);

        translationTagBox.appendChild(tag);
    }
}
/**
 * Constructs tag HTML div element.
 * 
 * @param {String} label Tag's label (text displayed on tag)
 * @param {Function} deleteCallback Tag's callback on deletion. Will be linked to div's delete button's click.
 * @returns {Object} HTML div object.
 */
function createTag(label, deleteCallback) {
    // div structure
    // <div class="d-inline bg-light border p-1 mx-1 rounded">
    //    <p class="d-inline fw-light text-wrap">LABEL</p>
    //    <button class="d-inline btn btn-sm btn-outline-danger py-0 px-1">✕</button>
    // </div>
    var tagDiv = document.createElement('div');
    var paragraph = document.createElement('p');
    var button = document.createElement('button');

    tagDiv.classList.add('d-inline', 'bg-light', 'border', 'p-1', 'mx-1', 'rounded');
    paragraph.classList.add('d-inline', 'fw-light', 'text-wrap');
    button.classList.add('d-inline', 'btn', 'btn-sm', 'btn-outline-danger', 'py-0', 'px-1', 'mx-1');

    button.addEventListener('click', deleteCallback);

    paragraph.innerText = label;
    button.innerText = '✕';

    tagDiv.appendChild(paragraph);
    tagDiv.appendChild(button);

    return tagDiv;
}

/////////////////////////////////
// --- Parsing raw request --- //
/////////////////////////////////
/**
 * Parses verse string (that used in raw text box).
 * 
 * @param {String} verseString verse string
 * @returns Object with parsed data.
 * 
 * Example:
 * "Gen.:4:15" ->
 * `{
 *      book: "1",
        chapter: "4",
        label: "Gen. 4:15",
        verse: "15"
 * }`
 */
function parseVerse(verseString) {
    let verseData = verseString.split(":");
    verseData[0] = verseData[0].replace(/_/g, ' ');

    let bookAbbr = verseData[0];
    let chapterId = verseData[1];
    let verseId = verseData[2];

    let bookId = -1;
    for (let id in bookAbbriviations) {
        if (bookAbbr === bookAbbriviations[id]) {
            bookId = id;
            break;
        }
    }

    return {
        "label": formVerseLabel(bookId, chapterId, verseId),
        "book_id": bookId,
        "chapter": chapterId,
        "verse": verseId
    }
}
/**
 * Parses translation string (that used in raw text box).
 * Basically extracts id.
 * 
 * @param {*} translationString translation string
 * @returns Object with parsed data
 */
function parseTranslation(translationString) {
    return {
        "label": "Translation Label",
        "id": translationString.replace(/[^0-9]+/, "")
    }
}
/**
 * Parses text that from `requestTextBox`. Parses verses and translations from it.
 * @returns Two lists with parsed translations and verses objects.
 */
function parseRawRequest() {
    let textToParse = requestTextBox.value;
    let splitted = textToParse.split(/\n-+\n/);

    if (splitted.length < 2) {
        displayInfoBox(rawReqestErrorBox, 'Add at least one verse and one translation first.', 'warn');
        return;
    }

    let rawVerses = splitted[0].split(" ");
    if (rawVerses.length <= 1 && rawVerses[0] == "") {
        displayInfoBox(rawReqestErrorBox, 'Add at least one verse.', 'warn');
        return;
    }
    let rawTranslations = splitted[1].split(" ");
    console.log(rawTranslations);
    if (rawTranslations.length <= 1 && rawTranslations[0] == "") {
        displayInfoBox(rawReqestErrorBox, 'Add at least one translation.', 'warn');
        return;
    }

    let parsedVerses = rawVerses.map(parseVerse);
    let parsedTranslations = rawTranslations.map(parseTranslation);

    hideErrorBox(rawReqestErrorBox);

    return {
        "verses": parsedVerses,
        "translations": parsedTranslations
    }
}

/////////////////////////////////
// --- Request processing  --- //
/////////////////////////////////
/**
 * Forms verse/translation table from text request in `requestTextBox`.
 * 
 * Parses text from `requestTextBox`
 * -> initialisates HTML table element
 * -> fills table with verses using backend api
 */
function processRawRequest() {
    let parsedData = parseRawRequest();
    if (!parsedData) return;
    let verseData = parsedData["verses"];
    let translationData = parsedData["translations"];
    createDataTable(verseData.length, translationData.length);

    for (let v = 0; v < verseData.length; v++) 
        tableCellElements['row_heads'][v].textContent = verseData[v]['label'];

    for (let t = 0; t < translationData.length; t++) {
        tableCellElements["col_heads"][t].textContent = 'Loading...';
        getTranslationMeta(translationData[t]["id"])
        .then((json) => {
            let label = formTranslationLabelFromMeta(json);
            tableCellElements["col_heads"][t].textContent = label;
        })
        for (let v = 0; v < verseData.length; v++) {
            tableCellElements['cells'][v][t].textContent = 'Loading...';
            getVerseLine(verseData[v]["book_id"], verseData[v]["chapter"], verseData[v]["verse"], translationData[t]["id"])
            .then((json) => {
                let data = 'default';

                if (!json) data = 'Error.';
                else if (!json["verse"]) data = 'This verse is missing in this translation.';
                else data = json["verse"];

                tableCellElements['cells'][v][t].textContent = data;
            })
        }
    }
}

/////////////////////////////////
// --- Main table forming  --- //
/////////////////////////////////
/**
 * Creates HTML table cell (td) with desired text content.
 * 
 * @param {String} content 
 * @returns HTML cell element (td)
 */
function createDataTableCell(content='Empty cell') {
    let cell = document.createElement('td');
    cell.textContent = content;
    return cell;
}
/**
 * Creates HTML table header cell (th) with desired text content and scope.
 * 
 * @param {String} scope Scope of the header. Possible values are: 'row' or 'col'.
 * See HTML documentation about scope.
 * @param {String} content Default is "Empty head cell"
 * @returns HTML header cell element (th)
 */
function createDataTableHeadCell(scope, content='Empty head cell') {
    let cell = document.createElement('th');
    cell.classList.add('table-success');
    if (scope === 'row') cell.classList.add('text-nowrap');
    if (scope != null) cell.setAttribute('scope', scope);
    cell.textContent = content;
    return cell;
}
/**
 * Creates HTML table element and places it in document body.
 * 
 * Deletes children of `tableContainer`, clears `tableCellElements` lists.
 * 
 * Forms table HTML element and adds it to `tableContainer` div.
 * 
 * Fills `tableCellElements['cells']` with table cells (td).
 * Resulting list is 2D `tableCellElements['cells'][x][y]`,
 * x for rows (verses) and y for columns (translations).
 * 
 * Then each cell in the table can be accessed via this list.
 * 
 * In the same manner forms `tableCellElements['col_heads']` and `tableCellElements['row_heads']`
 * with collumn and row header cells (td).
 * 
 * @param {*} rowAmount 
 * @param {*} colAmount 
 */
function createDataTable(rowAmount, colAmount) {
    wipeAllChildren(tableContainer);
    resetTableCellElements();

    let table = document.createElement('table');
    let tableHead = document.createElement('thead');
    let tableBody = document.createElement('tbody');
    table.appendChild(tableHead);
    table.appendChild(tableBody);
    tableContainer.appendChild(table);

    table.classList.add('table', 'table-bordered');

    // collumn of verses
    tableHead.appendChild(createDataTableHeadCell(null, ''));
    // headers of collumns
    for (let i = 0; i < colAmount; i++) {
        let cellHead = createDataTableHeadCell('col', `${i}`);
        tableCellElements['col_heads'].push(cellHead);
        tableHead.appendChild(cellHead);
    }

    for (let i = 0; i < rowAmount; i++) {
        let rowCellElementList = [];
        let row = document.createElement('tr');
        let rowHead = createDataTableHeadCell('row', `${i}'s head`);
        tableCellElements['row_heads'].push(rowHead);
        row.appendChild(rowHead);
        for (let j = 0; j < colAmount; j++) {
            cell = createDataTableCell(`${i} ${j}`);
            rowCellElementList.push(cell);
            row.appendChild(cell);
        }
        tableCellElements['cells'].push(rowCellElementList);
        tableBody.appendChild(row);
    }
}
