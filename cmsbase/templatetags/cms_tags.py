from django import template
register = template.Library()

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