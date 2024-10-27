document.addEventListener("DOMContentLoaded", function()
{
    fetchSongData();
    setInterval(fetchSongData, 1000);

    function fetchSongData()
    {
        fetch('http://localhost:3001/currenttrack')
            .then(response =>
            {
                return response.json()
            })
            .then(data =>
            {
                updateUI(data)
            })
            .catch(error => console.error('Error fetching song data:', error)); //TODO: figure out why this isn't handling 500 errors
    }

    function updateUI(data)
    {
        var currentTrackContent = data.item;
        var currentlyPlayingType = data.currently_playing_type;
        if (currentTrackContent === null)
        {
            console.log('No track is currently playing');
            setAlbumArtAndText("assets/spotify.png");
        } else if (currentlyPlayingType === 'track')
        {
            setAlbumArtAndText(currentTrackContent.album.images[0].url, currentTrackContent.name, currentTrackContent.artists[0].name, currentTrackContent.album.name);
        } else if (currentlyPlayingType === 'episode')
        {
            setAlbumArtAndText(currentTrackContent.album.images[0].url, currentTrackContent.name);
        } else
        {
            setAlbumArtAndText("assets/spotify.png");
        }
    }

    function setAlbumArtAndText(albumArtPath="", title = "", subtitle = "", secondSubtitle = "")
    {
        document.getElementById('albumArt').src = albumArtPath;
        document.getElementById('title').textContent = title;
        document.getElementById('subtitle').textContent = subtitle;
        document.getElementById('secondsubtitle').textContent = secondSubtitle;
    }
});