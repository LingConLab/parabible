////////////////////////////
// --- Initialisation --- //
////////////////////////////

//const rootEndPoint = "/parabible";
const rootEndPoint = "";
const host = window.location.protocol + "//" + window.location.host + rootEndPoint;

const bookSelect = document.querySelector('#book_select');
const chapterSelect = document.querySelector('#chapter_select');
const verseSelect = document.querySelector('#verse_select');
const verseTagBox = document.querySelector('#verse_tag_box');

const langFormatSelect = document.querySelector('#lang_format_select');
const langSelect = document.querySelector('#lang_select');
const translationSelect = document.querySelector('#translation_select');
const translationTagBox = document.querySelector('#verse_translations_box');

const addVerseButton = document.querySelector('#add_verse_btn');
const addTranslationButton = document.querySelector('#add_translation_btn');

const requestTextBox = document.querySelector('#request_text_box');
const tableContainer = document.querySelector('#result_table_container');

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
function resetTableCellElements() {
    tableCellElements ={
        "col_heads": [],
        "row_heads": [],
        "cells": []
    };
}

///////////////////////////////////
// --- Select boxes managing --- //
///////////////////////////////////

// general select boxes funcs
function addOption(parent, label, value, disable_option=false, preselect_option=false) {
    node = document.createElement("option");
    node.value = value;
    textNode = document.createTextNode(label);
    if (disable_option) node.setAttribute('disabled', '');
    if (preselect_option) node.setAttribute('selected', '');
    node.appendChild(textNode);
    parent.appendChild(node);
}

function wipeAllChildren(parent) {
    while (parent.hasChildNodes()) {
        parent.removeChild(parent.lastChild);
    }
}

function wipeOptions(parent, disable_menu=false) {
    wipeAllChildren(parent);
    addOption(parent, " -- select an option -- ", "", true, true);
    if (disable_menu) parent.setAttribute('disabled', 'disabled');
}

function selectLoadingState(parent) {
    wipeAllChildren(parent);
    addOption(parent, " -- Loading ... -- ", "");
}

function errorSelect(parent) {
    wipeAllChildren(parent);
    addOption(parent, " -- Error. See console logs. -- ", "");
}
// listeners
bookSelect.addEventListener('change', () => {
    updateChapterSelect(bookSelect.value);
    wipeOptions(verseSelect, disable=true);
    addVerseButton.setAttribute('disabled', 'disabled');
});
chapterSelect.addEventListener('change', () => {
    updateVerseSelect(bookSelect.value, chapterSelect.value);   
});

langFormatSelect.addEventListener('change', () => {
    updateLangSelect(langFormatSelect.value);
    wipeOptions(translationSelect, disable=true);
});
langSelect.addEventListener('change', () => {
    updateTranslationSelect(langSelect.value);
    addTranslationButton.setAttribute('disabled', 'disabled');
});
translationSelect.addEventListener('change', () => {
    addTranslationButton.removeAttribute('disabled');
});

///////////////////////////////////////
// --------    API calls    -------- //
///////////////////////////////////////

function getJson(endpoint) {
    const url = host + endpoint;
    logRequest(url);
    return fetch(url)
    .then((response) => {
        if (!response.ok) {
            throw new Error(`HTTP error: ${response.status}`);
        }
        return response.json();
    })
    .then((data) => {
        return data;
    })
    .catch((error) => {
        console.log(`Could not fetch data: ${error}`);
        return null;
    });
}

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
        console.log(`Could not fetch langs: ${error}`);
        errorSelect(verseSelect);
    });

    verseSelect.removeAttribute('disabled');
    addVerseButton.removeAttribute('disabled');
}

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
        console.log(`Could not fetch langs: ${error}`);
        errorSelect(chapterSelect);
    });

    chapterSelect.removeAttribute('disabled');
}

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
        console.log(`Could not fetch langs: ${error}`);
        errorSelect(langSelect);
    });

    translationSelect.removeAttribute('disabled');
}

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
        console.log(`Could not fetch langs: ${error}`);
        errorSelect(langSelect);
    });

    langSelect.removeAttribute('disabled');
}

function loadBookAbbrivs() {
    getJson(`/api/get/book_title_abbrs`)
    .then((json) => {
        bookAbbriviations = json;
    })
    .catch((error) => {
        console.log(`Could not fetch langs: ${error}`);
        bookAbbriviations = null;
    });
}

function getVerseLine(book_id, chapter, verse, translation_id) {
    return getJson(`/api/get/verse?book_id=${book_id}&chapter=${chapter}&verse=${verse}&translation_id=${translation_id}`)
    .then((json) => {
        return json;
    })
    .catch((error) => {
        console.log(`Could not fetch langs: ${error}`);
    });
}

function getTranslationMeta(translation_id) {
    return getJson(`/api/get/translation_meta?id=${translation_id}`)
    .then((json) => {
        return json;
    })
    .catch((error) => {
        console.log(`Could not fetch langs: ${error}`);
    });
}

/////////////////////////////////////////
// --- Text field content handling --- //
/////////////////////////////////////////

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

function formVerseLabelFromObj(obj) {
    return formVerseLabel(obj['book_id'], obj['chapter_id'], obj['verse_id']);
}

function formVerseLabel(book_id, chapter, verse) {
    var bookAbbriv = bookAbbriviations[book_id];
    return `${bookAbbriv} ${chapter}:${verse}`;
}

function formTranslationLabel(obj) {
    let maxLength = 25;
    return `${obj["label"].length > maxLength ? obj["label"].slice(0, maxLength - 3) + "..." : obj["label"]}`;
}

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

function updateTranslationTags() {
    wipeAllChildren(translationTagBox);
    for (var i = 0; i < addedTranslations.length; i++) {
        let label = formTranslationLabel(addedTranslations[i]);
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

function createTag(label, deleteCallback) {
    // // verse tag template
    // <div class="d-inline bg-light border p-1 mx-1 rounded">
    //    <p class="d-inline fw-light">LABEL</p>
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
        "book": bookId,
        "chapter": chapterId,
        "verse": verseId
    }
}

function parseTranslation(translationString) {
    return {
        "label": "Translation Label",
        "id": translationString.replace(/[^0-9]+/, "")
    }
}

function parseRawRequest() {
    let textToParse = requestTextBox.value;
    let splitted = textToParse.split(/\n-+\n/);

    let rawVerses = splitted[0].split(" ")
    let rawTranslations = splitted[1].split(" ");

    let parsedVerses = rawVerses.map(parseVerse);
    let parsedTranslations = rawTranslations.map(parseTranslation);

    return {
        "verses": parsedVerses,
        "translations": parsedTranslations
    }
}

/////////////////////////////////
// --- Request processing  --- //
/////////////////////////////////

function processRawRequest() {
    let parsedData = parseRawRequest();
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
            getVerseLine(verseData[v]["book"], verseData[v]["chapter"], verseData[v]["verse"], translationData[t]["id"])
            .then((json) => {
                tableCellElements['cells'][v][t].textContent = json["verse"] ? json["verse"] : 'No data';
            })
        }
    }
}

/////////////////////////////////
// --- Main table forming  --- //
/////////////////////////////////

function createDataTableCell(content='Empty cell') {
    let cell = document.createElement('td');
    cell.textContent = content;
    return cell;
}

function createDataTableHeadCell(scope, content='Empty head cell') {
    let cell = document.createElement('th');
    cell.classList.add('table-success');
    if (scope != null) cell.setAttribute('scope', scope);
    cell.textContent = content;
    return cell;
}

function createDataTable(rowAmount, colAmount) {
    /*
        Results of this function executed:
            0. `tableContainer`'s children deleted, `tableCellElements` list viped
            1. Table element is formed.
            2. Table Element is added to `tableContainer` div
            3. All cell Elements are added to `tableCellElements['cells']`
                - List is 2 dimentional (list of lists) tableCellElements[x][y]
                    - `x` axis stands for row, `y` - for column
                    - in other words `x` stands for verse, `y` - for translation
                - Each cell may be modified through this list
    */
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
    tableHead.appendChild(createDataTableHeadCell(null, 'Verse'));
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
