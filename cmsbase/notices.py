from cotimail import Notice

class CustomNotice(Notice):
	# Use as a list display
	name = 'Moderation request' 
	# Use for the preview URL as a slug, so it must not contains spaces or other symbols than lowercase letters and hyphens
	identifier = 'moderation-request' 
	# Defines an HTML template for this notice
	html_template = 'cmsbase/notice/moderate.html'
	text_template = 'cmsbase/notice/moderate.txt'

	# A JSON representation of the context dictionary, which is the format it will be saved as in the EmailLog
	context = {'object-title': 'Object title'}
	
	# Passing on come context variables to build the subject line 
	subject = u'%s %s' % ('Moderation request for: ', context['object-title'])