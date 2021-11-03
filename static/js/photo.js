function photo_upload(){
    var file = document.querySelector(".file_input")
    file.click();
}

function loadFile(event) {
    var output = document.getElementById('upload_pic');
    output.src = URL.createObjectURL(event.target.files[0]);
    output.onload = function() {
        URL.revokeObjectURL(output.src) // free memory
        console.log("memory free");
    }
}

function make_id() {
    const length = 5;
    var result           = '';
    var characters       = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz';
    var charactersLength = characters.length;
    for ( var i = 0; i < length; i++ ) {
      result += characters.charAt(Math.floor(Math.random() * charactersLength));
   }
   return result;
}

function gen_random_dp(){
    var random_str = make_id();
    var url = "https://avatars.dicebear.com/api/avataaars/tour"+random_str+".svg";
    var dp = document.querySelector("#upload_pic");
    dp.src = url;
    
    //add it to input field
    var input_url = document.querySelector(".file_url")
    input_url.value = url;

    //remove uploaded file from input type:file
    var input_file = document.querySelector(".file_input")
    input_file.value = input_file.defaultValue;
}