function modalHidden(id){
    var e = jQuery(id).css("visibility");
    if (e == "visible") {
         jQuery(id").css("visibility", "hidden");
    } else {
         jQuery(id).css("visibility", "visible");
    }
};