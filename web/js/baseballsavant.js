import { constructquery } from './url.js';
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
                    constructquery(result);
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
    constructquery(result);
    $("div.container.parameters").empty().append(table);
});
$("div.baseballsavant.datepicker input, div.baseballsavant.enddatepicker input").on('change', function () {
    $.get('baseballsavant.json').then(result => {
        constructquery(result);
    });
    return;
});

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

export { collapseall };