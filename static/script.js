document.addEventListener("DOMContentLoaded", function()
{
    fetchSongData();
    setInterval(fetchSongData, 1000);

    function fetchSongData()
    {
        fetch('http://localhost:3001/currenttrack')
            .then(response =>
            {
                if (!response.ok)
                {
                    throw new Error(response.statusText)
                }
                return response.json()
            })
            .then(data =>
            {
                updateUI(data)
            })
            .catch(error => console.error('Error fetching song data:', error));
    }

    function updateUI(data)
    {
        var currentTrackContent = data.item;
        var currentlyPlayingType = data.currently_playing_type;
        if (currentTrackContent === null)
        {
            console.log("here");
            console.log('No track is currently playing');
            setAlbumArtAndText("static/assets/spotify.png");
        } else if (currentlyPlayingType === 'track')
        {
            genColourPaletteFromAlbumArtUrl(currentTrackContent.album.images[0].url)
            setAlbumArtAndText(currentTrackContent.album.images[0].url, currentTrackContent.name, currentTrackContent.artists[0].name, currentTrackContent.album.name, true);
        } else if (currentlyPlayingType === 'episode')
        {
            genColourPaletteFromAlbumArtUrl(currentTrackContent.album.images[0].url)
            setAlbumArtAndText(currentTrackContent.album.images[0].url, currentTrackContent.name, true);
        } else
        {
            setAlbumArtAndText("static/assets/spotify.png");
        }
    }

    function genColourPaletteFromAlbumArtUrl(albumArtUrl)
    {
        const url = `http://localhost:3001/colourpalette?albumArtUrl=${albumArtUrl}`

        const options =
        {
            method: "POST",
            headers:
            {
                "Content-Type": "application/json"
            }
        }

        fetch(url, options)
            .then(response => {
                if (!response.ok) {
                    throw new Error(response.statusText);
                }
                return response.json();
            })
            .then(data => {
                console.log(data);
            })
            .catch(error => {
                console.error("Error:", error);
            });
    }

    function setAlbumArtAndText(albumArtPath="", title = "", subtitle = "", secondSubtitle = "", addColourPalette = false)
    {
        console.log(albumArtPath);
        document.getElementById('albumArt').src = albumArtPath;
        document.getElementById('title').textContent = title.toUpperCase();
        document.getElementById('subtitle').textContent = subtitle.toUpperCase();
        document.getElementById('secondsubtitle').textContent = secondSubtitle.toUpperCase();

        if (addColourPalette)
        {
            document.getElementById('colourPalette').src = 'static/assets/palette.png';
        }
    }
});