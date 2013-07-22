$(document).ready(function(){
	$('.add-row a').click(function(){
		select_language();
		setup_redactor();
		set_prepopulate();
	});
	select_language();
	set_flag();
	set_prepopulate();
	related_pages();
});

//Set readactor textarea
function setup_redactor(){

        var redactor_fields = $('[class*="dynamic-"] .redactor_box textarea.redactor_content').last();
        var redactor_fields_boxes = $('[class*="dynamic-"] .redactor_box').last();
        
        $.each(redactor_fields_boxes, function(i, index){

            $(index).after(redactor_fields[i]);
	        $(index).next('textarea').redactor({
	            imageUpload: '/uploads/ajax/photos/upload/',
	            imageGetJson: '/uploads/ajax/photos/recent/',
	            fileUpload: '/uploads/ajax/files/upload/',
	            autoresize: false,
	            minHeight:300
	        });
	         $(index).remove();
        });
        //var redactor_fields = $("textarea.redactor_content");


}

function select_language(){
	// Switch flag accordingly
	$('.field-language_code select').change(function(e){
		name = $(this).attr('name').replace('-language_code','');
		if($(this).val()) $('#'+name+' h3 img').attr('src','/static/admin/img/flags/'+$(this).val()+'.png');
	})
}

function set_flag(){
	$.each($('.field-language_code select'), function(i, index){
		name = $(index).attr('name').replace('-language_code','');
		if($(this).val()) $('#'+name+' h3 img').attr('src','/static/admin/img/flags/'+$(this).val()+'.png');
	})
}

function set_prepopulate(){
	if(!$('body').hasClass('action-change')){
		$('.field-title input').keyup(function(){
			$(this).parent().parent().parent().next().find('input').val(URLify($(this).val(), 100));
		})
	}
	
	
}


// Behaviour for related pages
function related_pages(){
	$('.field-related_pages').hide();
	$('.field-related_pages').before('<div class="inner"><a href="#" onclick="$(\'.field-related_pages\').slideDown();$(this).parent().hide();" class="btn btn-small">Show related pages</a><br><br></div>');
}
