from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404
from apps.photogallery.models import Gallery, Photo


class GalleriesListView(ListView):
    """Отображает страницу со списком галерей."""
    model = Gallery
    template_name = 'photogallery/galleries_list.html'
    paginate_by = 12

    def get_queryset(self):
        return Gallery.objects.filter(is_visible=True).order_by('-created_at')


class PhotosListView(ListView):
    """Отображает страницу со списком фотографий."""
    model = Photo
    template_name = 'photogallery/photos_list.html'
    paginate_by = 12
    gallery = None

    def get_queryset(self, *args, **kwargs):
        self.gallery = get_object_or_404(Gallery, pk=self.kwargs['pk'], is_visible=True)
        return self.gallery.photo_set.filter(is_visible=True).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super(PhotosListView, self).get_context_data(**kwargs)
        context['gallery'] = self.gallery
        return context
