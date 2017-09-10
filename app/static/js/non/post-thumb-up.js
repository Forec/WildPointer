function thumbUp(url_string) {
	$.ajax({
		url: url_string,
		type: "GET",
		success: thumbUpSuccess,
		err: thumbUpFailed
	});
}

function thumbUpSuccess(response) {
	if (response.code == -1) {
		flash_error("您点赞的文章不存在。");
		rollback();
	}
	else if (response.code == 0) {
		flash_info("您不能给自己发布的文章点赞。");
		rollback();
	}
	else if (response.code == 1) {
		jQuery("#like-it-counter").text(response.count);
        jQuery("#static-like-count").text(response.count);
		jQuery("#liked").val("cancel_like_it");
	}
	else {
		flash_error("您对此操作无权限，请确认您已经登录并激活了账号。");
		rollback();
	}
}

function thumbUpFailed(error) {
	flash_error("无法连接至服务器，请检查您的网络配置。");
	rollback();
}	

function thumbDown(url_string) {
	$.ajax({
		url: url_string,
		type: "GET",
		success: thumbDownSuccess,
		err: thumbDownFailed
	});
}

function thumbDownSuccess(response) {
	if (response.code == -1) {
		flash_error("您取消点赞的文章不存在。");
		rollback();
	}
	else if (response.code == 0) {
		flash_info("您不能给自己发布的文章点赞或取消点赞。");
		rollback();
	}
	else if (response.code == 1) {
		jQuery("#like-it-counter").text(response.count);
        jQuery("#static-like-count").text(response.count);
		jQuery("#liked").val("like_it");
	}
	else if (response.code == 2) {
		flash_error("您对此操作无权限，请确认您已经登录并激活了账号。");
		rollback();
	}
}

function thumbDownFailed(error) {
	flash_error("无法连接至服务器，请检查您的网络配置");
	rollback();
}

function rollback() {
	var counter = jQuery("#like-it-counter");
	var likeButton = jQuery("#like-it-counter");
	var likeHtml = counter.html();
	var likeNum = parseInt(likeHtml, 10);
	var liked = jQuery("#liked");
	
	if (liked.val() == "like_it") {
		likeNum--;
		likeButton.html(likeNum);
		likeButton.removeClass("dislike-it").addClass("like-it");
	} else if (liked.val() == "cancel_like_it") {
		likeNum++;
		likeButton.html(likeNum);
		likeButton.removeClass("like-it").addClass("dislike-it");
	}
}
