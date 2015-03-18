---
layout: page
title: Usage
permalink: "usage.html"
---

Usage
=====

## Template 


### Get the page url

Generate the full page URL in the current language and including the language prefix (if multilingual).

	{{page.get_absolute_url}}


### Retrieve the page main title

Please note that the 'translated' method retrieves the content associated to the current set language.

	{{page.translated.title}}


### Retrieve the page content from the data set

The article is using a dataset to manage the fields associated to it. Each field is contained within a fieldset. So the path to retrieve the content from the dataset will always be the fieldset name followed by the field name. Spaces are replaced with underscore.

So for example, the field 'body' within the "page content" fieldset will be:

	{{article.translated.page_content_body|safe}}

> Please note that the 'translated' method retrieves the content associated to the current set language. The 'safe' filter must be used for content created using the 'editorfield' to render the HTML.

### Retrieve page links from the data set

The CMS saves the id of the page as a reference in the data set, so you will need to call the filter `page_id|get_page_url` to retrieve the url from the page id:


	{% load cms_tags %}
	<a href="{{page.translated.page_content_another_page_link|get_page_url}}">
		{{page.translated.page_content_another_page_text}}
	</a>

### Retrieve images

When using the `imagefield` in the data set, all images will available against the page objects:
	
	{{page.images}}

To display the images, you can loop through them:

	{% for image in page.images %}
		<a href="{{image.link_to_url}}">
			<img src="{{image.get_file_url}}" alt="{{image.caption}}">
		</a>
	{% endfor %}

If you would like to display thumbnail, you can `sorl.thumbnail` to display them:
	
	{% load thumbnail %}

	{% for image in page.images %}
		<a class="lightbox" href="{{image.get_file_url}}">	
			{% thumbnail image.file "400x400" crop="center" as im %}
			    <img src="{{ im.url }}" width="{{ im.width }}" height="{{ im.height }}">
			{% endthumbnail %}
		</a>
	{% endfor %}

## Tags

### Retrieve a page by unique identifier

You can retrieve a specific page using the template tag `get_page_by_unique_identifier`, and using the "Unique Page Identifier" field as a key:

	{% get_page_by_unique_identifier 'unique-page-identifer' as page %}

	<!-- Get the page title from translated content -->

	{{page.translated.title}}


### Retrieve links for a page

`links_for_page` populate the template context with a list of members related to a specific page.

	{% links_for_page page as links %}
	
Eg:

	{% links_for_page page as links %}
	{% for link in links %}
		{{link}}
	{% endfor %}

### Retrieve home page

Return the original home page instance as `home` in the template context if exist, otherwise return `False`

	{% home_page as home %}

### Retrieve current language

Get the language name from the language code:

	{% language_name LANGUAGE_CODE %}


## Filters

### Truncate text

Truncates by number of character without splitting whole words, and add '...' in the end if longer. 

	{{var|smart_truncate_chars}}

*Last updated by Guillaume Piot, 18 March 2015*