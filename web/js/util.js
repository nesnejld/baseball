define([], function () {
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
    return { runcommand: runcommand };
});