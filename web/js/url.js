
let baseurl = "https://baseballsavant.mlb.com/statcast_search/csv?";
function constructquery(keys) {
    // let key = div.attr('data-key');
    let status = '';
    let keyprefix = '';
    for (let k in keys) {
        let div__ = $($(`div.target.container[data-key='${k}']`)[0]);
        let checks = div__.find('input:checked');
        if (checks.length > 0) {
            status += keyprefix + k + '=';
            prefix = '';
            for (let c of checks) {
                let cc = $(c);
                console.log(`${k}: ${cc.prop('value')}`);
                status += prefix + cc.prop('value');
                prefix = '|';
            }
            keyprefix = '&';
        }
        // console.log(k);dd
    }
    let startdate = $("#datepicker input").val();
    let enddate = $("#enddatepicker input").val();
    status += `${keyprefix}game_date_gt=${startdate}`;
    keyprefix = '&';
    status += `${keyprefix}game_date_lt=${enddate}`;
    status += '&all=true&type=detail';
    $("div.status").text(`${baseurl}${status}`);
    $("div.output").text(`/tmp/data.${startdate}.${enddate}.csv`);
    return;
}
export { constructquery };