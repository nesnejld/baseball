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
function canonicalize(text) {
    let lines = text.split('\n');
    lines = lines.map(l => l.trim());
    return lines.join(' ').trim();
}
export { runcommand, canonicalize };
