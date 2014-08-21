
$(document).ready(function(){
	function convertToSlug(Text)
	{
	    return Text
	        .toLowerCase()
	        .replace(/ /g,'-')
	        .replace(/[^\w-]+/g,'')
	        ;
	}

	$('[data-slug]').keyup(function(){
		var slug = convertToSlug($(this).val());
		var slug_field = $(this).data('slug');
		$('[name='+slug_field+']').val(slug);
	})
})
