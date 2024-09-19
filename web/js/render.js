function seterror(message, attr = null) {
    return $("div.error").empty().append($("<pre>").removeAttr('style').css(attr).text(message));
}
function setstatus(message, css = {}) {
    let margin = $("div.status").css("margin");
    return $("div.status").empty().css(css).css('margin', margin).text(message);
}
function seturl(url) {
    return $("div.url").empty().append($("<a>").attr({ "href": "#", "data-href": url }).text(url));
}
export { seterror, setstatus, seturl };