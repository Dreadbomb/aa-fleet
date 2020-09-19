# -*- coding: utf-8 -*-

"""
our app setting
"""

from .utils import clean_setting

# AA-GDPR / Avoid CDN setting
AVOID_CDN = clean_setting("AVOID_CDN", False)


# check if we should avoid CDNs, even if AA-GDPR is currently not active
# If the AVOID_CDN setting is set to true, we will anyways
# This should be implemented in every view that uses JS or CSS from a CDN
def avoid_cdn() -> bool:
    """
    Grab the AVOID_CDN setting and return its value
    :return: bool
    """
    return AVOID_CDN
