function create_spot(spot){
    // format
    // <div onclick="location">
    //     <img src="place_img"/>
    //     <h3>place_name</h3>
    // </div>

    const spot_ele = document.querySelector(".search_spots")
    spot_ele.innerHTML = "";
    for(i=0;i<spot.length;i++){ 
        var div = document.createElement('div');
        div.setAttribute("onclick","window.location='/places/"+spot[i]['place_id']+"/';")
        div.setAttribute("class","place_container pointer")

        var img = document.createElement('img');
        img.src = spot[i]["place_img"];
        img.setAttribute("class","place_img")

        var h3 = document.createElement('h3');
        h3.innerHTML = spot[i]["place_name"];
        h3.setAttribute("class","place_name")

        div.appendChild(img);
        div.appendChild(h3);
        spot_ele.appendChild(div);
    }
}

function create_profile(spot){
    // format
    // <div onclick="location">
    //     <img src="profile_img"/>
    //     <h3>profile_name</h3>
    // </div>

    const profile_ele = document.querySelector(".search_users")
    profile_ele.innerHTML = "";
    for(i=0;i<spot.length;i++){ 
        var div = document.createElement('div');
        div.setAttribute("onclick","window.location='/profile/"+spot[i]['profile_id']+"';")
        div.setAttribute("class","place_container profile_container pointer")

        var img = document.createElement('img');
        img.src = spot[i]["profile_img"];
        img.setAttribute("class","place_img")

        var h3 = document.createElement('h3');
        h3.innerHTML = spot[i]["profile_name"];
        h3.setAttribute("class","place_name")

        div.appendChild(img);
        div.appendChild(h3);
        profile_ele.appendChild(div);
    }
}

function req(query){
    var myHeaders = new Headers();

    var requestOptions = {
        method: 'GET',
        headers: myHeaders,
        redirect: 'follow'
    };

    fetch("https://review-yt.herokuapp.com/api/search?q="+query, requestOptions)
    .then(function(response) {
        return response.json();
    }).then(function(data) {
            // console.log(data);
            var spots_button = document.querySelector(".search_spots_button")
            var users_button = document.querySelector(".search_users_button")

            spots_button.innerHTML = "Spots ("+data["spots"].length+")";
            users_button.innerHTML = "Users ("+data["profile"].length+")";

            create_spot(data["spots"]);  
            create_profile(data["profile"]);   
        })

    
}

function get_results(){
    window.scrollTo(0,0);
    var q = document.querySelector("#search").value;
    var page = document.querySelector(".search_res");
    var body_hide = document.querySelector(".search_hide");
    //transparent disable in header
    var header = document.querySelector(".header");
    if(q.length>0){
        page.style.display = "block";
        body_hide.style.display = "none";
        header.style.backgroundColor = "var(--sec_col)";
        req(q);
    }else{
        page.style.display = "none";
        body_hide.style.display = "flex";
        header.style.backgroundColor = "var(--sec_col_light)";
    }
}

function show(n){
    console.log("showing")
    var spots_button = document.querySelector(".search_spots_button")
    var users_button = document.querySelector(".search_users_button")

    var spots = document.querySelector(".search_spots")
    var users = document.querySelector(".search_users")

    if(n==1){
        spots_button.style.borderBottom = "5px solid var(--white)";
        users_button.style.borderBottom = "none";

        spots.style.display = "flex";
        users.style.display = "none";

    }else{
        spots_button.style.borderBottom = "none";
        users_button.style.borderBottom = "5px solid var(--white)";

        spots.style.display = "none";
        users.style.display = "flex";
    }
}