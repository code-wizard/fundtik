/*
Template Name: Color Admin - Responsive Admin Dashboard Template build with Twitter Bootstrap 3 & 4
Version: 4.0.0
Author: Sean Ngu
Website: http://www.seantheme.com/color-admin-v4.0/admin/
*/

var handleClipboard = function() {
	var clipboard = new Clipboard('.btn');
	
	$('.copy').on('click', function(e) {

		$(this).tooltip({
			title: 'Copied',
			placement: 'top'
		});
		$(this).tooltip('show');
		setTimeout(()=> {
			$(this).tooltip('dispose');
		}, 500);
	});
};


var FormPlugins = function () {
	"use strict";
    return {
        //main function
        init: function () {
			// handleDatepicker();
			// // handleIonRangeSlider();
			// handleFormMaskedInput();
			// handleFormColorPicker();
			// handleFormTimePicker();
			// handleFormPasswordIndicator();
			// handleJqueryAutocomplete();
			// handleBootstrapCombobox();
			// handleSelectpicker();
			// handleTagsInput();
			// handleJqueryTagIt();
			// handleDateRangePicker();
			// handleSelect2();
			// handleDateTimePicker();
			// handleBootstrapColorPalette();
			// handleSimpleColorpicker();
			handleClipboard();
        }
    };
}();