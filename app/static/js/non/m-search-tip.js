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

function hasInput(text, event, search_url) {
//	console.log(text);
	if (text == "" && jQuery("#search-tip").css("display") != "none") {
		jQuery("#search-tip").css("display", "none");
		return;
	}
	$.ajax({
		url: search_url + "/" + text,
		type: "GET",
		success: showSimilar,
		err: function(err) {
		}
	});
};

function showSimilar(response) {
	resizeSearchTip();
	
	var html = "";
	for (var i = 0; i < response.results.length; ++i) {
	    var title = response.results[i].substr(0, 20);
	    if (response.results[i].length > 20) {
	        title += "...";
	    }
		html += ELEM_TEMPLATE.replace('{{url}}', response.urls[i]).replace('{{id}}', 'elem-' + i).replace('{{content}}', title);
	}
	
	jQuery("#search-tip").html(html);
	jQuery("#search-tip").css("display", "block");
};

function jump(id) {
	var text = $("#" + id).children('a').attr('href');
	$(location).attr('href', text);
};

function resizeSearchTip() {
	var tip = jQuery("#search-tip");
	
	var top = jQuery("#s").offset().top;
	var left = jQuery("#s").offset().left;
	var width = jQuery("#s").outerWidth();
	var height = jQuery("#s").outerHeight();

	tip.css("top", top + height + "px");
	tip.css("width", width + "px");
	tip.css("left", left + "px");
}
