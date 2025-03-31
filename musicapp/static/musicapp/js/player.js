
let currentAudio = document.getElementById('bottom-audio-player');
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

const audioPlayer = document.getElementById('bottom-audio-player');

  // const playPauseBtn = document.querySelector('.play-pause');
  // const progressBar = document.getElementById('progress-bar');
  // const progress = document.getElementById('progress');
  // const currentTimeElement = document.getElementById('current-time');
  // const totalDurationElement = document.getElementById('total-duration');
  let currentSongElement = null;
    const playPauseButtons = document.querySelectorAll('.play-pause');

    // Get progress bars
    const progressBars = document.querySelectorAll('.progress-bar');
    const progressIndicators = document.querySelectorAll('.progress');

    // Get current time & duration elements
    const currentTimeElements = document.querySelectorAll('#current-time');
    const totalDurationElements = document.querySelectorAll('#total-duration');
  function playSong(element, songUrl) {
      if (currentSongElement === element) {
          togglePlayPause();
          return;
        }

      audioPlayer.pause();
      progress.style.width = "0%";
      currentTimeElements.forEach(timeElement => timeElement.textContent = "0:00");
      totalDurationElements.forEach(totalElement => totalElement.textContent = "0:00");
      audioPlayer.src = songUrl;
      playPauseButtons.forEach(btn => btn.innerHTML = "▶");

      setTimeout(() => {
          audioPlayer.play();
          playPauseButtons.forEach(btn => btn.innerHTML = "❚❚");
          updateSongHighlight(element);
          currentSongElement = element;
          }, 500); // Wait for half a second before playing the new song
  }

  function togglePlayPause() {
      if (audioPlayer.paused) {
          audioPlayer.play();
          playPauseButtons.forEach(btn => btn.innerHTML = "❚❚"); // Pause symbol
          if (currentSongElement) {
              currentSongElement.innerHTML = "❚❚";
          }
      } else {
          audioPlayer.pause();
          playPauseButtons.forEach(btn => btn.innerHTML = "▶");
          if (currentSongElement) {
              currentSongElement.innerHTML = "▶";
          }
      }
  }

  // BUG FIX - update total when it is loaded (include pause in between)
  audioPlayer.addEventListener("loadedmetadata", () => {
    if (!isNaN(audioPlayer.duration)) {
        const totalMinutes = Math.floor(audioPlayer.duration / 60);
        const totalSeconds = Math.floor(audioPlayer.duration % 60);
        totalDurationElements.forEach(e => e.textContent = `${totalMinutes}:${totalSeconds.toString().padStart(2, "0")}`);
    }
});

  // Update progress bar as song plays
  audioPlayer.addEventListener("timeupdate", () => {
      if (!audioPlayer.duration) return;  //  audio is not loaded yet, so the function exits early;

      const progressPercentage = (audioPlayer.currentTime / audioPlayer.duration) * 100;
        progressIndicators.forEach(indicator => {
            indicator.style.width = `${progressPercentage}%`;
        });
      // progress.style.width = `${progressPercentage}%`;

      // Update current time display
      const currentMinutes = Math.floor(audioPlayer.currentTime / 60);
      const currentSeconds = Math.floor(audioPlayer.currentTime % 60);
      currentTimeElements.forEach(e => e.textContent = `${currentMinutes}:${currentSeconds.toString().padStart(2, "0")}`);

      // Set total duration when available
      // if (!totalDurationElement.textContent.includes(":") && !isNaN(audioPlayer.duration)) {
      //     const totalMinutes = Math.floor(audioPlayer.duration / 60);
      //     const totalSeconds = Math.floor(audioPlayer.duration % 60);
      //     totalDurationElement.textContent = `${totalMinutes}:${totalSeconds.toString().padStart(2, "0")}`;
      // }
  });

  progressBars.forEach(bar => bar.addEventListener("click", (e) => {
      if (!audioPlayer.duration) return;  //  audio is not loaded yet, so the function exits early;

      const progressBarWidth = bar.clientWidth;
      const clickX = e.offsetX;
      audioPlayer.currentTime = (clickX / progressBarWidth) * audioPlayer.duration;

  }));


  function updateSongHighlight(element) {
      if (currentSongElement) {
          currentSongElement.innerHTML = "▶";
      }
      element.innerHTML = "❚❚";
  }

  audioPlayer.addEventListener("ended", () => {
    playPauseButtons.forEach(btn => btn.innerHTML = "▶"); // Change back to play icon when song ends
    if (currentSongElement) {
        currentSongElement.innerHTML = "▶"; // Reset the song element icon
    }
});

  const prevButtons = document.querySelectorAll('.skip-back');
  const nextButtons = document.querySelectorAll('.skip-forward');

  prevButtons.forEach(btn => btn.addEventListener("click", () => {
      audioPlayer.currentTime = Math.max(0, audioPlayer.currentTime - 10); // Go back 10 seconds
  }));

  nextButtons.forEach(btn => btn.addEventListener("click", () => {
      audioPlayer.currentTime = Math.min(audioPlayer.duration, audioPlayer.currentTime + 10); // Skip forward 10 seconds
  }));

