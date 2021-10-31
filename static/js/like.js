function like_click(e,r_id,u_id){

    var myHeaders = new Headers();

    var formdata = new FormData();
    formdata.append("user_id", u_id);
    console.log("user_id: ",u_id)
    var requestOptions = {
    method: 'POST',
    headers: myHeaders,
    body: formdata,
    redirect: 'follow'
    };

    fetch("http://127.0.0.1:8000/api/like/"+r_id, requestOptions)
    .then(function(response) {
        return response.json();
    }).then(function(data) {
        console.log(data);
        var l = e.parentNode.querySelector(".tot_likes");
        l.innerHTML = data["likes"];
        // update like of other elements too
    })
    
    var like = e.parentNode.querySelector('.like_img');
    
    var main_like = document.querySelector(".main_like");
    if(like.id == "not_liked"){
        like.src = "/static/img/heart_fill.png";
        like.id = "liked";
        main_like.innerHTML = parseInt(main_like.innerHTML)+1;
    }else{
        like.id = "not_liked";
        like.src = "/static/img/heart_line.png";
        main_like.innerHTML = parseInt(main_like.innerHTML)-1;
    }
}