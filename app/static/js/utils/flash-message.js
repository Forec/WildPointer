function flash_success(message, title='') {
    var opts = {
    	"closeButton": true,
	    "debug": false,
	    "positionClass": "toast-top-right",
	    "onclick": null,
	    "showDuration": "300",
	    "hideDuration": "1400",
	    "timeOut": "5000",
	    "extendedTimeOut": "3000",
    	"showEasing": "swing",
	    "hideEasing": "linear",
    	"showMethod": "fadeIn",
    	"hideMethod": "fadeOut"
    };
    toastr.success(message, title, opts);
}

function flash_warning(message, title='') {
    var opts = {
    	"closeButton": true,
	    "debug": false,
	    "positionClass": "toast-top-right",
	    "onclick": null,
	    "showDuration": "300",
	    "hideDuration": "1400",
	    "timeOut": "5000",
	    "extendedTimeOut": "3000",
    	"showEasing": "swing",
	    "hideEasing": "linear",
    	"showMethod": "fadeIn",
    	"hideMethod": "fadeOut"
    };
    toastr.warning(message, title, opts);
}

function flash_error(message, title='') {
    var opts = {
    	"closeButton": true,
	    "debug": false,
	    "positionClass": "toast-top-right",
	    "onclick": null,
	    "showDuration": "300",
	    "hideDuration": "1400",
	    "timeOut": "5000",
	    "extendedTimeOut": "3000",
    	"showEasing": "swing",
	    "hideEasing": "linear",
    	"showMethod": "fadeIn",
    	"hideMethod": "fadeOut"
    };
    toastr.error(message, title, opts);
}

function flash_info(message, title='') {
    var opts = {
    	"closeButton": true,
	    "debug": false,
	    "positionClass": "toast-top-right",
	    "onclick": null,
	    "showDuration": "300",
	    "hideDuration": "1400",
	    "timeOut": "5000",
	    "extendedTimeOut": "3000",
    	"showEasing": "swing",
	    "hideEasing": "linear",
    	"showMethod": "fadeIn",
    	"hideMethod": "fadeOut"
    };
    toastr.info(message, title, opts);
}

function flash_normal(message, title='') {
    flash_info(message, title);
}