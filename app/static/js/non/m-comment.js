var commentPage = new CommentPage();

jQuery(document).ready(function() {
	//页面加载成功后加载评论
	setTimeout(commentPage.init, 1000);
	
	//加载更多评论
	jQuery("#load-comment-button").click(function() {
		commentPage.loadMore();
	});
	
	//绑定滚动事件，如果到达顶部，收起多余的评论
	$(window).bind('scroll', function(){    			
        if($(document).scrollTop() == 0){
            commentPage.packUp();
        }
    });
});


//=======================================================================
//
//	html模板
//
//=======================================================================

//评论
var COMMENT_TEMPLATE = fromText(function(){/*
	<li class="comment even thread-odd thread-alt depth-1" id="comment-li-{{id}}">
        <article id="comment-article-{{id}}" style="padding-bottom: 0px;">
			<a href="{{author-url}}">
                <img alt="" src="{{head-url}}" class="avatar avatar-60 photo" height="60" width="60">
            </a>

            <div class="comment-meta">
                <h5 class="author">
                    <cite class="fn"><a href="{{author-url}}" rel="external nofollow" class="url">{{author-name}}</a></cite>
                </h5>

                <p class="date">
					<a href="javascript:void(0)">
                        <time datetime="{{datatime-value}}">{{datetime-text}}</time>                                                                                
					</a>
                </p>

            </div>

            <div class="comment-body">
				{{comment-body}}
            </div><!-- end of comment-body -->
			
			<div class="reply-head">
				<label class="reply-label">
					<a class="reply-btn" style="font-size: 10px; background-color: #;" id="reply-btn-{{id}}" href="javascript:void(0)" onclick="showreply(this.id)" value="show" style="font-size: 10px;">
						Reply
					</a>
				</label>
			</div>	
			<div class="replys-body" id="reply-div-{{id}}" style="display: none; border:1px solid #e2e2e2; background-color: #f2f2f2; font-size: 8px;">
				<div name="replies-container">
					<ul class="children" style="padding-left: 40px; margin-left: 0px; padding-left: 30px; border-bottom:1px solid #e2e2e2;">
						{{reply}}
				    </ul>
				</div>
				<div class="page-number" id="page-line-{{id}}">
				
				</div>
				<table style="width: 100%; background-color: #f2f2f2;">
					<tr>
						<td style="width: 90%; background-color: #f2f2f2;">
							<div style="padding-left: 30px; padding-right: 30px;">
								<textarea class="span8" id="reply-input-{{id}}" cols="90" rows="10" style="height: 40px; width: 98%; resize:none; padding-top: 0px;" placeholder="say something"></textarea>
							</div>
						</td>
						<td style="width: 10%; padding-top: 5px; padding-bottom: 5px; background-color: #f2f2f2;">
							<button class="btn btn-primary" id="reply-send-{{id}}" style="height: 25px; line-height: 2px; font-size: 10px; margin-bottom: 10px;" onclick="reply(this.id)">发送</button>
						</td>							
					</tr>
				</table>
			</div>
		</article>
    </li>
*/});

//回复
var REPLY_TEMPLAE = fromText(function(){/*
		<li class="comment byuser comment-author-saqib-sarwar bypostauthor odd alt depth-2 reply-block" id="reply-li-{{cid}}-{{id}}" style="margin-top: 0px; padding-top: 5px;">
			<article style="padding-bottom: 5px;" id="reply-artical-{{cid}}-{{id}}">
				<a href="{{author-url}}">
					<img alt="" src="{{head-url}}" class="avatar avatar-60 photo" height="30" width="30">
				</a>

				<div class="comment-meta">
					<h5 class="author" style="font-size: 10px;">
						<cite class="fn"><a href="{{author-url}}" rel="external nofollow" class="url">{{author-id}}</a></cite>
						<time datetime="{{datatime-value}}">{{datetime-text}}</time>  
					</h5>
				</div>

				<div class="comment-body">
					<p style="margin-bottom: 0px;">{{reply-content}}</p>
				</div>
			</article>
        </li>
*/});

//页码
var PAGE_CURRENT = '<a class="page-current">{{page-num}}</span>';
var PAGE_NORM = '<a href="javascript:void(0)" name="{{id}}" onclick="switchPage(this.name, this.text)">{{page-num}}</a>';
var PAGE_SWITCH_DISABLE = '<a class="switch-disabled">{{arrow}}</span>';
var PAGE_SWITCH = '<a class="page-switch-btn" name="{{id}}" href="javascript:void(0)" onclick="switchPage(this.name, this.text)">{{arrow}}</a>';


//=======================================================================
//
//	常量
//
//=======================================================================

//参数
//var MAX_PAGE_BUTTON		= 4;	//显示页码时最多显示几个按钮
var MAX_REPLY_PAGE		= 5;		//楼中楼每页回复数量
var MAX_COMMENT_PAGE	= 10;		//每次加载的评论数

//字符串常量
	//标签id
	var COMMENT_LI_ID = "comment-li-";
	var COMMENT_ARTICLE_ID = "comment-artical-";
	var REPLY_BTN_ID = "reply-btn-";
	var REPLY_DIV_ID = "reply-div-";
	var PAGE_LINE_ID = "page-line-";
	var REPLY_INPUT_ID = "reply-input-";	
	var REPLY_SEND_ID = "reply-send-";	
		
	var REPLY_LI_ID = "reply-li-";
	var REPLY_ARTICAL_ID = "reply-artical-";

//=======================================================================
//
//	类定义
//
//=======================================================================

function CommentPage() {													//评论容器类
//member: 
	var mHTMLContainerID = "#comments-container";	
	this.mComments = new Array();											//存储评论信息
	this.currentShow = 0;													//存储当前显示的评论数

	var commentsInference = this.mComments;									//引用
	var currShowInf		  = this.currentShow;								//
	
//public function:	
	//打开页面时调用，载入初始评论
	this.init = function() {	
		console.log("comment init");
		var urlstr = "";

		$.ajax({
			url: urlstr,
			type: "POST",
			//data: {},
			success: loadCommentSuccess,
			err: loadCommentFailed
		});	
	};
			
	//点击按钮时调用，载入新的评论
	this.loadMore = function() {							
		var urlstr = "";
 	    
		$.ajax({
			url: urlstr,
			type: "POST",
			//data: {},
			success: loadCommentSuccess,
			err: loadCommentFailed
		});	
	};
		
	//回到顶部时收起多余评论
	this.packUp = function() {
		console.log(currentShow);
		if (currentShow <= 10) {
			return;
		}
		this.currentShow = 10;
		var html = "";
		for (var index = 0; index < MAX_COMMENT_PAGE; index++) {
			html += this.mComments[index].template();
		}
		setHTML(html);
	};
		
//private function:
	function setHTML(html) {
		var container = jQuery(mHTMLContainerID);
		container.html(html);
	}
		
	//显示更多回复
	function appendHTML(html) {
		var container = jQuery(mHTMLContainerID);
		container.html(container.html() + html);
	}
	
	//载入评论成功时调用
	function loadCommentSuccess(response) {	
		var html = "";
		var comment;
		var reply;
		var start = commentsInference.length;

		
		for (var commentIndex = start; commentIndex < start + MAX_COMMENT_PAGE; ++commentIndex) {
			comment = new Comment(commentIndex, t_head_url, t_author_id, t_author_url, t_datetime_text, t_content);
			
			for (var replyIndex = 0; replyIndex < 10; ++replyIndex) {	//一开始先获取现有的所有回复
				reply = new Reply(commentIndex, replyIndex, t_r_head_url, t_r_author_id + replyIndex, t_r_author_url, t_datetime_text, t_reply_content);
				comment.mReplyPage.addReply(reply);
			}
			currShowInf++;
			commentsInference.push(comment);
			html += comment.template();
		}
		appendHTML(html);
	};
	
	//载入评论失败时调用
	function loadCommentFailed(error) {
		console.log("failed");
	};
};

function Comment(index, headUrl, userName, homepageUrl, date, content) {	//评论类
//member:
	this.mIndex 		= index;											//索引值
	this.mHeadUrl 		= headUrl;											//头像url
	this.mUsername 		= userName;											//用户昵称
	this.mHomepageUrl 	= homepageUrl;										//用户链接(可选)
	this.mDate 			= date;												//评论日期
	this.mContent		= content;											//评论内容	
	
	this.mReplyPage 	= new ReplyPage();									//评论中的回复
	var replyPageInference = this.mReplyPage;								//私有函数用这个
	
//public function:
	//显示回复
	this.showReplyPage = function() {
		this.mReplyPage.freshHTML(this.mIndex);
		this.mReplyPage.freshPageHTML(this.mIndex);
	};
	
	//收起回复
	this.hideReplyPage = function() {
		var replyBody = jQuery(REPLY_DIV_ID + this.mIndex).children('ul');
		replyBody.html("");
	};
	
	//生成html
	this.template = function() {
		return COMMENT_TEMPLATE.replace(/{{id}}/g, this.mIndex)
								  .replace(/{{author-url}}/g, this.mHomepageUrl)
								  .replace("{{head-url}}", this.mHeadUrl)
								  .replace("{{author-name}}", this.mUsername)
								  .replace("{{datetime-value}}", this.mDate)
								  .replace("{{datetime-text}}", this.mDate)
								  .replace("{{comment-body}}", this.mContent);
	};
	
	this.reply = function() {
		var inputbox = jQuery("#" + REPLY_INPUT_ID + this.mIndex);
		console.log("reply: " + inputbox.val());
		if (inputbox.val() == undefined || inputbox.val() == "") {
			return;
		}
		
		//	ajax
		
		replySuccess();
	}
//private function	
	function replySuccess(response) {
		replyPageInference
	}
	//eplySuccess.call(this);
	
	function replyFailed(error) {
		
	}
}

function ReplyPage() {														//回复页
//member:
	this.mReplyArray = new Array();											//回复容器
	this.mCurrentPage = 1;													//当前页码
	this.mTotalPage = 0;													//总页数
	
//public function:
	//显示回复
	this.freshHTML = function(id) {
		var replyBody = jQuery("#" + REPLY_DIV_ID + id).children('div[name="replies-container"]').children('ul');
	    var html = "";
		
		if (this.mTotalPage == 0) {
			html="暂时还没有评论";
		} else {
			var start = (this.mCurrentPage - 1) * MAX_REPLY_PAGE;
			var end = start + MAX_REPLY_PAGE > this.mReplyArray.length 
						? this.mReplyArray.length - 1 
						: start + MAX_REPLY_PAGE;

			for (var index = start; index < end; ++index) {
				html += this.mReplyArray[index].template();
			}
		}
		replyBody.html(html);
	};
	
	//显示页码
	this.freshPageHTML = function(id) {
		var pageLine = jQuery("#" + PAGE_LINE_ID + id);
		var html = "";
		
		if (this.mTotalPage != 0) {
			if (this.mCurrentPage == 1) {
				html += PAGE_SWITCH_DISABLE.replace('{{arrow}}', '<');
			} else {
				html += PAGE_SWITCH.replace('{{arrow}}', '<').replace('{{id}}', id);
			}
			
			for (var index = 1; index <= this.mTotalPage; ++index) {
				if (index == this.mCurrentPage) {
					html += PAGE_CURRENT.replace('{{page-num}}', index);
				} else {
					html += PAGE_NORM.replace('{{page-num}}', index).replace('{{id}}', id);
				}
			}
		
			if (this.mCurrentPage == this.mTotalPage) {
				html += PAGE_SWITCH_DISABLE.replace('{{arrow}}', '>');
			} else {
				html += PAGE_SWITCH.replace('{{arrow}}', '>').replace('{{id}}', id);
			}
		}
		
		pageLine.html(html);
	}
	
	//换页
	this.switchPage = function(id, buttonType) {
		if (buttonType == '<') {
			this.mCurrentPage--;
		} else if (buttonType == '>') {
			this.mCurrentPage++;
		} else {
			this.mCurrentPage = parseInt(buttonType);
		}
		console.log("switch page");
		this.freshHTML(id);
		this.freshPageHTML(id);
	};
	
	//添加回复
	this.addReply = function(reply) {
		this.mReplyArray.push(reply);
		this.mTotalPage = Math.ceil(this.mReplyArray.length / MAX_REPLY_PAGE);
	};
}

function Reply(commentIndex, index, headUrl, userName, homepageUrl, date, content) {
//member:
	this.mCommentIndex = commentIndex;
	this.mIndex = index;
	this.mHeadUrl = headUrl;
	this.mUsername = userName;
	this.mHomepageUrl = homepageUrl;
	this.mDate = date;
	this.mContent = content;

//public function:
	this.template = function() {
		return REPLY_TEMPLAE.replace(/{{cid}}/g, this.mCommentIndex)
						    .replace(/{{id}}/g, this.mIndex)
						    .replace(/{{author-url}}/g, this.mHomepageUrl)
							.replace("{{head-url}}", this.mHeadUrl)
							.replace("{{author-id}}", this.mUsername)
							.replace("{{datetime-value}}", this.mDate)
							.replace("{{datetime-text}}", this.mDate)
							.replace("{{reply-content}}", this.mContent);
	}

}

//=======================================================================
//
//	测试用
//
//=======================================================================
	var t_author_url = "#";
	var t_head_url = "http://1.gravatar.com/avatar/50a7625001317a58444a20ece817aeca?s=60&amp;d=http%3A%2F%2F1.gravatar.com%2Favatar%2Fad516503a11cd5ca435acc9bb6523536%3Fs%3D60&amp;r=G";
	var t_author_id = "John Doe";
	var t_datetime_value = "2013-02-26T13:27:04+00:00";
	var t_datetime_text = "February 26, 2013 at 1:27 pm";
	var t_content = 'Lorem ipsum dolor sit amet, consectetuer adipiscing elit, sed diam nonummy nibh euismod tincidunt ut laoreet dolore magna aliquam erat volutpat. Ut wisi enim ad minim veniam, quis nostrud exerci tation ullamcorper suscipit lobortis nisl ut aliquip ex ea commodo consequat. </p><p>Duis autem vel eum iriure dolor in hendrerit in vulputate velit esse molestie consequat, vel illum dolore eu feugiat nulla facilisis at vero eros et accumsan et iusto odio dignissim qui blandit praesent luptatum zzril delenit augue duis dolore te feugait nulla facilisi. Nam liber tempor cum soluta nobis eleifend option congue nihil imperdiet doming id quod mazim placerat facer possim assum.';

	var t_r_author_url = "#";
	var t_r_head_url = "http://1.gravatar.com/avatar/50a7625001317a58444a20ece817aeca?s=60&amp;d=http%3A%2F%2F1.gravatar.com%2Favatar%2Fad516503a11cd5ca435acc9bb6523536%3Fs%3D60&amp;r=G";
	var t_r_author_id = "John Doe";
	var t_r_datetime_value = "2013-02-26T13:27:04+00:00";
	var t_r_datetime_text = "February 26, 2013 at 1:27 pm";
	var t_reply_content = 'i think ok';

	var t_comments = new Array();
	
//=======================================================================
//
//	辅助函数
//
//=======================================================================
function showreply(btnId) {
	var id = parseInt(btnId.substr(btnId.lastIndexOf("-") + 1));
	var replyPage = jQuery("#" + REPLY_DIV_ID + id);
	
	if (replyPage.css("display") == "none") {
		commentPage.mComments[id].showReplyPage();
		replyPage.css("display", "block");
	} else {
		commentPage.mComments[id].hideReplyPage();
		replyPage.css("display", "none");
	}
}

function switchPage(id, btn) {
	commentPage.mComments[parseInt(id)].mReplyPage.switchPage(id, btn);
}

function fromText(wrap) {
    return wrap.toString().match(/\/\*\s([\s\S]*)\s\*\//)[1];
};

function reply(btnId) {
	console.log(btnId);
	var id = parseInt(btnId.substr(btnId.lastIndexOf("-") + 1));
	commentPage.mComments[id].reply();
}
