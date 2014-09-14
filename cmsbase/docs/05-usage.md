---
layout: page
title: Usage
permalink: "usage.html"
---

Usage
=====

##Template

**Retrieve the page url**

{% raw %}`{{page.get_absolute_url}}`{% endraw %}

Generate the full page URL in the current language and including the language prefix (if multilingual)


###Retrieve the page main title

{% raw %}`{{page.translated.title}}`{% endraw %}

Please note that the 'translated' method retrieves the content associated to the current set language.


###Retrieve the article content from the data set

The article is using a dataset to manage the fields associated to it. Each field is contained within a fieldset. So the path to retrieve the content from the dataset will always be the fieldset name followed by the field name. Spaces are replaced with underscore.

So for example, the field 'body' within the "page content" fieldset will be:

Eg:
{% raw %}`{{article.translated.page_content_body|safe}}`{% endraw %}

> Please note that the 'translated' method retrieves the content associated to the current set language. The 'safe' filter must be used for content created using the 'editorfield' to render the HTML.

###Rendering page links

The CMS saves the id of the page as a reference in the data set, so you will need to call the filter `page_id|get_page_url` to retrieve the url from the page id:

{% raw %}
	{% load cms_tags %}
	<a href="{{page.translated.page_content_another_page_link|get_page_url}}">{{page.translated.page_content_another_page_text}}</a>
{% endraw %}	

##Admin

#Make auto-complete slug field from another field

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