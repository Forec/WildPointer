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
		console.log("不存在对应文章");
		rollback();
	}
	else if (response.code == 0) {
		console.log("不能给自己点赞");
		rollback();
	}
	else if (response.code == 1) {
		jQuery("#like-it-counter").text(response.count);
		jQuery("#liked").val("not_like_it");
	}
	else if (response.code == 2) {
		console.log("未知错误");
		rollback();
	} else {
	    rollback();
	}
}

function thumbUpFailed(error) {
	console.log("服务器连接失败");
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
		console.log("不存在对应文章");
		rollback();
	}
	else if (response.code == 0) {
		console.log("不能给自己取消赞");
		rollback();
	}
	else if (response.code == 1) {
		jQuery("#like-it-counter").text(response.count);
		jQuery("#liked").val("like_it");
	}
	else if (response.code == 2) {
		console.log("未知错误");
		rollback();
	} else {
	    rollback();
	}
}

function thumbDownFailed(error) {
	console.log("服务器连接失败");
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
	} else if (liked.val() == "not_like_it") {
		likeNum++;
		likeButton.html(likeNum);
		likeButton.removeClass("like-it").addClass("dislike-it");
	}
}
