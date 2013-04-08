import os

from django.contrib.admin.widgets import AdminFileWidget
from django.utils.translation import ugettext as _
from django.utils.safestring import mark_safe

class AdminImageWidget(AdminFileWidget):
	def render(self, name, value, attrs=None):
		output = []
		
		if value and getattr(value, "url", None):
			image_url = value.url
			file_name=str(value)
			#image_url = '%s_%s%s' % (os.path.splitext(image_url)[0],280, os.path.splitext(image_url)[1])
			output.append(u' <a href="%s" target="_blank" class="image_link"><img title="Click to preview" src="%s" alt="%s" width="80px" /></a>' % (image_url, image_url, file_name))
		output.append(super(AdminFileWidget, self).render(name, value, attrs))

		return mark_safe('<div class="thumbnail admin-thumbnail">%s</div>' % u''.join(output))

class AdminCustomFileWidget(AdminFileWidget):
	def render(self, name, value, attrs=None):
		output = []
		
		if value and getattr(value, "url", None):
			image_url = value.url
			file_name=str(value)
			file_type = os.path.splitext(image_url)[1]
			file_type = file_type.replace('.','')
			#image_url = '%s_%s%s' % (os.path.splitext(image_url)[0],280, os.path.splitext(image_url)[1])
			if file_type in ['jpg', 'jpeg', 'png', 'gif']:
				output.append(u' <a href="%s" target="_blank" class="image_link"><img title="Click to preview" src="%s" alt="%s" width="80px" /></a>' % (image_url, image_url, file_name))
			else:
				output.append(u' <i class="file-icon-%s float-left margin-right"></i>' % (file_type))
		output.append(super(AdminFileWidget, self).render(name, value, attrs))

		return mark_safe('<div class="thumbnail admin-thumbnail">%s</div>' % u''.join(output))


def get_media_upload_to(location, filename):
	import os, hashlib, random

	fileName, fileExtension = os.path.splitext(filename)


	# print "location = %s, filename = %s, fileExtension = %s"%(location, fileName, fileExtension)
	
	sha = hashlib.new('sha1')
	sha.update(str(random.random()))
	salt = sha.hexdigest()[:5]
	
	sha = hashlib.new('sha1')
	sha.update('%s%s' % (salt,fileName))
	newname = sha.hexdigest()
	
	return '%s/%s%s' % (location, newname, fileExtension) 