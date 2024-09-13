import * as url from './url.js';
import { overlay as Overlay } from './overlay.js';
import * as json from './json.js';
// import * as util from './util.js';
import { runcommand, interpolate, canonicalize } from './util.js';
import * as baseballreference from './baseballreference.js';
import { getdropdownvalue, buildoptions } from './baseballreference.js';
$(function () {

    function collapseall() {
        let divs = $("div.target.list-item");
        for (let div of divs) {
            toggletarget($(div), false);
        }
        return;
    }
    function toggletarget(div, bvalue = null) {
        let span = div.find('span');
        let marker = span.prop('marker');
        if (bvalue != null) {
            div.prop('open', !bvalue);
        }
        let target = $(div.siblings('div.container.target')[0]);
        if (div.prop('open')) {
            target.css('display', 'none');
            marker.removeClass('fa-minus').addClass('fa-plus');
        }
        else {
            let offset = div.offset();

            target.css({
                'display': 'block',
                'top':
                    `${offset.top + 20}px`,
                'left':
                    `${offset.left + 20}px`,

            });
            marker.removeClass('fa-plus').addClass('fa-minus');
        }
        div.prop('open', !div.prop('open'));

    }
    $.get('baseballsavant.json').then(result => {
        console.log(result);
        let ncols = 3;
        let table = $("<table>").addClass("table table-striped");
        table.on("click", e => {
            e.stopImmediatePropagation();
        });
        let tbody = $("<tbody>");
        table.append(tbody);
        let tr = $('<tr>');
        tbody.append(tr);
        let icol = 0;
        for (let k in result) {
            let td = $("<td>");
            if (icol == ncols) {
                tr = $('<tr>');
                tbody.append(tr);
                icol = 0;
            }
            icol += 1;
            tr.append(td);
            let div = $("<div>").addClass("target list-item").prop('open', true).attr('data-key', k);
            let i = $("<i>").addClass("fa fa-solid fa-minus target").css("margin-right", "20px");
            td.append(div);
            div.append(i);
            let span = $("<span>").addClass('target').text(`${result[k].label.replace(':', '')} (${k})`);
            span.prop("marker", i);
            div.append(span);
            div.on("click", e => {
                console.log(e);
                e.stopImmediatePropagation();
                let div = $(e.currentTarget);
                let p = div.prop('open');
                collapseall();
                div.prop('open', p);
                toggletarget(div);
            });

            {
                let container = $("<div>").addClass("container target");
                container.attr('data-key', k);
                div.prop('container', container);
                td.append(container);
                let table = $("<table>").addClass("table table-striped");
                table.on("click", e => {
                    e.stopImmediatePropagation();
                });
                let tbody = $("<tbody>").attr('data-key', k);
                table.append(tbody);
                container.append(table);
                for (let kk in result[k].value.choice) {
                    let tr = $("<tr>").attr('data-key', k);
                    tbody.append(tr);
                    let td = $("<td>").attr('data-key', k);
                    tr.append(td);
                    let checkbox = $("<input>").attr('type', 'checkbox').attr('data-key', k);
                    td.append(checkbox);
                    checkbox.prop('div', div).attr('data-key', k);
                    checkbox.on('click', e => {
                        e.stopImmediatePropagation();
                        url.constructquery(result);
                        return;
                    });
                    td = $("<td>").attr('data-key', k);
                    td.text(kk);
                    checkbox.prop('value', kk).attr('data-key', k);
                    tr.append(td);
                    td = $("<td>").attr('data-key', k);
                    tr.append(td);
                    td.text(result[k].value.choice[kk]);
                }
            }
            toggletarget(div);
        }
        url.constructquery(result);
        $("div.container.parameters").empty().append(table);
    });
    $("#baseballsavant div.retrievecsv").on("click", e => {
        let url = $("div.status").text();
        let outputfile = $('div.output').text();
        Overlay.text(`Retrieving ${url} and writing ${outputfile}`);
        Overlay.show();
        runcommand(`curl '${url}'`, { output: outputfile }).then(d => {
            d = JSON.parse(d);
            Overlay.hide();
            return;
        });
    });
    $("#baseballsavant div.getdatajson").on("click", e => {
        let outputfile = $('div.output').text().replace(/\.csv$/, '.json');
        Overlay.text(`Writing ${outputfile}`);
        Overlay.show();
        let parameters = json.getdatajson($("body>div.container.parameters"));
        parameters['type'] = 'detail';
        parameters['all'] = 'true';
        let data = JSON.stringify(parameters);
        let args = {
            command: 'file',
            filename: outputfile,
            data: data
        };
        $.get('/baseball-cgi-bin/commands.py',
            args
        ).done(d => {
            let result = JSON.parse(d);
            return;
        }).always(d => {
            Overlay.hide();
        });
        return;
        // runcommand(`curl '${url}'`, { output: outputfile }).then(d => {
        //     d = JSON.parse(d);
        //     Overlay.hide();
        //     return;
        // });
    });
    $("#baseballref div.retrievecsv").on("click", e => {

        $("div.container.baseballref").empty().text('Retrieving data');
        let startdate = $("#baseballref div.datepicker input").val();
        let enddate = $("#baseballref div.enddatepicker input").val();
        let franch = getdropdownvalue('Franchise');
        let level = getdropdownvalue('Level');
        let type = getdropdownvalue('type');
        // franch = $(franch.closest("li")).attr("data-value");
        let args = {
            "franch": franch,
            "level": level,
            "end_dt": enddate,
            "start_dt": startdate,
            "type": type
        };
        baseballreference.getdatajson(args).then(function (_data_) {
            let data = _data_.data;
            let fields = ['data', 'csk', 'href', 'title'];
            let urlprefix = baseballreference.urlprefix;
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
            let table = $("<table>").addClass('table table-striped');
            let thead = $("<thead>");
            let tbody = $("<tbody>");
            table.append(thead).append(tbody);
            let tr = $("<tr>");
            thead.append(tr);
            for (let c of data.columns) {
                let th = $("<th>").text(c.key);
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
    $("body").on("click", e => {
        collapseall();
        return;
    });
    $("#datepicker").datepicker({
        autoclose: true,
        todayHighlight: true,
    }).datepicker('update', new Date()).
        datepicker('option', 'onSelect', function () {
            alert(date);
        });
    $("#enddatepicker").datepicker({
        autoclose: true,
        todayHighlight: true,
    }).datepicker('update', new Date()).
        datepicker('option', 'onSelect', function () {
            alert(date);
        });
    $("#baseballref div.datepicker").datepicker({
        autoclose: true,
        todayHighlight: true,
    }).datepicker('update', new Date()).
        datepicker('option', 'onSelect', function () {
            alert(date);
        });
    $("#baseballref div.enddatepicker").datepicker({
        autoclose: true,
        todayHighlight: true,
    }).datepicker('update', new Date()).
        datepicker('option', 'onSelect', function () {
            alert(date);
        });
    $("#datepicker input, #enddatepicker input").on('change', function () {
        $.get('baseballsavant.json').then(result => {
            url.constructquery(result);
        });
        return;
    });
    $("#baseballref-tab").on("click", e => {
        $("div.status").text('');
    });
    $.get("baseballref/help.html").then(d => {
        $("div.container.baseballref").empty().append(d);
    });
    $("#baseballref-tab").on("shown.bs.tab", e => {
        let parameters = baseballreference.getparametersjson().then(data => {
            let target = $("#baseballref div.options");
            target.empty();
            buildoptions(target, data.parameters);
            return;
        });
        return;
    }
    );
    return;

});
