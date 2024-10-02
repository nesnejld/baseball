import { runcommandsync } from './util.js';
// let constants = {
//     urlprefix: 'https://www.baseball-reference.com',
//     urlpattern: "/leagues/daily.cgi?user_team=&bust_cache=&type={type}&lastndays=7&dates=fromandto&fromandto={start_dt}.{end_dt}&level={level}&franch={franch}&stat={stat}&stat_value={stat_value}",
//     parametersurl: '/leagues/daily.fcgi',
//     baseurl: "https://baseballsavant.mlb.com/statcast_search/csv?",
//     user: 'djensen',
//     debug: 'true',
//     browserhome: '/home/djensen'
// };
let constants = {};

async function loadconstants() {
    return new Promise((resolve, reject) => {
        if (Object.keys(constants) == 0) {
            $.get("baseballref/constants.json").then(d => {
                resolve(d);
            });
        }
        else {
            resolve(constants);
        }
    });
}
function setconstants(c) {
    constants = Object.assign(constants, c);
    return constants;
}
async function getconstants() {
    if (Object.keys(constants) == 0) {
        constants = await loadconstants();
        let result = await runcommandsync('uname');
        let uname = result.stdout.join("\n").trim().toLowerCase();
        constants.uname = uname;
        constants.datadir = constants.uname == 'darwin' ? '/tmp' : '/var/www/data';
        constants.home = `/home/${constants.user}`;
        if (uname == 'darwin') {
            constants.home = `/Users/${constants.user}`;
        }
    }
    return constants;
}
export { getconstants, setconstants };
