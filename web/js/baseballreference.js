define(['util'], function (util) {
    urlprefix = 'https://www.baseball-reference.com';
    urlpattern = "/leagues/daily.cgi?user_team=&bust_cache=&type={type}&lastndays=7&dates=fromandto&fromandto={start_dt}.{end_dt}&level={level}&franch={franch}&stat=&stat_value=0";
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
        for (key in args) {
            let value = args[key];
            string = string.replace(`{${key}}`, value);
        }
        return string;
    }
    function getdatajson(args) {
        $("div.status").empty().append($("<a>").attr("data-href", urlprefix + interpolate(urlpattern, args)).text("url").attr("href", "#"));
        let sargs = JSON.stringify(args);
        soptions = JSON.stringify({
            'urlprefix': urlprefix,
            'urlpattern': urlpattern,
            'csvfile': '/tmp/getdatajson.csv'
        });
        return new Promise((resolve, reject) => {
            let command = 'uname';
            util.runcommand(command).then(d => {
                let uname = JSON.parse(d).stdout[0].toLowerCase();
                let home = '/home/djensen';
                if (uname == 'darwin') {
                    home = '/Users/djensen';
                }

                command = `PATH=${home}/venv/bin:\${PATH} PYTHONPATH=${home}/git/baseball ../../baseballref/getdata.py '${sargs}' '${soptions}'`;
                // command = `PATH=/Users/djensen/venv/bin:\${PATH} PYTHONPATH=/Users/djensen/git/baseball env`;
                // command = 'env';
                util.runcommand(command).then(function (d) {
                    d = JSON.parse(d);
                    output = JSON.parse(d.stdout.join('\n'));
                    resolve(output);
                });
            });
        });
    }
    return { 'getdatajson': getdatajson, 'urlprefix': urlprefix, 'urlpattern': urlpattern };
});