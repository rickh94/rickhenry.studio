from blog.models import BlogPage
from django.core.paginator import Paginator
from django.db import models
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase
from wagtail import blocks
from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField, StreamField
from wagtail.images.blocks import ImageChooserBlock
from wagtail.models import Page, ParentalKey
from wagtail.search import index
from wagtail.search.backends import get_search_backend

from studioblog.blocks import ABCBlock, AudioBlock
from studioblog.types import HtmxHttpRequest, WagtailPageManager


class HomePage(Page):
    intro = RichTextField(blank=True)
    intro_title = models.CharField(max_length=250, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("intro_title"),
        FieldPanel("intro"),
    ]

    def get_context(self, request: HtmxHttpRequest, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["recent_posts"] = BlogPage.objects.live().order_by("-date")[:5]
        context["featured_tools"] = PracticeToolPage.objects.live().filter(
            featured=True
        )
        return context

    def get_template(self, request: HtmxHttpRequest, *args, **kwargs):
        if request.htmx and not request.htmx.boosted:
            return "home/htmx/home_page.html"
        else:
            return "home/home_page.html"


class AboutPage(Page):
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

    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]

    def get_template(self, request: HtmxHttpRequest, *args, **kwargs):
        if request.htmx and not request.htmx.boosted:
            return "home/htmx/about_page.html"
        else:
            return "home/about_page.html"


class PracticeToolTag(TaggedItemBase):
    content_object = ParentalKey(
        "PracticeToolPage", related_name="tagged_items", on_delete=models.CASCADE
    )


# TODO: add video demos


class PracticeToolPage(Page):
    objects: WagtailPageManager
    short_description = RichTextField(blank=True)
    long_description = RichTextField(blank=True)
    tags = ClusterTaggableManager(through=PracticeToolTag, blank=True)
    location = models.URLField(blank=True)
    featured = models.BooleanField(default=False)

    content_panels = Page.content_panels + [
        FieldPanel("location"),
        FieldPanel("short_description"),
        FieldPanel("long_description"),
        FieldPanel("tags"),
        FieldPanel("featured"),
    ]

    search_fields = Page.search_fields + [
        index.SearchField("short_description"),
        index.SearchField("long_description"),
    ]

    def get_template(self, request: HtmxHttpRequest, *args, **kwargs):
        if request.htmx and not request.htmx.boosted:
            return "home/htmx/practice_tool_page.html"
        else:
            return "home/practice_tool_page.html"


class PracticeToolIndexPage(Page):
    intro = RichTextField(blank=True)
    content_panels = Page.content_panels + [
        FieldPanel("intro"),
    ]

    paginate_by = 20

    def get_context(self, request: HtmxHttpRequest):
        """Handles pagination and search for live blog pages"""
        context = super().get_context(request)
        practice_tool_list = PracticeToolPage.objects.live().order_by("title")

        if request.GET.get("q"):
            q = request.GET.get("q")
            s = get_search_backend()
            practice_tool_list = s.search(q, practice_tool_list)
            context["q"] = q

        paginator = Paginator(practice_tool_list, self.paginate_by)
        page_number = request.GET.get("page", 1)
        page_obj = paginator.get_page(page_number)
        context["page_obj"] = page_obj

        return context

    def get_template(self, request: HtmxHttpRequest, *args, **kwargs):
        if request.htmx and not request.htmx.boosted:
            return "home/htmx/practice_tool_index_page.html"
        else:
            return "home/practice_tool_index_page.html"


class PracticeToolTagIndexPage(Page):
    paginate_by = 20

    def get_context(self, request: HtmxHttpRequest):
        tag = request.GET.get("tag")
        practice_tools = PracticeToolPage.objects.live().filter(tags__name=tag)

        context = super().get_context(request)

        paginator = Paginator(practice_tools, self.paginate_by)
        page_number = request.GET.get("page", 1)
        page_obj = paginator.get_page(page_number)
        context["page_obj"] = page_obj
        context["tag"] = tag

        return context

    def get_template(self, request, *args, **kwargs):
        if request.htmx and not request.htmx.boosted:
            return "home/htmx/practice_tool_tag_index_page.html"
        else:
            return "home/practice_tool_tag_index_page.html"
