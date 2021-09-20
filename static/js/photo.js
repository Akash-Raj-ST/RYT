function photo_upload(){
    var file = document.querySelector(".file_input")
    file.click();
}

function loadFile(event) {
    var output = document.getElementById('upload_pic');
    output.src = URL.createObjectURL(event.target.files[0]);
    output.onload = function() {
        URL.revokeObjectURL(output.src) // free memory
    }
}