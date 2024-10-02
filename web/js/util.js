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
}
function interpolate(string, args) {
    for (let key in args) {
        let value = args[key];
        string = string.replace(`{${key}}`, value);
    }
    return string;
}
function savefile(filename, data, mimetype) {
    let blob = new Blob([data], { type: mimetype });
    let link = document.createElement("a");
    link.download = filename;
    //link.innerHTML = "Download File";
    link.href = window.URL.createObjectURL(blob);
    document.body.appendChild(link);
    link.onclick = () => {
        setTimeout(() => {
            document.body.removeChild(link);
            window.URL.revokeObjectURL(link.href);
        }, 100);
    };
    link.click();
}
export { runcommand, runcommandsync, canonicalize, interpolate, savefile };
