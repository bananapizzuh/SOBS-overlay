function updateSongInfo(songName, artists, albumCover, duration, progress) {
    let artistString = "";
    for (let i = 0; i < artists.length; i++) {
        if (i === artists.length - 1) {
            artistString += artists[i].name;
            break;
        }
        artistString += `${artists[i].name}, `;
    } 

    document.getElementById('song-name').innerText = songName;
    document.getElementById('artists').innerText = artistString;
    document.getElementById('album-cover').src = albumCover;

    
    let lengthS = Math.floor(duration / 1000);
    let lengthM = Math.floor(lengthS / 60);
    let lengthMS = lengthS % 60;
    if (lengthMS < 10) {
        lengthMS = `0${lengthMS}`;
    }

    let progressS = Math.floor(progress / 1000);
    let progressM = Math.floor(progressS / 60);
    let progressMS = progressS % 60;
    if (progressMS < 10) {
        progressMS = `0${progressMS}`;
    }

    document.getElementById('progress-bar').style.width = `${(progress / duration) * 100}%`;

    // Update time info
    document.getElementById('time-info').innerText = `${progressM}:${progressMS} / ${lengthM}:${lengthMS}`;
    scroll_text();
}
function scroll_text() {
    var songElement = document.querySelector(".song");
    var artistElement = document.querySelector(".artist");
    console.log(songElement.scrollWidth, artistElement.scrollWidth );
    if (songElement.scrollWidth > 220) {
        console.log("adding marquee");
        songElement.classList.add("marquee");
    } else {
        songElement.classList.remove("marquee");
    }

    if (artistElement.scrollWidth > 220) {
        artistElement.classList.add("marquee");
    } else {
        artistElement.classList.remove("marquee");
    }
}

setInterval(function() {
    fetch("https://sobs.bananapizzuh.dev/update")
        .then(response => response.json())
        .then(data => {
            updateSongInfo(data.track_name, data.artists, data.album_cover, data.duration, data.progress);
        });
}, 1000);
