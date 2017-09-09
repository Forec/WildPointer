/*
*显示和隐藏模态对话框
*	参数：
+		modal:	对话框id值
*/
function modalHidden(modalID) {
	var idString = "#" + modalID;
	var modal = jQuery(idString);
    var visibility = modal.css("visibility");
    if (visibility == "visible") {
        modal.css("visibility", "hidden");
    } else {
		modal.css("visibility", "visible");
    }
};