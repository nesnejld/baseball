function runcommand(command, options = null) {
    let args = {
        command: 'exec',
        exec: command,
    };
    args = Object.assign(args, options);
    return $.get('/baseball-cgi-bin/commands.py',
        args
    );
    return;
}
export { runcommand };
