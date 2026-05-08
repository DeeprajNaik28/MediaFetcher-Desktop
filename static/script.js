let isPlaylist = false;

async function getInfo() {
    let url = document.getElementById("url").value;

    let res = await fetch("/info", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({url})
    });

    let data = await res.json();

    document.getElementById("videoSection").innerHTML = "";
    document.getElementById("playlistSection").innerHTML = "";
    document.getElementById("playlistOptions").style.display = "none";

    if (data.type === "video") {
        isPlaylist = false;

        document.getElementById("videoSection").innerHTML = `
            <h3>${data.title}</h3>
            <img src="${data.thumbnail}" width="300">
            <br>
            <select id="formats"></select>
            <br>
            <label><input type="checkbox" id="audio"> MP3</label>
        `;

        let formats = document.getElementById("formats");

        data.formats.forEach(f => {
            let opt = document.createElement("option");
            opt.value = f.format_id;
            opt.innerText = `${f.quality} (${f.ext}) - ${f.filesize}MB`;
            formats.appendChild(opt);
        });

    } else {
        isPlaylist = true;

        document.getElementById("playlistOptions").style.display = "block";

        let html = `<div class="grid">`;

        data.videos.forEach(v => {
            html += `
                <div class="card">
                    <img src="${v.thumbnail}">
                    <p>${v.title}</p>
                    <input type="checkbox" value="${v.url}">
                </div>
            `;
        });

        html += `</div>`;
        document.getElementById("playlistSection").innerHTML = html;
    }
}

// DOWNLOAD
async function download() {
    trackProgress();

    if (isPlaylist) {
        let urls = [];
        document.querySelectorAll(".card input:checked")
            .forEach(cb => urls.push(cb.value));

        if (urls.length === 0) {
            alert("Select videos!");
            return;
        }

        let quality = document.getElementById("playlistQuality").value;
        let audio = document.getElementById("playlistAudio").checked;

        await fetch("/download", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({urls, quality, audio})
        });

    } else {
        await fetch("/download", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({
                url: document.getElementById("url").value,
                format_id: document.getElementById("formats").value,
                audio: document.getElementById("audio").checked
            })
        });
    }
}

// CANCEL
async function cancelDownload() {
    await fetch("/cancel", { method: "POST" });
}

// PROGRESS
function trackProgress() {
    let bar = document.getElementById("bar");

    let interval = setInterval(async () => {
        let res = await fetch("/progress");
        let data = await res.json();

        let percent = parseFloat(data.percent);
        if (!isNaN(percent)) bar.style.width = percent + "%";

        document.getElementById("speed").innerText = "Speed: " + data.speed;
        document.getElementById("eta").innerText = "ETA: " + data.eta;
        document.getElementById("current").innerText = "File: " + data.current;
        document.getElementById("status").innerText = "Status: " + data.status;

        if (data.status === "completed" || data.status === "cancelled") {
            clearInterval(interval);
        }
    }, 500);
}