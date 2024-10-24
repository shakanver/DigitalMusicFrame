document.addEventListener("DOMContentLoaded", function() {
    fetchSongData();
    setInterval(fetchSongData, 1000);

    function fetchSongData() {
        fetch('http://localhost:3001/currenttrack')
            .then(response => response.json())
            .then(data => {
                updateUI(data);
            })
            .catch(error => console.error('Error fetching song data:', error));
    }

    function updateUI(data) {
        document.getElementById('albumArt').src = data.albumArtUrl;
        document.getElementById('title').textContent = data.title;
        document.getElementById('artist').textContent = data.artist;
        document.getElementById('album').textContent = data.album;
    }
});