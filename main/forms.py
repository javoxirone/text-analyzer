from django import forms


class TextFileUploadForm(forms.Form):
    file = forms.FileField(
        label='Загрузите текстовый файл для анализа',
        widget=forms.ClearableFileInput(
            attrs={
                'class': 'form-control form-control-lg',
                'id': 'formFileLg',
            }
        ),
        required=True,
    )

    is_public = forms.BooleanField(
        label='Сделать файл и его анализ общедоступными',
        required=False,
        initial=False,
        widget=forms.CheckboxInput(
            attrs={
                'class': 'form-check-input',
            }
        )
    )

    class Meta:
        fields = ['file', 'is_public']
