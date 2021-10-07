from django.http import HttpResponse

from wagtail.contrib.routable_page.models import RoutablePage, route


def routable_page_external_view(request, arg="ARG NOT SET"):
    return HttpResponse("EXTERNAL VIEW: " + arg)


class RoutablePageTest(RoutablePage):
    @route(r"^archive/year/1984/$")
    def archive_for_1984(self, request):
        # check that routes are tested in order (and thus this takes precedence over archive_by_year)
        return HttpResponse("we were always at war with eastasia")

    @route(r"^archive/year/(\d+)/$")
    def archive_by_year(self, request, year):
        return HttpResponse("ARCHIVE BY YEAR: " + str(year))

    @route(r"^archive/author/(?P<author_slug>.+)/$")
    def archive_by_author(self, request, author_slug):
        return HttpResponse("ARCHIVE BY AUTHOR: " + author_slug)

    @route(r"^external/(.+)/$")
    @route(r"^external-no-arg/$")
    def external_view(self, *args, **kwargs):
        return routable_page_external_view(*args, **kwargs)

    # By default, the method name would be used as the url name but when the
    # "name" kwarg is specified, this should override the default.
    @route(r"^override-name-test/$", name="name_overridden")
    def override_name_test(self, request):
        pass

    @route(r"^render-method-test/$")
    def render_method_test(self, request):
        return self.render(request, context_overrides={"self": None, "foo": "bar"})

    @route(r"^render-method-test-custom-template/$")
    def render_method_test_custom_template(self, request):
        return self.render(
            request,
            context_overrides={"self": 1, "foo": "fighters"},
            template="routablepagetests/routable_page_test_alternate.html",
        )

    def get_route_paths(self):
        return [
            "/",
            "/render-method-test/",
            "not-a-valid-route",
        ]


class RoutablePageWithOverriddenIndexRouteTest(RoutablePage):
    @route(r"^$")
    def main(self, request):
        return HttpResponse("OVERRIDDEN INDEX ROUTE title=" + self.title)
