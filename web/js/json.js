define([], function () {
    function getdatajson(div) {
        let json = {};
        let fields = $(div).find("input[type='checkbox']:checked");
        for (let f of fields) {
            let key = $(f).attr('data-key');
            let value = $(f).attr('value');
            if (!(key in json)) {
                json[key] = [];
            }
            json[key].push(value);
        }
        return json;
    }
    return { 'getdatajson': getdatajson };
});