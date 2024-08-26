const jspaths = {
    url: 'js/url',
    overlay: 'js/overlay'
};

require.config({
    paths: jspaths,
    waitSeconds: 200,
});
$(function () {
    require(['url', 'overlay'], function (url, Overlay) {
        let keys = null;
        function runcommand(command, options = null) {
            args = {
                command: 'exec',
                exec: command,
            };
            args = Object.assign(args, options);
            return $.get('/baseball-cgi-bin/commands.py',
                args
            );
            return;
        }
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
            keys = XPathResult;
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
                    let tbody = $("<tbody>");
                    table.append(tbody);
                    container.append(table);
                    for (let kk in result[k].value.choice) {
                        let tr = $("<tr>");
                        tbody.append(tr);
                        let td = $("<td>");
                        tr.append(td);
                        let checkbox = $("<input>").attr('type', 'checkbox');
                        td.append(checkbox);
                        checkbox.prop('div', div);
                        checkbox.on('click', e => {
                            e.stopImmediatePropagation();
                            url.constructquery(result);
                            return;
                        });
                        td = $("<td>");
                        td.text(kk);
                        checkbox.prop('value', kk);
                        tr.append(td);
                        td = $("<td>");
                        tr.append(td);
                        td.text(result[k].value.choice[kk]);
                    }
                }
                toggletarget(div);
            }
            url.constructquery(result);
            $("div.container").empty().append(table);
        });
        $("button.retrievecsv").on("click", e => {
            let url = $("div.status").text();
            let outputfile = '/tmp/aaaa.csv';
            Overlay.text(`Retrieving ${url} and writing ${outputfile}`);
            Overlay.show();
            runcommand(`curl '${url}'`, { output: outputfile }).then(d => {
                d = JSON.parse(d);
                Overlay.hide();
                return;
            });
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
        $("#datepicker input, #enddatepicker input").on('change', function () {
            url.constructquery(keys);
            return;
        });
        return;
    });
});
