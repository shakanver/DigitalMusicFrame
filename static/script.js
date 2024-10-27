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
                console.log(data)
            })
            .catch(error => console.error('Error fetching song data:', error)); //TODO: figure out why this isn't handling 500 errors
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