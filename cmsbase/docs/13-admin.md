## Admin

### Make auto-complete slug field from another field

You can set a field to pre-populated as a slug from another field. First you need to include the following Media class in your form:

	class Media:
        js = ('js/slugify.js',)

Then, on init the form or when declaring the field widget, you need to set the following attribute:

	...
	def __init__(self, page, *args, **kwargs):

        super(FormClass, self).__init__(*args, **kwargs)
		
		# Assign auto-slug from title to slug field
        self.fields['title'].widget.attrs['data-slug'] = 'slug'

In the example above, the field 'title' will prepopulate the field 'slug' with a slug value generated from the title value.