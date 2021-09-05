from django import forms

class SuggestWidget(forms.TextInput):
    template_name = 'widgets/suggest.html'

    class Media:
        js = ['suggest.js']
        # css = {
        #     'all': ['suggest.css']
        # }

    def __init__(self, attrs=None):
        super().__init__(attrs)
        if 'class' in self.attrs:
            self.attrs['class'] += ' suggest'
        else:
            self.attrs['class'] = 'suggest'


