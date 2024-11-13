# forms.py
from dal import autocomplete
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


class DonateForm(Form):
    card_holder = CharField(max_length=255, label="Card Holder Name")
    card_number = CharField(max_length=16, label="Card Number")
    expiry_date = CharField(max_length=5, label="Expiry Date (MM/YY)")
    cvv = CharField(max_length=3, label="CVV")
    amount = DecimalField(label="Donation amount")

