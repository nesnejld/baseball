(function () {
    function toggletarget(div) {
        let span = div.find('span');
        let marker = span.prop('marker');
        let target = $(div.siblings('div.container.target')[0]);
        if (div.prop('open')) {
            target.css('display', 'none');
            marker.removeClass('fa-minus').addClass('fa-plus');
        }
        else {
            target.css('display', 'block');
            marker.removeClass('fa-plus').addClass('fa-minus');
        }
        div.prop('open', !div.prop('open'));

    }
    $.get('baseballsavant.json').then(result => {
        console.log(result);
        let ncols = 3;
        let table = $("<table>").addClass("table table-striped");
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
            let div = $("<div>").addClass("target list-item").prop('open', true);
            let i = $("<i>").addClass("fa fa-solid fa-minus target").css("margin-right", "20px");
            td.append(div);
            div.append(i);
            let span = $("<span>").addClass('target').text(k);
            span.prop("marker", i);
            div.append(span);
            div.on("click", e => {
                console.log(e);
                e.stopImmediatePropagation();
                let div = $(e.currentTarget);
                toggletarget(div);
                // let span = div.find('span');
                // let marker = span.prop('marker');
                // let target = $(div.siblings('div.container.target')[0]);
                // // li = ol.find("li");
                // if (div.prop('open')) {
                //     target.css('display', 'none');
                //     marker.removeClass('fa-minus').addClass('fa-plus');
                // }
                // else {
                //     target.css('display', 'block');
                //     marker.removeClass('fa-plus').addClass('fa-minus');
                // }

            });

            {
                let container = $("<div>").addClass("container target");
                div.prop('container', container);
                td.append(container);
                let table = $("<table>").addClass("table table-striped");
                let tbody = $("<tbody>");
                table.append(tbody);
                container.append(table);
                for (let kk in result[k].value.choice) {
                    let tr = $("<tr>");
                    tbody.append(tr);
                    let td = $("<td>");
                    tr.append(td);
                    td.text(kk);
                    td = $("<td>");
                    tr.append(td);
                    td.text(result[k].value.choice[kk]);
                }
            }
            toggletarget(div);
        }
        $("div.container").empty().append(table);
    });
})();