////////////////////////////
// --- Initialisation --- //
////////////////////////////

const rootEndPoint = "/parabible";
//const rootEndPoint = "";
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

var langFormatValue = null;
var addedVerses = [];
var addedTranslations = [];

var bookAbbriviations = null;
loadBookAbbrivs();

function logRegular(prefx, msg) {
    console.log(`[${prefx}] ${msg}`);
}
function logRequest(url) {
    logRegular('Request', url);
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
    
    getJson(`/api/get/translation_meta?format=${langFormatValue}&lang=${lang}`)
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

/////////////////////////////////////////
// --- Text field content handling --- //
/////////////////////////////////////////

function formVerseLabel(obj) {
    var bookAbbriv = bookAbbriviations[obj["book_id"]];
    return `${bookAbbriv} ${obj["chapter_id"]}:${obj["verse_id"]}`;
}

function formTranslationLabel(obj) {
    let maxLength = 25;
    return `${obj["label"].length > maxLength ? obj["label"].slice(0, maxLength - 3) + "..." : obj["label"]}`;
}

function updateRequestTextBox() {
    var versesString = "";
    var translationsString = "";
    var delimeter = ":";
    for (var i = 0; i < addedVerses.length; i++) {
        bookAbbriv = bookAbbriviations[addedVerses[i]["book_id"]];
        versesString += `"${bookAbbriv}"${delimeter}${addedVerses[i]["chapter_id"]}${delimeter}${addedVerses[i]["verse_id"]} `;
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
        let label = formVerseLabel(addedVerses[i]);
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
