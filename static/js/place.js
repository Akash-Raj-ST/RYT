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
        spot.style.backgroundColor = "#DFA7CC";
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
        rev.style.backgroundColor = "#DFA7CC";
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