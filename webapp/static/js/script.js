// Grab elements, create settings, etc.
var video = document.getElementById('video');

// Get access to the camera!
if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
    // Not adding `{ audio: true }` since we only want video now
    navigator.mediaDevices.getUserMedia({ video: true }).then(function(stream) {
        video.src = window.URL.createObjectURL(stream);
        video.play();
    });
}

// Trigger photo take
document.getElementById("snap-button").addEventListener("click", function() {
    if ($("#instructions span").attr("state") == "step1") {
        var canvas = document.createElement('canvas');
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        var context = canvas.getContext('2d');
        context.drawImage(video, 0, 0, video.videoWidth, video.videoHeight);
        document.getElementById("snap1").value = canvas.toDataURL("image/png")
        $('#video').delay(100).fadeOut().fadeIn('slow');
        $("#instructions span").attr("state", "step2")
        $("#instructions span").html("<strong>Step 2</strong>: take a pic of the label")
    } else if ($("#instructions span").attr("state") == "step2") {
        var canvas = document.createElement('canvas');
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        var context = canvas.getContext('2d');
        context.drawImage(video, 0, 0, video.videoWidth, video.videoHeight);
        document.getElementById("snap2").value = canvas.toDataURL("image/png");
        $('#video').delay(100).fadeOut().fadeIn('slow');
        document.getElementById("form-save").submit();
    }
});

$(document).ready(function(){
    // the "href" attribute of .modal-trigger must specify the modal ID that wants to be triggered
    $('.modal').modal();
});
