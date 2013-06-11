from django import template
register = template.Library()

from cmsbase.models import Page

# Truncate chars but leaving last word complete
@register.filter("smart_truncate_chars")
def smart_truncate_chars(value, max_length):
	if len(value) > max_length:
		# Limits the number of characters in value tp max_length (blunt cut)
		truncd_val = value[:max_length]
		# Check if the next upcoming character after the limit is not a space, in which case it might be a word continuing
		if value[max_length] != " ":
			# rfind will return the last index where matching the searched character, in this case we are looking for the last space
			# Then we only return the number of character up to that last space
			truncd_val = truncd_val[:truncd_val.rfind(" ")]
		return  truncd_val + "..."
	return value



class PageBySlugNode(template.Node):
    def __init__(self, slug, varname):
    	if slug[0] in ('"', "'"):
    		self.slug = slug[1:-1]
    		self.is_template_var = False
    	else:
    		self.slug = template.Variable(slug)
    		self.is_template_var = True
        self.varname = varname
    def render(self, context):
    	if self.is_template_var:
    		self.slug = self.slug.resolve(context)
    	self.pages = Page.objects.filter(slug=self.slug)
        if self.pages.count() > 0:
    	   context[self.varname] = self.pages[0]
    	return ''

@register.tag
def get_page_by_unique_identifier(parser, token):
    try:
        # split_contents() knows not to split quoted strings.
        tag_name, slug, conjonction, varname  = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("%r tag must be in the following format: {% get_page_by_slug 'page-slug' as pagevar %}" % token.contents.split()[0])
    
    return PageBySlugNode(slug, varname)