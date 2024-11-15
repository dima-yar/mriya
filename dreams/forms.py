# forms.py
from dal import autocomplete
from django.core.exceptions import ValidationError
from django.forms import ModelForm, Textarea, TextInput, Form, CharField, DecimalField, NumberInput
from tinymce.widgets import TinyMCE
from dreams.models import Dream


class DreamForm(ModelForm):
    class Meta:
        model = Dream
        fields = ['title', 'short_descriptions', 'content', 'tags', 'target_amount']
        widgets = {
            'title' : TextInput(attrs={"class": "title","type": "text", "name": "title", "maxlength": "255", "id": "id_title" }),
            'short_descriptions': Textarea(attrs={"name": "short_descriptions", "class": "short_descriptions", "maxlength": "510", "id": "id_short_descriptions"}),
            'target_amount': NumberInput(attrs={"class": "amount", "name": "amount", "min": "0"}),
            'tags': autocomplete.ModelSelect2Multiple(
                url='tag-autocomplete',
                attrs={"name": "tags", "id": "id_tags"},
            ),
            'content': TinyMCE(attrs={'cols': 80, 'rows': 30, 'id': 'id_content'}),
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean_tags(self):
        tags = self.cleaned_data.get('tags')
        max_tags = 3  # Максимальна кількість тегів
        if len(tags) > max_tags:
            raise ValidationError(f"Можна вибрати не більше {max_tags} тегів.")
        return tags


class DonateForm(Form):
    card_number = CharField(max_length=16)
    expiry_date = CharField(max_length=5)
    cvv = CharField(max_length=3)
    amount = DecimalField()



