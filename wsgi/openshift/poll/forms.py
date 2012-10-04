from django import forms

import logging
logger = logging.getLogger('myproject.custom')

class PollVoteForm(forms.Form):
    vote = forms.ChoiceField(widget=forms.RadioSelect())
    
    def __init__(self, poll):
        forms.Form.__init__(self)
        self.fields['vote'].choices = [(c.id, c.choice) for c in poll.choice_set.all()]

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file  = forms.FileField()
    