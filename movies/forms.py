from django import forms


class NameForm(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100)


class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)
    sender = forms.EmailField()
    cc_myself = forms.BooleanField(required=False)


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(max_length=150)
    email = forms.EmailField()


class NewQuestionForm(forms.Form):
    question_short = forms.CharField(label='Question', max_length=200)


class AddSuggestion(forms.Form):
    reason = forms.CharField(label='Reason', max_length=200, required=False)
    mid = forms.IntegerField()
    qid = forms.IntegerField()


class AddSimilar(forms.Form):
    reason = forms.CharField(label='Reason', max_length=200, required=False)
    linkto = forms.IntegerField()
    linkfrom = forms.IntegerField()


class VoteOnSuggestion(forms.Form):
    vote = forms.IntegerField
    suggid = forms.IntegerField


class RateSuggestion(forms.Form):
    rating = forms.IntegerField()
    suggid = forms.IntegerField()
    opcomment = forms.CharField()


class SimilarMovies(forms.Form):
    movid = forms.IntegerField()


class SettingButton(forms.Form):
    type = forms.CharField(label='Reason', max_length=200, required=False)
    value = forms.CharField(label='Reason', max_length=200, required=False)