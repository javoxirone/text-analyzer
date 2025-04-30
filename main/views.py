from django.shortcuts import render
from django.http import HttpResponse

from main.forms import TextFileUploadForm


# Create your views here.
def index_view(request):
    return render(request, "main/index.html", status=200)


def new_file_upload_view(request):
    if request.method == 'GET':
        form = TextFileUploadForm()
        return render(request, "main/form.html", context={'form': form}, status=200)
    elif request.method == 'POST':
        new_pk = request.POST.get("pk")
        return render(request, "main/result.html", status=200)
    else:
        return HttpResponse("Method not allowed", status=405)
