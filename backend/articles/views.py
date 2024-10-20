from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.conf import settings

@csrf_exempt  # To allow cross-site requests (remove if CSRF is being handled elsewhere)
def image_upload(request):
    if request.method == 'POST' and request.FILES.get('file'):
        file = request.FILES['file']
        file_name = default_storage.save(file.name, file)  # Save the file
        file_url = f'{settings.MEDIA_URL}{file_name}'  # Generate file URL
        return JsonResponse({'location': file_url})  # Return the file location for TinyMCE

    return JsonResponse({'error': 'Invalid request'}, status=400)
