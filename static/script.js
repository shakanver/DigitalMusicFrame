document.addEventListener("DOMContentLoaded", function()
{
    fetchSongData();
    setInterval(fetchSongData, 1000);

    function fetchSongData()
    {
        fetch('http://localhost:3001/currenttrack')
            .then(response => response.json())
            .then(data =>
            {
                console.log("this is the data: \n" + data)
                var dataAsJson = JSON.parse(data)
                console.log(dataAsJson);
                updateUI(dataAsJson);
            })
            .catch(error => console.error('Error fetching song data:', error));
    }

    function updateUI(data)
    {
        var currentTrackContent = data.item;
        if (currentTrackContent === null)
        {
            console.log('No track is currently playing');
            setAlbumArtAndText("assets/spotify.png");
        }
        // if (data.cu)
        // {
        //     [albumArtPath, title, subtitle, secondSubtitle] = getTrackInfo(currentTrackContent);
            
        // }
    }

    function setAlbumArtAndText(albumArtPath, title = "", subtitle = "", secondSubtitle = "")
    {
        document.getElementById('albumArt').src = albumArtPath;
        document.getElementById('title').textContent = title;
        document.getElementById('artist').textContent = subtitle;
        document.getElementById('album').textContent = secondSubtitle;
    }

    function getTrackInfo(currentTrackContent)
    {

    }
});