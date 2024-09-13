import * as util from './util.js';
var urlprefix = 'https://www.baseball-reference.com';
var urlpattern = "/leagues/daily.cgi?user_team=&bust_cache=&type={type}&lastndays=7&dates=fromandto&fromandto={start_dt}.{end_dt}&level={level}&franch={franch}&stat=&stat_value=0";
var parametersurl = '/leagues/daily.fcgi';

//
// Calling url with jQuery directly has COR violation
//
let command = 'uname';
let uname = null;
let home = null;
util.runcommand(command).then(d => {
    uname = JSON.parse(d).stdout[0].toLowerCase();
    home = '/home/djensen';
    if (uname == 'darwin') {
        home = '/Users/djensen';
    }
});
function interpolate(string, args) {
    for (let key in args) {
        let value = args[key];
        string = string.replace(`{${key}}`, value);
    }
    return string;
}
function getdatajson(args) {
    $("div.status").empty().append($("<a>").attr("data-href", urlprefix + interpolate(urlpattern, args)).text("url").attr("href", "#"));
    let sargs = JSON.stringify(args);
    let soptions = JSON.stringify({
        'urlprefix': urlprefix,
        'urlpattern': urlpattern,
        'csvfile': '/tmp/getdatajson.csv',
        'debug': false,
        'actions': ['data']
    });
    return new Promise((resolve, reject) => {
        let command = 'uname';
        util.runcommand(command).then(d => {
            let uname = JSON.parse(d).stdout[0].toLowerCase();
            let home = '/home/djensen';
            if (uname == 'darwin') {
                home = '/Users/djensen';
            }
            let sargs = JSON.stringify(args);

            command = `PATH=${home}/venv/bin:\${PATH} PYTHONPATH=${home}/git/baseball ../../baseballref/main.py '${sargs}' '${soptions}'`;
            // command = `PATH=/Users/djensen/venv/bin:\${PATH} PYTHONPATH=/Users/djensen/git/baseball env`;
            // command = 'env';
            util.runcommand(command).then(function (d) {
                d = JSON.parse(d);
                resolve(JSON.parse(d.stdout.join('\n')));
            });
        });
    });
}
function getparametersjson(args = {}) {
    let soptions = JSON.stringify({
        'urlprefix': urlprefix,
        'urlpattern': parametersurl,
        'debug': false,
        'actions': ['parameters']
    });
    let sargs = JSON.stringify(args);
    return new Promise((resolve, reject) => {
        let command = 'uname';
        util.runcommand(command).then(d => {
            let uname = JSON.parse(d).stdout[0].toLowerCase();
            let home = '/home/djensen';
            if (uname == 'darwin') {
                home = '/Users/djensen';
            }
            command = `PATH=${home}/venv/bin:\${PATH} PYTHONPATH=${home}/git/baseball ../../baseballref/main.py '${sargs}' '${soptions}'`;
            // command = `PATH=/Users/djensen/venv/bin:\${PATH} PYTHONPATH=/Users/djensen/git/baseball env`;
            // command = 'env';
            util.runcommand(command).then(function (d) {
                d = JSON.parse(d);
                resolve(JSON.parse(d.stdout.join('\n')));
            });
        });
    });
}
function addradiobuttons(ul, label, options, defult) {
    let count = 0;
    let selected = null;
    for (let option of options) {
        let choices = option.choices;
        if (option.choices.length > 0) {
            for (let option of choices) {
                let li = $("<li>").addClass("dropdown-item").attr({ "href": "#", "data": option.label, 'data-value': option.value, "data-label": label }).
                    append($(`<div class="form-check">
        <input class="form-check-input" type="radio" name="${label}_radio" id="${label}_radio_${count}">
        <label class="form-check-label" for="${label}_radio_${count}">
          ${option.label}
        </label>
      </div>`));
                if ('selected' in option && option['selected']) {
                    li.find('input').attr('checked', true);
                    selected = li.find('input');
                }
                ul.append(li);
                count += 1;

            }
        }
        else {
            let li = $("<li>").addClass("dropdown-item").attr({ "href": "#", "data": option.label, 'data-value': option.value, "data-label": label }).
                append($(`<div class="form-check">
        <input class="form-check-input" type="radio" name="${label}_radio" id="${label}_radio_${count}">
        <label class="form-check-label" for="${label}_radio_${count}">
          ${option.label}
        </label>
      </div>`));
            if ('selected' in option && option['selected']) {
                li.find('input').attr('checked', true);
                selected = li.find('input');
            }
            ul.append(li);
            count += 1;
        }
    }
    if (selected == null) {
        $(ul.find("li")[0]).find('input').attr('checked', true);
    }
}
function getdropdownvalue(name) {
    return $($(`#baseballref div.options div.dropdown[data-name="${name}"]`).
        find(`ul li[data-label="${name}"] input:checked`).closest("li")).attr("data-value");

}
function buildoptions(target, options) {

    for (let label in options) {
        let div = $(`<div class="dropdown" data-name='${util.canonicalize(label)}'>
                    <div class="btn btn-primary btn-small dropdown-toggle" type="button" data-bs-toggle="dropdown" aria-expanded="false">
                    ${label}
                    </div>
                    <div>
                    <ul class="dropdown-menu" style="max-height:500px;overflow:auto;">
                    </ul>
                    </div>
                    </div>`);

        let ul = div.find("ul");
        addradiobuttons(ul, label, options[label]);
        div.find("li").on("click", e => {
            let parameter = $(e.currentTarget).closest('div.dropdown').attr('data-name');
            if (parameter == 'Dates') {
                let dates = getdropdownvalue('Dates').split('.');
                let startdate = dates[0];
                let enddate = dates.length == 1 ? dates[0] : dates[1];
                if (startdate == 'yesterday') {
                    startdate = new Date(new Date().setDate(new Date().getDate() - 1));
                    enddate = startdate;
                }
                // startdate = '2024-09-12';
                // enddate = '2024-09-13';
                $("#baseballref div.datepicker").datepicker("setDate", startdate);
                $("#baseballref div.enddatepicker").datepicker("setDate", enddate);
                return;
            }
        });
        target.append(div);
        continue;
    }
    return;
}


export {
    urlprefix,
    urlpattern,
    getdatajson,
    getparametersjson,
    buildoptions,
    getdropdownvalue
};
