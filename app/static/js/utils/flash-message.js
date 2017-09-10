function flash_success(message) {
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
    toastr.success(message, '', opts);
}

function flash_warning(message) {
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
    toastr.warning(message, '', opts);
}

function flash_error(message) {
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
    toastr.error(message, '', opts);
}

function flash_info(message) {
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
    toastr.info(message, '', opts);
}

function flash_normal(message) {
    flash_info(message);
}