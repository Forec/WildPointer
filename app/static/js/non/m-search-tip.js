var ELEM_TEMPLATE = '<div class="search-tip-elem" id="{{id}}" onclick="jump(this.id)"><a class="search-tip-content" href="{{url}}">{{content}}</a></div>';

jQuery(document).ready(
	function() {
		$(window).resize(resizeSearchTip);
		
		$('body').click(function(e) {
			if(!$(e.target).hasClass(".search-tip") || !$(e.target).hasClass(".search-tip-elem")) {
				if (jQuery("#search-tip").css("display") == "block")
					jQuery("#search-tip").css("display", "none");
			}
		});
		
		$('.search-tip-elem').click(
			function() {
				jQuery("#search-tip").html("");
				$(location).attr('href', $(this).children('a').attr("href"));
			}
		);
	}
);



var arr = new Array("faqfaqfa", "faqfaqfa", "faqfaqfa", "faqfaqfa");

function hasInput(text, event) {
	console.log(text);
	if (text == "" && jQuery("#search-tip").css("display") != "none") {
		jQuery("#search-tip").css("display", "none");
		return;
	}
	showSimilar('dafs');
//	$.ajax({
//		url: "",
//		type: "POST",
//		data: {
//			'request': /*JSON.stringfy({
//				'username': username,
//				'password': password
//			})*/
//			{
//				'userInput': text,
//			}
//		},
//		success: showSimilar,
//		err: doNothing
//	});
};

function showSimilar(response) {
	resizeSearchTip();
	
	var html = "";
	for (var i = 0; i < 5; ++i) {
		html += ELEM_TEMPLATE.replace('{{url}}', 'http://baidu.com').replace('{{id}}', 'elem-' + i).replace('{{content}}', '知乎');
	}
	
	jQuery("#search-tip").html(html);
	jQuery("#search-tip").css("display", "block");
};

function doNothing(error) {

};

function jump(id) {
	var text = $("#" + id).children('a').attr('href');
	console.log(text);
	$(location).attr('href', text);
};

function resizeSearchTip() {
	var tip = jQuery("#search-tip");
	
	var top = jQuery("#s").offset().top;
	var left = jQuery("#s").offset().left;
	var width = jQuery("#s").outerWidth();
	var height = jQuery("#s").outerHeight();
	console.log("a" + top);
	
	tip.css("top", top + height + "px");
	tip.css("width", width + "px");
	tip.css("left", left + "px");
}
