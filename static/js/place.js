function rev_spot(e,n){
    const ele = e.parentNode;
    const post = document.querySelector(".all_post");

    var rev = ele.querySelector(".rev");
    var spot = ele.querySelector(".spot");
    var sub_place = document.querySelector(".sub_place_container");
    var review = document.querySelector(".all_post");
    if(n==2){
        console.log("clicked spot");
        console.log("sub_place: ",sub_place);
        spot.style.backgroundColor = "var(--light_pink)";
        spot.style.textDecoration = "underline";

        rev.style.backgroundColor = "white";
        rev.style.textDecoration = "none"; 
        
        if(post.style.display="flex"){
            post.style.display="none";
        }

        sub_place.style.display = "block";
        review.style.display = "none";
    }

    else{
        console.log("clicked Review");
        rev.style.backgroundColor = "var(--light_pink)";
        rev.style.textDecoration = "underline";

        spot.style.backgroundColor = "white";
        spot.style.textDecoration = "none"; 
         
        if(post.style.display="none"){
            post.style.display="flex";
        }

        sub_place.style.display = "none";
        review.style.display = "flex";
    }
}

function filter(e){  
    // remove other filters bg first
    var filters = e.parentNode.querySelectorAll(".filter");
    for(i=0;i<filters.length;i++){
        filters[i].style.backgroundColor="var(--light_pink)";
    }
    e.style.backgroundColor = "#EC6969";

    // manage subplace
    var all_subplaces = document.querySelectorAll(".sub_place");
    if(e.innerHTML.toLowerCase()=="all"){ //show all subplaces
        for(i=0;i<all_subplaces.length;i++){
            all_subplaces[i].style.display = "grid";
        }
    }
    else{
        var real_type = e.innerHTML.toLowerCase();
        for(i=0;i<all_subplaces.length;i++){
            var ori_type = all_subplaces[i].getAttribute("id").toLowerCase();
            if(ori_type==real_type)
                all_subplaces[i].style.display = "grid";
            else
                all_subplaces[i].style.display = "none";
        }
    }
}