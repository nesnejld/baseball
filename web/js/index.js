(function () {
    $.get('baseballsavant.json').then(result => {
        console.log(result);
        let ol = $("<ol>").addClass("list-group").prop('open', true);
        for (let k in result) {
            let li = $("<li>").addClass("list-group-item");
            let span = $("<span>").addClass('target').text(k);
            li.append(span);
            span.on("click", e => {
                console.log(e);
                e.stopImmediatePropagation();
                let ol = $($(e.currentTarget).siblings("ol")[0]);
                li = ol.find("li");
                if (ol.prop('open')) {
                    li.css('display', 'none');
                }
                else {
                    li.css('display', 'block');
                }
                ol.prop('open', !ol.prop('open'));
            });
            ol.append(li);
            let ol_ = $("<ol>").addClass("list-group").prop('open', true);
            li.append(ol_);
            for (let kk in result[k].value.choice) {
                let li = $("<li>").addClass("list-group-item");
                li.text(`${kk} ${result[k].value.choice[kk]}`);
                ol_.append(li);
            }
        }
        $("div.container").empty().append(ol);
    });
})();