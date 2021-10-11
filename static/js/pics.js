s=[];

posts = document.getElementsByClassName("nav_b");
for(k=0;k<posts.length;k++){
    s.push(0);
}

// e -> points to the required html
// n -> -1 or 1 depending on forward or backward
// l -> holds the id of the post

function show_slide(e,n,l){
    hide(e);
    img = e.parentNode.parentNode.parentNode.getElementsByClassName("post_pic");
    cir = e.parentNode.parentNode.parentNode.getElementsByClassName("circle");
    s[l]+=n;

    if(s[l]==img.length){
        s[l] = 0;
    }
    if(s[l]==-1){
        s[l] = img.length-1;
    }
    console.log(img[s[l]]);
    img[s[l]].style.display = "block";
    cir[s[l]].style.backgroundColor = "var(--pri_col)";
}

function hide(e){
    img = e.parentNode.parentNode.parentNode.getElementsByClassName("post_pic");
    cir = e.parentNode.parentNode.parentNode.getElementsByClassName("circle");
    for(i=0;i<img.length;i++){
        img[i].style.display="none";
        cir[i].style.backgroundColor = "transparent";
    }
}

for(j=0;j<posts.length;j++){
    console.log(posts[j]);
    hide(posts[j]);
    show_slide(posts[j],0,0);
}





