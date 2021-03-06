/*
*
*   Custom JavaScript
*   Product: KnowledgeBase WordPress Theme
*
* */
jQuery(document).ready(function(e) {

	$ = jQuery;

    /*-----------------------------------------------------------------------------------*/
    /*	Menu Dropdown Control
     /*-----------------------------------------------------------------------------------*/
    $('.main-nav li').hover(function(){
        $(this).children('ul').stop(true, true).slideDown(500);
    },function(){
        $(this).children('ul').stop(true, true).slideUp(500);
    });

    $('.sub-menu li').click(function(){
        window.location = $(this).children('a').attr('href');
    });


    /*-----------------------------------------------------------------------------------*/
    /* CSS Fixes
    /*-----------------------------------------------------------------------------------*/
    //$(".flickr-photos > a:nth-child(3n+3) img").css("marginLeft","0px");



    /*-----------------------------------------------------------------------------------*/
    /* Apply Class on search form widget inputs
    /*-----------------------------------------------------------------------------------*/
    $("#searchform #s").addClass("span3 search-query");
    $("#searchform #searchsubmit").addClass("btn");



    /*-----------------------------------------------------------------------------------*/
    /*	Page's Nav
     /*-----------------------------------------------------------------------------------*/
    $(".pages-nav a").addClass("btn");



    /*-----------------------------------------------------------------------------------*/
    /*	Tags Cloud
    /*-----------------------------------------------------------------------------------*/
    $('.tagcloud a').removeAttr('style').addClass('btn btn-mini');

	
    /*-----------------------------------------------------------------------------------*/
	/* Pretty Photo Lightbox
	/*-----------------------------------------------------------------------------------*/
   if( jQuery().prettyPhoto )
    {
        $(".pretty-photo").prettyPhoto({
            deeplinking: false,
            social_tools: false
        });


        $('a[data-rel]').each(function() {
            $(this).attr('rel', $(this).data('rel'));
        });


        $("a[rel^='prettyPhoto']").prettyPhoto({
            deeplinking: false,
            social_tools: false
        });
    }




	/* ---------------------------------------------------- */
	/*	Accordion
	/* ---------------------------------------------------- */
    $(function() {
		$('.accordion dt').click(function(){
			$(this).siblings('dt').removeClass('current');
			$(this).addClass('current').next('dd').slideDown(500).siblings('dd').slideUp(500);
		});	
    });



	/* ---------------------------------------------------- */
	/*	Toggle
	/* ---------------------------------------------------- */
    $(function() {
		$('dl.toggle dt').click(function(){
			if($(this).hasClass('current')){
				$(this).removeClass('current').next('dd').slideUp(500);
			}				
			else{
				$(this).addClass('current').next('dd').slideDown(500);
			}
		});	 
    });



	/*-----------------------------------------------------------------------------------*/
	/*	Scroll to Top
	/*-----------------------------------------------------------------------------------*/	
    $(function() {
        $(window).scroll(function () {
            if(!$('body').hasClass('probably-mobile'))
            {
                if ($(this).scrollTop() > 50) {
                    $('a#scroll-top').fadeIn();
                } else {
                    $('a#scroll-top').fadeOut();
                }
            }
            else
            {
                $('a#scroll-top').fadeOut();
            }
        });

        $('a#scroll-top').on('click', function(){
            if(!$('body').hasClass('probably-mobile'))
            {
                $('html, body').animate({scrollTop:0}, 'slow' );
                return false;
            }
        });
    });



	/* ---------------------------------------------------- */
	/*	Tabs
	/* ---------------------------------------------------- */
    $(function(){

        var $tabsNav    = $('.tabs-nav'),
            $tabsNavLis = $tabsNav.children('li');

        $tabsNav.each(function(){
            var $this = $(this);
            $this.next().children('.tab-content').stop(true,true).hide()
                                                 .first().show();
            $this.children('li').first().addClass('active').stop(true,true).show();
        });

        $tabsNavLis.on('click', function(e) {
            var $this = $(this);
            $this.siblings().removeClass('active').end()
                 .addClass('active');
            var idx = $this.parent().children().index($this);
            $this.parent().next().children('.tab-content').stop(true,true).hide().eq(idx).fadeIn();
            e.preventDefault();
        });

    });



	 /* ---------------------------------------------------- */
	 /*  Responsive Tables by ZURB
	 /*	  Foundation v2.1.4 http://foundation.zurb.com
	 /* ---------------------------------------------------- */
	  var switched = false;
	  var updateTables = function() {
		if (($(window).width() < 767) && !switched ){
		  switched = true;
		  $("table.responsive").each(function(i, element) {
			splitTable($(element));
		  });
		  return true;
		}
		else if (switched && ($(window).width() > 767)) {
		  switched = false;
		  $("table.responsive").each(function(i, element) {
			unsplitTable($(element));
		  });
		}
	  };
	   
	  $(window).load(updateTables);
	  $(window).bind("resize", updateTables);
	   
		
		function splitTable(original)
		{
			original.wrap("<div class='table-wrapper' />");
			
			var copy = original.clone();
			copy.find("td:not(:first-child), th:not(:first-child)").css("display", "none");
			copy.removeClass("responsive");
			
			original.closest(".table-wrapper").append(copy);
			copy.wrap("<div class='pinned' />");
			original.wrap("<div class='scrollable' />");
		}
		
		function unsplitTable(original) {
            original.closest(".table-wrapper").find(".pinned").remove();
            original.unwrap();
            original.unwrap();
		}



    /* ---------------------------------------------------- */
    /*	Like Button JS
     /* ---------------------------------------------------- */
    $('#like-it-form .like-it').click(function() {
        var parent = $(this);
        var action = function(){
            var likeButton = parent;
            var likeHtml = likeButton.html();
            var likeNum = parseInt(likeHtml, 10);

            var liked = jQuery("#liked");

            if (liked.val() == "like_it") {
                var url = jQuery("#like_url").val();
                likeNum++;
                likeButton.removeClass("like-it").addClass("dislike-it");
                likeButton.html(likeNum);
                thumbUp(url);
            } else if (liked.val() == "cancel_like_it") {
                var url = jQuery("#cancel_like_url").val();
                likeNum--;
                likeButton.addClass("like-it").removeClass("dislike-it");
                likeButton.html(likeNum);
                thumbDown(url);
            }
	    };
	    auth_before_action(action);
	});

	$('#like-it-form .dislike-it').click(function() {
        var parent = $(this);
        var action = function(){
            var likeButton = parent;
            var likeHtml = likeButton.html();
            var likeNum = parseInt(likeHtml, 10);

            var liked = jQuery("#liked");

            if (liked.val() == "like_it") {
                var url = jQuery("#like_url").val();
                likeNum++;
                likeButton.removeClass("like-it").addClass("dislike-it");
                likeButton.html(likeNum);
                thumbUp(url);
            } else if (liked.val() == "cancel_like_it") {
                var url = jQuery("#cancel_like_url").val();
                likeNum--;
                likeButton.addClass("like-it").removeClass("dislike-it");
                likeButton.html(likeNum);
                thumbDown(url);
            }
	    };
	    auth_before_action(action);
	});

	/* ------------------------------------------------------*/
	/* Support Button JS
	/* ------------------------------------------------------*/
	$('#like-button').click(function() {
	    backupVote();
        var action = function(){
            var likeNum = parseInt(jQuery("#support-counter").html(), 10);
            var like_action = jQuery("#like_action").val();
            var unlike_action = jQuery("#unlike_action").val();

            if (like_action == "like_it") {
                if (unlike_action == "cancel_unlike_it") {
                    likeNum++;
                    jQuery("#unlike-button").removeClass("disunlike-it").addClass("unlike-it");
                    jQuery("#unlike_action").val("unlike_it");
                }
                likeNum++;
                jQuery("#like-button").removeClass("like-it").addClass("dislike-it");
                jQuery("#like_action").val("cancel_like_it");
                jQuery("#support-counter").html(likeNum);
            } else if (like_action == "cancel_like_it") {  /* 此时不可能已经点了 unlike */
                likeNum--;
                jQuery("#like-button").addClass("like-it").removeClass("dislike-it");
                jQuery("#like_action").val("like_it");
                jQuery("#support-counter").html(likeNum);
            }
            voteUp(jQuery("#like_url").val());
	    };
	    auth_before_action(action);
	});



	$('#unlike-button').click(function() {
	    backupVote();
        var action = function(){
            var likeNum = parseInt(jQuery("#support-counter").html(), 10);
            var like_action = jQuery("#like_action").val();
            var unlike_action = jQuery("#unlike_action").val();

            if (unlike_action == "unlike_it") {
                if (like_action == "cancel_like_it") {
                    likeNum--;
                    jQuery("#like-button").removeClass("dislike-it").addClass("like-it");
                    jQuery("#like_action").val("like_it");
                }
                likeNum--;
                jQuery("#unlike-button").removeClass("unlike-it").addClass("disunlike-it");
                jQuery("#unlike_action").val("cancel_unlike_it");
                jQuery("#support-counter").html(likeNum);
            } else if (unlike_action == "cancel_unlike_it") {  /* 此时不可能已经点了 like */
                likeNum--;
                jQuery("#unlike-button").addClass("unlike-it").removeClass("disunlike-it");
                jQuery("#unlike_action").val("unlike_it");
                jQuery("#support-counter").html(likeNum);
            }
            voteDown(jQuery("#unlike_url").val());
	    };
	    auth_before_action(action);
	});



    /*-----------------------------------------------------------------------------------*/
    /*	FAQs
    /*-----------------------------------------------------------------------------------*/
    $('.faq-item').not('.faq-item.active').find('.faq-answer').slideUp('slow');
    $('.faq-item').first().addClass('active').find('.faq-answer').slideDown('slow');

    $('.faq-question, .faq-icon').click(function(e){

        e.preventDefault();

        var $this = $(this);
        var $parent = $this.parent('.faq-item');

        if( $parent.hasClass('active') )
        {
            $parent.removeClass('active').find('.faq-answer').slideUp('slow');
        }
        else
        {
            $parent.addClass('active').find('.faq-answer').slideDown('slow');
        }

    });



    /*-----------------------------------------------------------------------------------*/
    /*	Contact Form 7
    /*-----------------------------------------------------------------------------------*/
    $('.wpcf7-textarea').addClass('span6');
    $('.wpcf7-submit').addClass('btn');


    /*-----------------------------------------------------------------------------------*/
    /*	Search Form Validation
     /*-----------------------------------------------------------------------------------*/
    $('#search-form').validate({
        errorLabelContainer: $("#search-error-container")
    });
	
	
	/*-----------------------------------------------------------------------------------*/
                /*	Responsive Nav
                /*-----------------------------------------------------------------------------------*/
                var $mainNav    = $('.main-nav > div').children('ul');
                var optionsList = '<option value="" selected>Go to...</option>';

                $mainNav.find('li').each(function() {
                        var $this   = $(this),
                                $anchor = $this.children('a'),
                                depth   = $this.parents('ul').length - 1,
                                indent  = '';
                        if( depth ) {
                                while( depth > 0 ) {
                                        indent += ' - ';
                                        depth--;
                                }
                        }
                        optionsList += '<option value="' + $anchor.attr('href') + '">' + indent + ' ' + $anchor.text() + '</option>';
                }).end();

                $('.main-nav > div').after('<select class="responsive-nav">' + optionsList + '</select>');

                $('.responsive-nav').on('change', function() {
                        window.location = $(this).val();
                });



                /*----------------------------------------------------------------------------------*/
                /*	Contact Form AJAX validation and submition
                /*  Validation Plugin : http://bassistance.de/jquery-plugins/jquery-plugin-validation/
                /*	Form Ajax Plugin : http://www.malsup.com/jquery/form/
                /*---------------------------------------------------------------------------------- */
//                if(jQuery().validate && jQuery().ajaxSubmit)
//                {
//                        // Contact Form Handling
//                        var contact_options = {
//                                target: '#message-sent',
//                                beforeSubmit: function(){
//                                        $('#contact-loader').fadeIn('fast');
//                                        $('#message-sent').fadeOut('fast');
//                                },
//                                success: function(){
//                                        $('#contact-loader').fadeOut('fast');
//                                        $('#message-sent').fadeIn('fast');
//                                        $('#contact-form').resetForm();
//                                }
//                        };
//
//                        $('#contact-form').validate({
//                                errorLabelContainer: $("div.error-container"),
//                                submitHandler: function(form) {
//                                        $(form).ajaxSubmit(contact_options);
//                                }
//                        });
//
//                }

                /*-----------------------------------------------------------------------------------*/
                /*	Live Search
                /*-----------------------------------------------------------------------------------*/
//                if(jQuery().liveSearch){
//                        jQuery('#s').liveSearch({url: 'search.php?livesearch=used&s='});
//                }
				
});







