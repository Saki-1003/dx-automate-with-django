from django.shortcuts import redirect, render
from .forms import CompressImageForm
from PIL import Image
import io
from django.http import HttpResponse

def compress(request):
  user = request.user

  if request.method == 'POST':
    form = CompressImageForm(request.POST, request.FILES)
    if form.is_valid():
      original_img= form.cleaned_data['original_img']
      quality = form.cleaned_data['quality']

      compressed_image = form.save(commit=False)
      compressed_image.user = user

      # compress the imgae useing Pillow
      img = Image.open(original_img)
      output_format = img.format

      # create an empty buffer(virtual-file-like-object in memory) to hold the compressed image data in memory instead of saving to disk
      buffer = io.BytesIO()
      # print('buffer:', buffer.getvalue())
      print('cursor position at the beginning:', buffer.tell())

      img.save(buffer, format=output_format, quality=quality)
      print('cursor position after image compression:', buffer.tell())
      buffer.seek(0)
      # print('buffer:', buffer.getvalue())
      print('cursor position after setting back to 0:', buffer.tell())


      # save the compressed imgae in the model instance
      compressed_image.compressed_img.save(
        f'compressed_{original_img}', buffer
      )
      # Automatically download the compressed file
      # covert the binary value in HttpResponse to the file that can be downloaded
      response = HttpResponse(buffer.getvalue(), content_type=f'image/{output_format.lower()}')
      response['Content-Disposition'] = f'attachment; filename=compressed_{original_img}'
      return response
      # return redirect('compress')

  else:
    form = CompressImageForm()
    context = {
      'form': form,
    }
    return render(request, 'image_compression/compress.html', context)