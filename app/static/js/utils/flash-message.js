var opts = {
	"closeButton": true,
	"debug": false,
	"positionClass": "toast-top-full-width",
	"onclick": null,
	"showDuration": "5000",
	"hideDuration": "1000",
	"timeOut": "5000",
	"extendedTimeOut": "5000",
	"showEasing": "swing",
	"hideEasing": "linear",
	"showMethod": "fadeIn",
	"hideMethod": "fadeOut"
};
toastr.success("{{ message }}", "", opts);