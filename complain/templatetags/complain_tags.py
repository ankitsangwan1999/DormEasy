from django import template
register = template.Library()
from ..models import Comment
from ..models import Complaint

@register.simple_tag
def useful_comments(complain_id):
	cnt=0
	comments=[]
	i=0
	for comment in Comment.objects.all():
		if comment.complaint.id == complain_id:
			if comment.user.email == comment.complaint.concerned_authority:
				comments.insert(i,comment)
				i=i+1
			else:
				comments.append(comment)
	if len(comments)==0:
		return 0
	else:
		return comments

@register.simple_tag
def useful_reviews(complain_id):
	cnt=0
	comments=[]
	for comment in Comment.objects.all().filter(complaint_id=complain_id,is_review=True):
		comments.append(comment)
	if len(comments)==0:
		return 0
	else:
		return comments

@register.filter
def is_res(complain_id):
	for complaint in Complaint.objects.all().filter(id = complain_id):
		if int(complaint.status) == 2:
			
			return True
		else:
			
			return False