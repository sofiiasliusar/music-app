let currentAudio = document.getElementById('audio-player');
let currentPlayingIcon = null;

function togglePlay(icon, audioUrl) {
    if (currentAudio.src !== audioUrl) {
        currentAudio.src = audioUrl;
        currentAudio.play();
        if (currentPlayingIcon) {
            currentPlayingIcon.textContent = '▶';
        }
        icon.textContent = '❚❚';
        currentPlayingIcon = icon;
    } else {
        if (currentAudio.paused) {
            currentAudio.play();
            icon.textContent = '❚❚';
        } else {
            currentAudio.pause();
            icon.textContent = '▶';
        }
    }
}

