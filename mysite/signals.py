# -*- coding: utf-8 -*-

import os

import logging
import requests
from wagtail.core import signals as wtcsig  # type: ignore[import]


logger = logging.getLogger(__name__)


def trigger_netlify_build_hook(sender, **kwargs):
    """Tigger Netlify build hook."""
    instance = kwargs['instance']
    logger.info(
        'Netlify build tiggered by: {0} - {1}'.format(sender, instance)
    )
    netlify_build_hook_url = os.getenv('NETLIFY_BUILD_HOOK_URL')
    if not netlify_build_hook_url:
        logger.error(
            'No environment variable NETLIFY_BUILD_HOOK_URL found. '
            + 'Can not trigger frontend build.',
        )
        return None
    response = requests.post(netlify_build_hook_url, data={})
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as error:
        logger.error(
            'Received error response from Netlify build hook:\n'
            + '\t{0}'.format(error),
        )
    else:
        logger.info('Netlify build hook triggered successfully.')


wtcsig.page_published.connect(trigger_netlify_build_hook)
