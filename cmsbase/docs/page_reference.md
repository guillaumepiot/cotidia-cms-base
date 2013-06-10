Page reference
==============

Properties
----------

`BasePage.siblings`: Returns all siblings from a given page (original not published version) including itself.


Method
----------

`BasePage.get_published()`: Returns the published version of an original page. If the page it's called from is a published version, then it returns `None`

`BasePage.translated()`: Returns the translated object of a given page, in the current language set.

`BasePage.get_translations()`: Returns all translation objects from a given page.

`BasePage.publish_translations()`: Publish transaltions of a given original page.

`BasePage.publish_version()`: Publish a given original page

`BasePage.unpublish_version()`: Un-publish a given original page

`BasePage.delete()`: Delete a given original page and its published version.

`BasePage.get_absolute_url()`: Construct a URL based on the page ancestor tree and returns it.

`BasePage.get_breadcrumbs()`: Returns a list of ancestor pages until the root page.

`BasePage.get_child_pages(include_self=False)`: Returns all the child pages of any given page. Return the current object as well if `include_self` equals `True`

- If the page object is original, all descendants are returned included un-published pages
- If the page object is a live version, only published descendants are returnes

`BasePage.get_root_page()`: Returns the root page from the ancestor tree of a given page.

`BasePage.images()`: Returns all the inline images of the original image. Please note that currently inline images are not part of the publishing workflow. Any uploaded images will be directly available from the published version as well.

`BasePage.feature_image()`: Returns the first image depending on the order_id. If no order_id has been specified, then the oldest image uploaded will be returned.
