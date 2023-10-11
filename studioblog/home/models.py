from blog.models import BlogPage
from django.core.paginator import Paginator
from django.db import models
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase

from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField
from wagtail.models import Page, ParentalKey
from wagtail.search import index
from wagtail.search.backends import get_search_backend

# TODO: add htmx in the usual way


class HomePage(Page):
    intro = RichTextField(blank=True)
    intro_title = models.CharField(max_length=250, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("intro_title"),
        FieldPanel("intro"),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["recent_posts"] = BlogPage.objects.live().order_by("-date")[:5]
        context["featured_tools"] = PracticeToolPage.objects.live().filter(
            featured=True
        )
        return context


class PracticeToolTag(TaggedItemBase):
    content_object = ParentalKey(
        "PracticeToolPage", related_name="tagged_items", on_delete=models.CASCADE
    )


# TODO: add video demos


class PracticeToolPage(Page):
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


class PracticeToolIndexPage(Page):
    intro = RichTextField(blank=True)
    content_panels = Page.content_panels + [
        FieldPanel("intro"),
    ]

    paginate_by = 20

    def get_context(self, request):
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


# TODO: make this pretty
class PracticeToolTagIndexPage(Page):
    def get_context(self, request):
        tag = request.GET.get("tag")
        practice_tools = PracticeToolPage.objects.filter(tags__name=tag)

        context = super().get_context(request)

        paginator = Paginator(practice_tools, self.paginate_by)
        page_number = request.GET.get("page", 1)
        page_obj = paginator.get_page(page_number)
        context["page_obj"] = page_obj
        context["tag"] = tag

        return context
