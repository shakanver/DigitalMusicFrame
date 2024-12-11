//pixel dims for testing: 	Width: 3897 pixels Height: 6732 pixels
document.addEventListener("DOMContentLoaded", function()
{
    fetchSongData();
    setInterval(fetchSongData, 1000);

    function fetchSongData()
    {
        fetch('http://localhost:3001/queue')
            .then(response =>
            {
                if (!response.ok)
                {
                    throw new Error(response.statusText)
                }
                return response.json();
            })
            .then(data =>
            {
                updateUI(data);
            })
            .catch(error => console.error('Error fetching song data:', error));
    }

    function updateUI(data)
    {
        var currentTrackContent = data.currently_playing;
        var queue = data.queue
        console.log(data)
        console.log(currentTrackContent);
        if (currentTrackContent === null || currentTrackContent === undefined)
        {
            console.log('No track is currently playing');
            setAlbumArtAndText("static/assets/spotify.png");
        } else
        {
            genColourPaletteFromAlbumArtUrl(currentTrackContent.album.images[0].url);
            setAlbumArtAndText(currentTrackContent.album.images[0].url, currentTrackContent.name, currentTrackContent.artists[0].name, currentTrackContent.album.name, true);
        }

        if (queue !== null && queue !== undefined)
        {
            showQueue(queue);
        }
    }

    function showQueue(queue)
    {
        var tracksNamesInQueue =  queue.map(track => track.name).slice(0, 5);
        document.getElementById('track-queue').innerHTML = '';
        const trackListElement = document.getElementById('track-queue');
        tracksNamesInQueue.forEach( track => {
            const li = document.createElement('li');
            li.textContent = track;
            trackListElement.appendChild(li);
        });

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
        if (addColourPalette)
        {
            url = 'static/assets/palette.png'
            fetch(url, {cache: 'reload', mode: 'no-cors'})
                .then(response =>
                {
                    if (!response.ok)
                    {
                        throw new Error(response.statusText);
                    }
                })
                .then(data => 
                {
                    console.log(data);
                    document.getElementById('colourPalette').src = url;
                })
                .catch(error => {
                    console.error("Error:", error);
                });
        } else
        {
            document.getElementById('colourPalette').src = "";
        }

        document.getElementById('albumArt').src = albumArtPath;
        document.getElementById('title').textContent = title.toUpperCase();
        document.getElementById('subtitle').textContent = subtitle.toUpperCase();
        document.getElementById('secondsubtitle').textContent = secondSubtitle.toUpperCase();
    }
});