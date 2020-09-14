from django.shortcuts import render
from django.core.files.storage import FileSystemStorage


def image_upload(request):
    if request.method == "POST" and request.FILES["imagefile"]:
        image_file = request.FILES["imagefile"]
        fs = FileSystemStorage()
        filename = fs.save(image_file.name, image_file)
        image_url = fs.url(filename)
        print(image_url)
        return render(request, "blog/upload.html", {
            "image_url": image_url
        })
    return render(request, "blog/upload.html")


def index(request):
    return render(request, "blog/upload.html")
