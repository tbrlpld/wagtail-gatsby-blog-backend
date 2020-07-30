# -*- coding: utf-8 -*-

"""
Mixin for Wagtail Page model to serve pages from a separate host.

There is only one class defined and that is the HeadlessServeMixin. This
mixin does nothing but overrides the serve method of a Wagtail Page to serve
the same page URL but from a separate host.

This is helpful for headless configurations, where only the data is defined in
Wagtail but no templates are defined. In such a setup, the frontend is
typically served from a separate host.

In such a setup, the 'Live' or 'View Live' button in the Wagtail Admin would
lead to a '404' or (in debug mode) 'Template not found' error. To prevent this
error, the pages need to know that they are not served by Wagtail is self, but
from a different host. This is what the defined mixin allows.

"""

from django import shortcuts as djshrt  # type: ignore
from django import http as djhttp
from wagtail.core import models as wtcm  # type: ignore


class HeadlessServeMixin(object):
    """
    Mixin overriding the default serve method with a redirect.

    The URL of the requested page is kept the same, only this host is
    overridden. To control which host the redirect should lead to, use
    the SERVE_HEADLESS_WAGTAIL_HOST setting.
    """

    def serve(
        self: wtcm.Page,
        request: djhttp.HttpRequest,
    ) -> djhttp.HttpResponse:
        """
        Override for the Wagtail Page `serve` method that returns a redirect.

        Parameters
        ----------
        request: django.http.HttpRequest
            Django request object to extract the requested page URL from.

        Returns
        -------
        django.http.HttpResonse
            Django response redirecting to the host serving the headless pages.
        """
        site_id, site_root, relative_page_url = self.get_url_parts(request)
        return djshrt.redirect(
            'http://localhost:8001{0}'.format(relative_page_url),
        )
