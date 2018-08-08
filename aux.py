##### HELPFUL FUNCTION #####

def sanitize(input_str):
	"""sanitize/validate user phone number inputs."""
	sanitized = input_str
	invalid_strs = ['(',')','-','input://','file://',';','<','>','$','--',
					'../','table','TABLE','*','#',' ','_','/','@','drop','DROP']

	for char in invalid_strs:
		if char in sanitized:
		   sanitized = sanitized.replace(char,'')

	# sanitized = ''
	# for char in input_str:
	# 	#if char is OK:
	# 		sanitized += char	

	return sanitized


def sanitize_comments(input_str):
	"""sanitize comments before adding to db."""
	sanitized_comments = input_str
	invalid_strs = [';','file://','../','input://','users;','calls;','--']

	for char in invalid_strs:
		if char in sanitized_comments:
			sanitized_comments = sanitized_comments.replace(char,' ')

	return	sanitized_comments
