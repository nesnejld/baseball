import * as url from './url.js';
import { overlay as Overlay } from './overlay.js';
import * as json from './json.js';
// import * as util from './util.js';
import { runcommand, interpolate, canonicalize } from './util.js';
import * as baseballreference from './baseballreference.js';
import * as baseballsavant from './baseballsavant.js';
import { collapseall } from './baseballsavant.js';
import { getdropdownvalue, buildoptions } from './baseballreference.js';
import { setstatus } from './render.js';
$(function () {

    window.onresize = baseballreference.resize;

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

    $("#baseballref-tab").on("click", e => {
        setstatus('');
    });
    $.get("baseballref/help.html").then(d => {
        $("div.container.baseballref").empty().append(d);
    });
    return;

});
