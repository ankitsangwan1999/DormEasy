from django import template
register = template.Library()

from ..models import Notices

# @register.simple_tag
# def categorise(hostel):
# 	print(hostel)
# 	value = "Hostels"
# 	ops = Notices.objects.all()
# 	print(ops)
# 	o=[]
# 	for notice in ops:
# 		print(notice.concerned_hostels.all())
# 		if value, hostel in notice.concerned_hostels.all():
# 			o.append(notice)		
# 	print("Hello")
# 	print(o)
# 	return o

@register.simple_tag
def get_options(question):
	ops = Option.objects.all().filter(question=question).first()
	o=[]
	o.append(ops.option1)
	o.append(ops.option2)
	if(ops.option3 and ops.option4):
		o.append(ops.option3)
		o.append(ops.option4)
	return o

@register.simple_tag
def get_ans(question):
	a = Answer.objects.all().filter(question=question).first()
	return a.corr_answer

@register.filter 	
def times(count):
	return range(int(count))

@register.filter
def is_false(var):
	if var == None:
		return True
	else:
		return False
# @register.filter
# def remove_new_line_at_end(var):
# 	var = str(var)
# 	var.strip()
# 	return var
@register.simple_tag
def noticetag(notice):
	# if hostel_name in notice.concerned_hostels:
	return notice.title
	# else:
		# return notice.concerned_hostels
	# else:
		# return False

