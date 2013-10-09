from __future__ import division

from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect, render

from datetime import date, timedelta

from niko.models import Poll, Vote

def poll(request, slug, year=None, month=None, day=None, error=None, success=None):

	context = {
		'error'   : error,
		'hostname': request.get_host(),
		'success' : success,
		'Vote'    : Vote
	}

	# Find related poll
	try:
		poll = Poll.objects.get(slug = slug)
		context['poll'] = poll
	except ObjectDoesNotExist:
		no_poll = 'No poll for {}'.format(slug.title())
		context['error'] = error + no_poll if error  else no_poll
		return render(request, 'poll.html', context)

	votes = None
	if day and month and year:
		givendate = date(int(year), int(month), int(day))
		votes = Vote.objects.filter(poll__id=poll.id).filter(
			pub_date__gte = givendate).order_by('-pub_date')
		context['day']   = day
		context['month'] = month
		context['year']  = year
	else:
		votes = Vote.objects.filter(poll__id=poll.id).order_by(
			'-pub_date')
	context['votes'] = votes
	
	# Compute average mood
	votes_count = votes.count()
	votes_kinds = { 'bads': Vote.BAD , 'oks' : Vote.OK,
		'greats' : Vote.GREAT
	}
	if votes_count > 0:
		for varname, votetype in votes_kinds.iteritems():
			# Compute average safely
			context[varname] = votes.filter( mood = votetype ).count()
			if context[varname] > 0:
				context[varname] = (context[varname] / votes_count) * 100
	else:
		for varname, _ in votes_kinds.iteritems():
			context[varname] = 0

	return render(request, 'poll.html', context)

def polls(request):
	polls = Poll.objects.all().order_by('-pub_date')
	return render(request, 'polls.html', { 'polls' : polls } )

def save(request, slug, mood):

	# Find related poll
	context = { 'Vote' : Vote }
	try:
		a_poll = Poll.objects.get(slug = slug)
		context['poll'] = a_poll
	except ObjectDoesNotExist:
		context['error'] = 'No poll for {}'.format(slug.title())
		return render(request, 'vote.html',context)

	# TODO: Create object with current date in database
	today = date.today()
	error = None
	success = None
	if not mood in [Vote.BAD, Vote.OK, Vote.GREAT]:
		error = 'I do not know this kind of vote.'
	else:
		currentip = get_client_ip(request)
		yesterday = today - timedelta( days = 1 )
		today_s_votes = Vote.objects.filter(poll__id=a_poll.id).filter(
			ip = currentip,pub_date__gt = yesterday).count() 
		if today_s_votes > 0:
			error = '{} already voted today.'.format(currentip)
		else:
			vote = Vote.objects.create(ip = currentip, mood = mood,
				pub_date = today, poll_id = a_poll.id)
			success = 'Vote saved.'
	return poll(request, slug, error = error, success = success)

def vote(request, slug):
	context = {'Vote': Vote}
	try:
		context['poll'] = Poll.objects.get(slug = slug)
	except ObjectDoesNotExist:
		context['error'] = 'No poll for {}'.format(slug.title())
	return render(request, 'vote.html', context)

# Utilities
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
