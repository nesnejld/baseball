import * as util from './util.js';
import { urlprefix, urlpattern, parametersurl, user } from './constants.js';
import { seterror, setstatus, seturl } from './render.js';
import { overlay as Overlay } from './overlay.js';

//
// Calling url with jQuery directly has COR violation
//
let command = 'uname';
let uname = null;
let home = null;
function getdropdowndiv(label) {
    return $(`<div class="dropdown" data-name='${util.canonicalize(label)}'>
<div class="btn btn-primary btn-small dropdown-toggle" type="button" data-bs-toggle="dropdown" aria-expanded="false">
${label}
</div>
<div class="dropdown-menu">
<ul style="max-height:500px;overflow:auto;">
</ul>
</div>
</div>`);
};
util.runcommand(command).then(d => {
    uname = JSON.parse(d).stdout[0].toLowerCase();
    home = `/home/${user}`;
    if (uname == 'darwin') {
        home = `/Users/${user}`;
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
    let url = urlprefix + interpolate(urlpattern, args);
    seturl(url);
    let csvfile = `/tmp/baseballref.${args.start_dt}.${args.end_dt}.csv`;
    setstatus(`Writing ${csvfile}`);
    let sargs = JSON.stringify(args);
    let soptions = JSON.stringify({
        'urlprefix': urlprefix,
        'urlpattern': urlpattern,
        'csvfile': csvfile,
        'debug': false,
        'actions': ['data', 'csv']
    });
    return new Promise((resolve, reject) => {
        let command = 'uname';
        util.runcommand(command).then(d => {
            let uname = JSON.parse(d).stdout[0].toLowerCase();
            home = `/home/${user}`;
            if (uname == 'darwin') {
                home = `/Users/${user}`;
            }
            let sargs = JSON.stringify(args);

            command = `PATH=${home}/venv/bin:\${PATH} PYTHONPATH=${home}/git/baseball ../../baseballref/main.py '${sargs}' '${soptions}'`;
            Overlay.text(`Retrieving ${csvfile}`);
            Overlay.show();
            util.runcommand(command).then(function (d) {
                d = JSON.parse(d);
                seterror(d.stderr.join('\n'), { color: 'red' });
                setstatus(`Wrote ${csvfile}`, { color: 'blue', background: 'lightgray' });
                Overlay.hide();
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
                seterror(d.stderr.join('\n'), { color: 'red' });
                resolve(JSON.parse(d.stdout.join('\n')));
            });
        });
    });
}
function addradiobuttons(ul, label, options) {
    let count = 0;
    let selected = null;
    function handleclick(e) {
        e.stopPropagation();
        let parameter = $(e.currentTarget).closest('div.dropdown').attr('data-name');
        if (['Dates', 'Since', "Decisions"].includes(parameter)) {
            let li = $(e.currentTarget);
            let dates;
            if (li.prop("tagName") == 'LI') {
                dates = li.attr("data-value").split('.');
            }
            else {
                dates = getdropdownvalue(parameter).split('.');
            }
            let startdate = dates[0];
            let enddate = dates.length == 1 ? dates[0] : dates[1];
            if (startdate == 'yesterday') {
                startdate = new Date(new Date().setDate(new Date().getDate() - 1));
                enddate = startdate;
            }
            if ($(e.currentTarget).attr('data-group') && $(e.currentTarget).attr('data-group') == "since") {
                enddate = new Date(Date.now());
            }
            // startdate = '2024-09-12';
            // enddate = '2024-09-13';
            $("#baseballref div.datepicker").datepicker("setDate", startdate);
            $("#baseballref div.enddatepicker").datepicker("setDate", enddate);
        }
        setstatus(`args: ${JSON.stringify(getargs())}`, { "color": "black" });
        return;
    }
    for (let option of options) {
        let choices = option.choices;
        if (option.choices.length > 0) {
            let dropdowndiv = getdropdowndiv(option.label).addClass('sub-menu');
            ul.after(dropdowndiv);
            dropdowndiv.on("click", e => {
                // e.preventDefault();
                e.stopPropagation();
                e.stopPropagation();
                $(e.currentTarget).parent().find("div.dropdown-toggle.show").toArray().filter(element => {
                    return $(e.currentTarget).find("div.dropdown-toggle")[0] != element;
                }).forEach(element => {
                    $(element).dropdown('toggle');
                });
            });
            let ulinner = dropdowndiv.find("ul");
            for (let choice of choices) {
                let li = $("<li>").addClass("dropdown-item").attr({
                    "href": "#", "data": choice.label,
                    'data-value': choice.value, "data-label": option.label, 'data-group': option.value
                }).
                    append($(`<div class="form-check">
        <input class="form-check-input" type="radio" name="${label}_radio" id="${label}_radio_${count}">
        <label class="form-check-label" for="${label}_radio_${count}">
          ${choice.label}
        </label>
      </div>`));
                if ('selected' in choice && choice['selected']) {
                    li.find('input').attr('checked', true);
                    selected = li.find('input');
                }
                ulinner.append(li);
                li.on("click", e => handleclick(e));
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
            li.on("click", e => handleclick(e));
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
        let div = getdropdowndiv(label);
        let ul = div.find("ul");
        addradiobuttons(ul, label, options[label]);
        target.append(div);
        continue;
    }
    return;
}
function resize() {
    let offset = $("div.container.baseballref").offset();
    console.log(`resize: ${window.innerHeight} ${window.innerWidth}`);
    let width = window.innerWidth - offset.left - 40;
    let height = window.innerHeight - offset.top - 100;
    $("div.baseballref.container").css({ 'max-width': `${width}px`, 'max-height': `${height}px`, 'margin': '0px' });
}
// Events
function getargs() {
    let startdate = $("#baseballref div.datepicker input").val();
    let enddate = $("#baseballref div.enddatepicker input").val();
    let franch = getdropdownvalue('Franchise');
    let level = getdropdownvalue('Level');
    let type = getdropdownvalue('type');
    // franch = $(franch.closest("li")).attr("data-value");
    return {
        "franch": franch,
        "level": level,
        "end_dt": enddate,
        "start_dt": startdate,
        "type": type
    };
}
$("#baseballref div.retrievecsv").on("click", e => {
    $("div.container.baseballref").empty().text('Retrieving data');
    // franch = $(franch.closest("li")).attr("data-value");
    getdatajson(getargs()).then(function (_data_) {
        let data = _data_.data;
        let fields = ['data', 'csk', 'href', 'title'];
        function gettd(c) {
            for (let f of fields) {
                if (f in c) {
                    if (f == 'href') {
                        return $("<td>").append($("<a>").attr("data-href", urlprefix + c[f]).text(c['key']).attr("href", "#"));
                    }
                    return $("<td>").text(c[f]);
                }
            }
        }
        $("div.container.baseballref").empty().append($("<pre>").text(JSON.stringify(data, null, 2)));
        let table = $("<table>").addClass('table table-striped table-fit');
        let thead = $("<thead>");
        let tbody = $("<tbody>");
        table.append(thead).append(tbody);
        let tr = $("<tr>").addClass("table-dark");
        thead.append(tr);
        for (let c of data.columns) {
            let th = $("<th>").text(c.key.split('_').join(' '));
            tr.append(th);
        }
        let ii = 0;
        for (let i in data.rows) {
            let r = data.rows[i];
            if (r.length == 0) {
                continue;
            }
            ii += 1;
            let tr = $("<tr>");
            let td = $("<td>").text(ii);
            tbody.append(tr);
            tr.append(td);
            for (let c of r) {
                td = gettd(c);
                tr.append(td);
            }
        }
        $("div.container.baseballref").empty().append(table);
        resize();
        $("a[data-href]").on("click", e => {
            let href = $(e.currentTarget).attr('data-href');
            window.open(href);
            return;
        });
        return;
    });

    return;
});
$("#baseballref div.getdatajson").on("click", e => {
    return;
});
$("#baseballref-tab").on("shown.bs.tab", e => {
    Overlay.text(`Retrieving options`);
    Overlay.show();
    let parameters = getparametersjson().then(data => {
        let target = $("#baseballref div.options");
        target.empty();
        buildoptions(target, data.parameters);
        resize();
        Overlay.hide();
        return;
    });
    return;
});

export {
    urlprefix,
    urlpattern,
    getdatajson,
    getparametersjson,
    buildoptions,
    getdropdownvalue,
    resize
};
