from django import forms

class DateInterval(forms.Form):

    '''Allow to specify two consecutive dates.'''
    startdate = forms.DateField(label='Shown votes starting date')
    enddate   = forms.DateField(label='Shown votes ending date', required=False)

    def clean(self):
        '''Check if end date is valid.'''
        cleaned_data = super(DateInterval, self).clean()
        startdate = cleaned_data.get('startdate')
        enddate   = cleaned_data.get('enddate')
        if enddate and (startdate > enddate):
            del cleaned_data['enddate']
            raise forms.ValidationError(
                'End date should be more recent than start date.',
                code = 'InvalidDateRange')
        return cleaned_data
