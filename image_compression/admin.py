from django.contrib import admin
from .models import CompressImage
from django.utils.html import format_html

class CompressImageAdmin(admin.ModelAdmin):
  def thumbnail(self, obj):
    return format_html('<img src="{}" width="40" height="40">', obj.compressed_img.url)
  thumbnail.short_description = 'サムネイル画像'

  def original_img_size(self, obj):
    size_mb = obj.original_img.size / (1024*1024)
    return f'{size_mb:.2f} MB'
  original_img_size.short_description = '元のサイズ(MB)'

  def compressed_img_size(self, obj):
    size_mb = obj.compressed_img.size / (1024*1024)
    # if size_mb > 1:
    return f'{size_mb:.2f} MB'
    # else:
    #   size_kb = obj.compressed_img.size / 1024
    #   return f'{size_kb:.2f} KB'
  compressed_img_size.short_description = '圧縮後のサイズ(MB)'

  list_display = ('user', 'thumbnail', 'original_img_size', 'compressed_img_size', 'compressed_at')

admin.site.register(CompressImage, CompressImageAdmin)
