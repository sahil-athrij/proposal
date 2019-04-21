function showprogress() {
    progress = document.getElementById("progressbar");
    progress.hidden = false;
    timeout = progress.content;
    timeout = parseInt(timeout);
    timeout = timeout * 100;
    setInterval(setwidth, timeout)

}

function setwidth() {
    progress = document.getElementById("progress");
    width = progress.style.width;
    width = width.slice(0, -1);
    width = parseInt(width);
    progress.style.width = (width + 10) + "%";

}

