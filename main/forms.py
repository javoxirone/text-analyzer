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

    class Meta:
        fields = ['file']
