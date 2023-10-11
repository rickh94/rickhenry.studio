from django.core.paginator import Paginator
from django.db import models
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey
from taggit.models import TaggedItemBase

from studioblog.blocks import ABCBlock, AudioBlock
from wagtail import blocks
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.fields import RichTextField, StreamField
from wagtail.images.blocks import ImageChooserBlock
from wagtail.models import Page
from wagtail.search import index
from wagtail.search.backends import get_search_backend


class BlogIndexPage(Page):
    intro = RichTextField(blank=True)
    content_panels = Page.content_panels + [
        FieldPanel("intro"),
    ]
    paginate_by = 20

    def get_context(self, request):
        """Handles pagination and search for live blog pages"""
        context = super().get_context(request)
        post_list = BlogPage.objects.live().order_by("-date")

        if request.GET.get("q"):
            q = request.GET.get("q")
            s = get_search_backend()
            post_list = s.search(q, post_list)
            context["q"] = q

        paginator = Paginator(post_list, self.paginate_by)
        page_number = request.GET.get("page", 1)
        page_obj = paginator.get_page(page_number)
        context["page_obj"] = page_obj

        return context


class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey(
        "BlogPage", related_name="tagged_items", on_delete=models.CASCADE
    )


# TODO: create video, audio, and abcjs blocks
class BlogPage(Page):
    date = models.DateField("Post date")
    intro = models.CharField(max_length=250)
    body = StreamField(
        [
            ("heading", blocks.CharBlock(classname="title")),
            ("paragraph", blocks.RichTextBlock()),
            ("image", ImageChooserBlock()),
            ("abcnotes", ABCBlock()),
            ("audio", AudioBlock()),
        ],
        blank=True,
        use_json_field=True,
    )
    tags = ClusterTaggableManager(through=BlogPageTag, blank=True)

    search_fields = Page.search_fields + [
        index.SearchField("intro"),
        index.SearchField("body"),
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("date"),
                FieldPanel("tags"),
            ]
        ),
        FieldPanel("intro"),
        FieldPanel("body"),
        # InlinePanel("gallery_images", label="Gallery images"),
    ]


# TODO: make this pretty
class BlogTagIndexPage(Page):
    paginate_by = 20

    def get_context(self, request):
        tag = request.GET.get("tag")
        blogpages = BlogPage.objects.live().filter(tags__name=tag)

        context = super().get_context(request)

        paginator = Paginator(blogpages, self.paginate_by)
        page_number = request.GET.get("page", 1)
        page_obj = paginator.get_page(page_number)
        context["page_obj"] = page_obj
        context["tag"] = tag

        return context


# class BlogPageGalleryImage(Orderable):
#     page = ParentalKey(
#         BlogPage, on_delete=models.CASCADE, related_name="gallery_images"
#     )
#     image = models.ForeignKey(
#         "wagtailimages.Image", on_delete=models.CASCADE, related_name="+"
#     )
#     caption = models.CharField(blank=True, max_length=250)
#
#     panels = [
#         FieldPanel("image"),
#         FieldPanel("caption"),
#     ]
