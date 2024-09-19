var urlprefix = 'https://www.baseball-reference.com';
var urlpattern = "/leagues/daily.cgi?user_team=&bust_cache=&type={type}&lastndays=7&dates=fromandto&fromandto={start_dt}.{end_dt}&level={level}&franch={franch}&stat=&stat_value=0";
var parametersurl = '/leagues/daily.fcgi';
var baseurl = "https://baseballsavant.mlb.com/statcast_search/csv?";
var user = 'djensen';
var datadir='/var/www/data'
export { urlprefix, urlpattern, parametersurl, baseurl, user, datadir };
