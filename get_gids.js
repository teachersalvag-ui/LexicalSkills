const https = require('https');

const url = "https://docs.google.com/spreadsheets/d/1npKHQOuAqO_PqNcdemVtBoZc34DS7l_SURaTl4rP2XY/htmlview";

https.get(url, (res) => {
    let data = '';
    res.on('data', chunk => data += chunk);
    res.on('end', () => {
        // Find sheet names and gids
        // Example: ["Basic",12345] or {name: "Basic", gid: "12345"}
        const gidRegex1 = /\["([^"]+)",(\d+)\]/g;
        let match;
        const gids = {};
        while ((match = gidRegex1.exec(data)) !== null) {
            gids[match[1]] = match[2];
        }
        console.log("Found tabs (regex 1):", gids);

        // also look for gid:
        const gidRegex2 = /"([^"]+)":\["(\d+)"\]/g; 
        // This is just to dump the raw text near 'gid' if regex1 fails
        const gids2 = [];
        const index = data.indexOf('"gid"');
        if (index !== -1) {
            console.log("Snippet near gid:", data.substring(Math.max(0, index-100), index+200));
        }
    });
}).on("error", (err) => {
    console.log("Error: " + err.message);
});
