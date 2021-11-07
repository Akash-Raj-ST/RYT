function focus_rev(n) {
    const my_rev = document.querySelector(".my_rev");
    const like_rev = document.querySelector(".like_rev");

    var all_my_rev = document.querySelector(".all_my_review");
    var all_like_rev = document.querySelector(".all_like_review");
    
    if(n==1){
        my_rev.style.backgroundColor ="var(--sec_col)" ;
        like_rev.style.backgroundColor ="#A3C1E4" ;

        all_my_rev.style.display = "flex";
        all_like_rev.style.display = "none";

    }else{
        my_rev.style.backgroundColor = "#A3C1E4";
        like_rev.style.backgroundColor ="var(--sec_col)" ;

        all_like_rev.style.display = "flex";
        all_my_rev.style.display = "none";
    }
}