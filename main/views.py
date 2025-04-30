from django.shortcuts import render
from django.http import HttpResponse

from main.forms import TextFileUploadForm
from main.models import File, FileAnalysis


# Create your views here.
def index_view(request):
    return render(request, "main/index.html", status=200)


def new_file_upload_view(request):
    if request.method == 'GET':
        form = TextFileUploadForm()
        return render(request, "main/form.html", context={'form': form}, status=200)
    elif request.method == 'POST':
        form = TextFileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['file']

            file = File.objects.create(
                file=uploaded_file,
            )
            file_analysis = FileAnalysis.objects.get(file=file)

            return render(request, "main/result.html",
                          context={'analysis': file_analysis},
                          status=200)
        else:
            return render(request, "main/form.html",
                          context={'form': form},
                          status=400)
    else:
        return HttpResponse("Method not allowed", status=405)
