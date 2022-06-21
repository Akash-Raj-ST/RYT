// s=[];

// for(k=0;k<posts.length;k++){
    //     s.push(0);
// }

// // e -> points to the required html
// // n -> -1 or 1 depending on forward or backward
// // l -> holds the id of the post

// function show_slide(e,n){
    //     hide(e);
    //     img = e.parentNode.parentNode.parentNode.getElementsByClassName("post_pic");
    //     cir = e.parentNode.parentNode.parentNode.getElementsByClassName("circle");
    //     var img_pos = e.parentNode.getAttribute("#id");
    //     console.log(img_pos);
    
    //     if(s[l]==img.length){
        //         s[l] = 0;
        //     }
        //     if(s[l]==-1){
            //         s[l] = img.length-1;
            //     }
            //     console.log(img[s[l]]);
            //     img[s[l]].style.display = "block";
            //     cir[s[l]].style.backgroundColor = "var(--pri_col)";
            // }
            
            // function hide(e){
                //     img = e.parentNode.parentNode.parentNode.getElementsByClassName("post_pic");
                //     cir = e.parentNode.parentNode.parentNode.getElementsByClassName("circle");
                //     for(i=0;i<img.length;i++){
                    //         img[i].style.display="none";
                    //         cir[i].style.backgroundColor = "transparent";
                    //     }
                    // }
                    
                    
posts = document.getElementsByClassName("nav_b");

function show_slide(e,n){
    var img_pos = e.parentNode.parentNode.querySelector(".nav_b");
    var pos = parseInt(img_pos.id)+n;
    
    // 2 parentnode is enough
    img = e.parentNode.parentNode.parentNode.getElementsByClassName("post_pic");
    cir = e.parentNode.parentNode.parentNode.getElementsByClassName("circle");
    
    if(pos>=img.length){
        pos=0
    }else if(pos==-1){
        pos = img.length-1;
    }
    img_pos.id = pos;
    
    hide(e);
    
    img[pos].style.display = "block";
    cir[pos].style.backgroundColor = "var(--pri_col)";
}

function hide(e){
    // 2 parentnode is enough
    img = e.parentNode.parentNode.parentNode.getElementsByClassName("post_pic");
    cir = e.parentNode.parentNode.parentNode.getElementsByClassName("circle");
    for(i=0;i<img.length;i++){
        img[i].style.display="none";
        cir[i].style.backgroundColor = "transparent";
    }
}
    
for(j=0;j<posts.length;j++){
    hide(posts[j]);
    show_slide(posts[j],0);
}