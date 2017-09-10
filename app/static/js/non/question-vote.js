function voteUp(url_string) {
	$.ajax({
		url: url_string,
		type: "GET",
		success: function(response) {
		    if (response.code == 1) {
		        jQuery("#support-counter").text(response.score);
		        jQuery("#static-like-count").text(response.score);
		        flash_success("您的称赞已提交。");
		        clearBackup();
		    } else if (response.code == 0) {
		        flash_info("已取消称赞。");
		        jQuery("#support-counter").text(response.score);
		        jQuery("#static-like-count").text(response.score);
		        clearBackup();
		    } else if (response.code == -1) {
		        flash_error("该问题不存在。");
		        rollbackVote();
		    } else if (response.code == 2) {
		        flash_error("您不能称赞自己的问题。");
		        rollbackVote();
		    } else {
		        flash_error("您没有权限执行此操作，请确认您已经登录并且激活了您的账号。");
		        rollbackVote();
		    }
		},
		err: function(err) {
		    flash_error("无法连接至服务器，请检查您的网络设置。");
		    rollbackVote();
		}
	});
}

function voteDown(url_string) {
	$.ajax({
		url: url_string,
		type: "GET",
		success: function(response) {
		    if (response.code == 1) {
		        jQuery("#support-counter").text(response.score);
		        jQuery("#static-like-count").text(response.score);
		        flash_success("您的反对意见已提交。");
		        clearBackup();
		    } else if (response.code == 0) {
		        jQuery("#support-counter").text(response.score);
		        jQuery("#static-like-count").text(response.score);
		        flash_info("已取消反对。");
		        clearBackup();
		    } else if (response.code == -1) {
		        flash_error("该问题不存在。");
		        rollbackVote();
		    } else if (response.code == 2) {
                flash_error("您不能反对自己的问题。");
                rollbackVote();
		    } else {
		        flash_error("您没有权限执行此操作，请确认您已经登录并且激活了您的账号。");
		        rollbackVote();
		    }
		},
		err: function(err) {
		    flash_error("无法连接至服务器，请检查您的网络设置。");
		    rollbackVote();
		}
	});
}

function backupVote() {
    if (jQuery("#backup_action").val() != "")
        return;
    var backupMsg = jQuery("#support-counter").html() + ";" +
                    jQuery("#like_action").val() + ";" +
                    jQuery("#unlike_action").val() + ";" +
                    jQuery("#like-button").attr("class") + ";" +
                    jQuery("#unlike-button").attr("class");
    jQuery("#backup_action").val(backupMsg);
}

function clearBackup() {
    jQuery("#backup_action").val("");
}

function rollbackVote() {
    var backupMsg = jQuery("#backup_action").val();
	jQuery("#support-counter").html(parseInt(backupMsg.split(";")[0], 10));
	jQuery("#like_action").val(backupMsg.split(";")[1]);
	jQuery("#unlike_action").val(backupMsg.split(";")[2]);
	jQuery("#like-button").attr("class", backupMsg.split(";")[3]);
	jQuery("#unlike-button").attr("class", backupMsg.split(";")[4]);
	jQuery("#backup_action").val("");
}
