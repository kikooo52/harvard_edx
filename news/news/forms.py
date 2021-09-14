from django import forms
from django.core.validators import validate_slug


class NewsForm(forms.Form):
    title = forms.CharField(max_length=255)
    slug = forms.SlugField(validators=[validate_slug])
    content = forms.CharField(widget=forms.Textarea())
    image = forms.FileField()
    is_active = forms.BooleanField(required=False)
    is_hot_news = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        super(NewsForm, self).__init__(*args, **kwargs)
        if not self.data:
            self.fields.get('image').required = True
        else:
            self.fields.get('image').required = False
