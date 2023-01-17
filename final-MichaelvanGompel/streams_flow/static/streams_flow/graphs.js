var divs = ["default", "half_year", "year", "all_plays" ];
    var id_visibility = null;
    function set_visibility(div_id) {
        if(id_visibility === div_id){
            id_visibility = null;
        } else {
            id_visibility = div_id
        }
        hide_other_objects();
    }
    function hide_other_objects() {
        var i, div_id, div;
        for(i = 0; i < divs.length; i++) {
            div_id = divs[i]
            div = document.getElementById(div_id)
            if(id_visibility === div_id) {
                div.style.display = "block";
            } else {
                div.style.display = "none";
            }
        }
    }