function enableModifyProfile(username) {
	var inputNickName = jQuery("#user-profile-dialog-nickname");
	var inputAddress = jQuery("#user-profile-dialog-address");
	var inputHomepage = jQuery("#user-profile-dialog-homepage");
	var inputAboutme = jQuery("#user-profile-dialog-aboutme");
	var inputContact = jQuery("#user-profile-dialog-email");
	var btn = jQuery("#hp-modify");

	if (btn.text() == "修改") {
		inputNickName.attr("readonly", false);	
		inputAddress.attr("readonly", false);	
		inputHomepage.attr("readonly", false);	
		inputAboutme.attr("readonly", false);
		inputContact.attr("readonly", false);
		inputNickName.css("background-color", "white");	
		inputAddress.css("background-color", "white");
		inputHomepage.css("background-color", "white");
		inputAboutme.css("background-color", "white");
		inputContact.css("background-color", "white");
		btn.attr("onclick", "submit_profile_change('" + username + "')");
		btn.text("提交");
	} else {
		inputNickName.attr("readonly", true);	
		inputAddress.attr("readonly", true);	
		inputHomepage.attr("readonly", true);	
		inputAboutme.attr("readonly", true);
		inputContact.attr("readonly", false);
		inputNickName.css("background-color", "#f2f2f2");	
		inputAddress.css("background-color", "#f2f2f2");
		inputHomepage.css("background-color", "#f2f2f2");
		inputAboutme.css("background-color", "#f2f2f2");
		inputContact.css("background-color", "#f2f2f2");
		btn.attr("onclick", "enableModifyProfile('" + username + "')");
		btn.text("修改");
	}

}