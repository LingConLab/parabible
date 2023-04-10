////////////////////////////
// --- Initialisation --- //
////////////////////////////

const rootEndPoint = "/parabible";
//const rootEndPoint = "";
const host = window.location.protocol + "//" + window.location.host + rootEndPoint;

const bookSelect = document.querySelector('#book_select');
const chapterSelect = document.querySelector('#chapter_select');
const verseSelect = document.querySelector('#verse_select');

const langFormatSelect = document.querySelector('#lang_format_select');
const langSelect = document.querySelector('#lang_select');
const translationSelect = document.querySelector('#translation_select');

const requestTextBox = document.querySelector('#request_text_box')

var langFormatValue = null;
var addedVerses = [];
var addedTranslations = [];

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

function wipeAllOptions(parent) {
    while (parent.hasChildNodes()) {
        parent.removeChild(parent.lastChild);
    }
}

function wipeOptions(parent, disable_menu=false) {
    wipeAllOptions(parent);
    addOption(parent, " -- select an option -- ", "", true, true);
    if (disable_menu) parent.setAttribute('disabled', 'disabled');
}

function selectLoadingState(parent) {
    wipeAllOptions(parent);
    addOption(parent, " -- Loading ... -- ", "");
}

function errorSelect(parent) {
    wipeAllOptions(parent);
    addOption(parent, " -- Error. See console logs. -- ", "");
}
// listeners
bookSelect.addEventListener('change', () => {
    updateChapterSelect(bookSelect.value);
    wipeOptions(verseSelect, disable=true);
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
});

///////////////////////////////////
// --------    API calls    -------- //
///////////////////////////////////

function updateVerseSelect(book_id, chapter_id) {
    const url = host + `/api/get/verses?book_id=${book_id}&chapter_id=${chapter_id}`;
    selectLoadingState(verseSelect);
    logRequest(url);
    fetch(url)
    .then((response) => {
        if (!response.ok) {
            throw new Error(`HTTP error: ${response.status}`);
        }
        return response.json();
    })
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
}

function updateChapterSelect(book_id) {
    const url = host + `/api/get/chapters?book_id=${book_id}`;
    selectLoadingState(chapterSelect);
    logRequest(url);
    fetch(url)
    .then((response) => {
        if (!response.ok) {
            throw new Error(`HTTP error: ${response.status}`);
        }
        return response.json();
    })
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
    const url = host + `/api/get/translations?format=${langFormatValue}&lang=${lang}`;
    selectLoadingState(translationSelect);
    logRequest(url);
    fetch(url)
    .then((response) => {
        if (!response.ok) {
            throw new Error(`HTTP error: ${response.status}`);
        }
        return response.json();
    })
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
    const url = host + `/api/get/langs?format=${langFormat}`;
    selectLoadingState(langSelect);
    logRequest(url);
    fetch(url)
    .then((response) => {
        if (!response.ok) {
            throw new Error(`HTTP error: ${response.status}`);
        }
        return response.json();
    })
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

/////////////////////////////////////////
// --- Text field content handling --- //
/////////////////////////////////////////

function updateRequestTextBox() {
    var versesString = "";
    var translationsString = "";
    for (var i = 0; i < addedVerses.length; i++) {
        versesString += `${addedVerses[i]["book_id"]}.${addedVerses[i]["chapter_id"]}.${addedVerses[i]["verse_id"]} `;
    }
    for (var i = 0; i < addedTranslations.length; i++) {
        translationsString += `${addedTranslations[i]["id"]} `;
    }
    versesString = versesString.trim();
    translationsString = translationsString.trim();

    var result = `${versesString}\n---\n${translationsString}`;
    requestTextBox.value = result;
    logRegular('TextBox', result);
}

function addVerse() {
    var objToAdd = {
        "book_id": book_select[book_select.selectedIndex].value,
        "chapter_id": chapter_select[chapter_select.selectedIndex].value,
        "verse_id": verse_select[verse_select.selectedIndex].value
    };
    // going through all the items to check the dubs
    var dublicateIndex = -1;
    for (var i = 0; i < addedVerses.length; i++) {
        if (JSON.stringify(addedVerses[i]) === JSON.stringify(objToAdd)) {
            dublicateIndex = i;
            break;
        }
    }
    // remove prev dublicate if met
    if (dublicateIndex >= 0) addedVerses.splice(dublicateIndex, 1);
    addedVerses.push(objToAdd);
    updateRequestTextBox();
}

function addTranslation() {
    var objToAdd = {
        "id": translationSelect[translationSelect.selectedIndex].value
    };
    // going through all the items to check the dubs
    var dublicateIndex = -1;
    for (var i = 0; i < addedTranslations.length; i++) {
        if (JSON.stringify(addedTranslations[i]) === JSON.stringify(objToAdd)) {
            dublicateIndex = i;
            break;
        }
    }
    // remove prev dublicate if met
    if (dublicateIndex >= 0) addedTranslations.splice(dublicateIndex, 1);
    addedTranslations.push(objToAdd);
    updateRequestTextBox();
}