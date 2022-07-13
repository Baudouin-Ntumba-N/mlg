from django import forms



class ReplyForm(forms.Form):

  reply_recipient = forms.CharField(widget = forms.HiddenInput())

  reply_content = forms.CharField(widget = forms.TextInput())

  comment_id = forms.CharField(widget = forms.HiddenInput())



class CommentForm(forms.Form):

  #user_id = forms.CharField(widget = forms.HiddenInput())

  article_slug = forms.CharField(widget = forms.HiddenInput())

  comment = forms.CharField(widget = forms.TextInput())