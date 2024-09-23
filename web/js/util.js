function runcommand(command, options = null) {
    let args = {
        command: 'exec',
        exec: command,
    };
    args = Object.assign(args, options);
    return $.get('/baseball-cgi-bin/commands.py',
        args
    );
}
async function runcommandsync(command) {
    return new Promise((resolve, reject) => {
        runcommand(command).then(d => {
            resolve(JSON.parse(d));
        });
    });
}
function canonicalize(text) {
    let lines = text.split('\n');
    lines = lines.map(l => l.trim());
    return lines.join(' ').trim();
} function interpolate(string, args) {
    for (let key in args) {
        let value = args[key];
        string = string.replace(`{${key}}`, value);
    }
    return string;
}
export { runcommand, runcommandsync, canonicalize, interpolate };
