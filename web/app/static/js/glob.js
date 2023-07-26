/**
 * Sets a cookie with name `cname`, value `cvalue` that expires in `exdays` days
 * Function is taken from https://www.w3schools.com/js/js_cookies.asp.
 * @param {String} cname 
 * @param {String} cvalue 
 * @param {Number} exdays 
 */
function setCookie(cname, cvalue, exdays) {
    const d = new Date();
    d.setTime(d.getTime() + (exdays*24*60*60*1000));
    let expires = "expires="+ d.toUTCString();
    document.cookie = encodeURIComponent(cname) + "=" + encodeURIComponent(cvalue) + ";" + encodeURIComponent(expires) + ";path=/;SameSite=Strict";
}

/**
 * Set a language cookie.
 * Intended value options are ["ru", "en"]
 * 
 * Also refreshes the page so content language is updated. 
 * Since translations are handeled on backend
 * 
 * @param {String} lang 
 * @returns {Boolean} true if lang is a valid option, false if its not
 */
function setLanguage(lang) {
    var validLanguages = ["ru", "en"];
    if (!validLanguages.includes(lang)) return false;
    setCookie("lang", lang, 365);
    window.location.reload();
    return true;
}
