import { runcommandsync } from './util.js';

let result = await runcommandsync('uname');
let uname = result.stdout.join("\n").trim().toLowerCase();
var urlprefix = 'https://www.baseball-reference.com';
var urlpattern = "/leagues/daily.cgi?user_team=&bust_cache=&type={type}&lastndays=7&dates=fromandto&fromandto={start_dt}.{end_dt}&level={level}&franch={franch}&stat=&stat_value=0";
var parametersurl = '/leagues/daily.fcgi';
var baseurl = "https://baseballsavant.mlb.com/statcast_search/csv?";
var user = 'djensen';
var datadir = uname == 'darwin' ? '/tmp' : '/var/www/data';
var debug = 'true';
export { urlprefix, urlpattern, parametersurl, baseurl, user, datadir, debug, uname };
