from django.contrib import messages
from django.db.models import Max, Min
from django.shortcuts import render, get_object_or_404

import datetime

from niko.models import Poll, Vote
from niko.forms import DateInterval

# Should match date format used in forms.DateInterval
DATE_FORMAT = '%d/%m/%Y'


def poll(request, slug):
    """Show details of a specific poll."""

    poll = get_object_or_404(Poll, slug=slug)
    context = {'Vote': Vote, 'poll': poll, }

    #
    # Selecting votes from a date interval when requested
    #
    dateform = None
    votes = None
    if request.method != 'POST':
        # Nothing to do
        dateform = DateInterval()
    else:
        # Date interval form has been filled
        dateform = DateInterval(request.POST)
        if dateform.is_valid():

            # Select votes since a date
            startdate = dateform.cleaned_data['startdate']
            context['startdate'] = startdate.strftime(DATE_FORMAT)
            votes = Vote.objects.filter(poll__id=poll.id).filter(
                pub_date__gte=startdate).order_by('-pub_date')

            # Select votes before a date
            enddate = dateform.cleaned_data['enddate']
            if enddate:
                context['enddate'] = enddate.strftime(DATE_FORMAT)
                votes = votes.filter(pub_date__lte=enddate).order_by(
                    '-pub_date')
        else:
            # Format form related errors)
            for fieldname, errors in dateform.errors.iteritems():
                for error in errors:
                    if '__all__' == fieldname:
                        messages.warning(request, error)
                    else:
                        messages.warning(request,
                            '{}: {}'.format(fieldname, error))
    context['dateform'] = dateform

    # Showing all votes if no date has been given
    if votes is None:
        votes = Vote.objects.filter(poll__id=poll.id).order_by('-pub_date')
    context['votes'] = votes

    # Compute average mood
    votes_count = votes.count()
    context['votes_count'] = votes_count
    votes_kinds = {'bads': Vote.BAD, 'oks': Vote.OK, 'greats': Vote.GREAT, }
    if votes_count > 0:
        for varname, votetype in votes_kinds.iteritems():
            # Compute average safely
            count_key = varname + "_count"
            percentage_key = varname + "_percentage"
            context[count_key] = votes.filter(mood=votetype).count()
            if context[count_key] > 0:
                context[percentage_key] = 100.0 * \
                    (float(context[count_key]) / float(votes_count))
            else:
                context[percentage_key] = 0
    else:
        for varname, _ in votes_kinds.iteritems():
            context[varname + "_count"] = 0
            context[varname + "_percentage"] = 0

    #
    # Mood change over poll duration
    #

    # Define dates shown in bar chart
    context['linechart'] = {}
    dates = votes.aggregate(Max('pub_date'), Min('pub_date'))
    startdate = dates['pub_date__min']
    enddate = dates['pub_date__max']

    # Single vote or all votes at once
    if startdate == enddate:
        context['linechart']['labels'] = [startdate]
        context['linechart']['values'] = {}
        for varname, votetype in votes_kinds.iteritems():
            context['linechart']['values'][varname] = [votes.filter(
                mood=votetype).count()]
    else:

        # Splitting vote duration in 4 subintervals
        timestep = (enddate - startdate) / 3
        dates = [startdate, startdate + timestep, startdate + 2 * timestep,
            enddate]

        # Vote count per poll subinterval
        context['linechart']['labels'] = dates
        context['linechart']['values'] = {}
        for adate in dates:
            for varname, votetype in votes_kinds.iteritems():
                count = votes.filter(mood=votetype, pub_date__lte=adate).count()
                if not varname in context['linechart']['values']:
                    context['linechart']['values'][varname] = []
                context['linechart']['values'][varname].append(count)

    return render(request, 'poll.html', context)


def polls(request):
    '''Showing all polls.'''
    polls = Poll.objects.all().order_by('-pub_date')
    return render(request, 'polls.html', {'polls': polls})


def save(request, slug, mood):
    """Saves a vote to database."""

    try:
        mood = int(mood)
    except ValueError:
        messages.warning(request, 'This is not the way to vote.')

    a_poll = get_object_or_404(Poll, slug=slug)

    if not mood in [Vote.BAD, Vote.OK, Vote.GREAT]:
        messages.warning(request, 'I do not know this kind of vote.')
    else:
        currentip = get_client_ip(request)
        yesterday = datetime.date.today() - datetime.timedelta(days=1)
        today_s_votes = Vote.objects.filter(poll__id=a_poll.id).filter(
            ip=currentip, pub_date__gt=yesterday).count()
        if today_s_votes > 0:
            messages.warning(request, '{} already voted today.'
                .format(currentip))
        else:
            Vote.objects.create(ip=currentip, mood=mood,
                poll_id=a_poll.id)
            messages.success(request, 'Your vote have been saved.')
    return poll(request, slug)


def vote(request, slug):
    poll = get_object_or_404(Poll, slug=slug)
    return render(request, 'vote.html', {'poll': poll, 'Vote': Vote})


def handler404(request):
    return render(request, '404.html')


# Utilities
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
