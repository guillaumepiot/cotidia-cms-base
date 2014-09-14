---
layout: page
title: Moderation
permalink: "moderation.html"
---

Moderation
==========

User levels
-----------

- Administrator - full feature access and power to publish (Superuser or has "can_publish" permission)

- Editor - can edit content but can not publish (not Superuser and do not have "can_publish" permission)



The page model bear a specific permission for publishing ("can_publish"). This way any non-superuser bearing that permission will have the power to publish content.

The text editor used by default is redactor. You can use the one by Cotidia, but you will need to get your own license. http://imperavi.com/redactor/


Publishing
----------

We differentiate between published pages and draft pages by setting the published option:

- True: The page will be hidden from the result list in the backend and will be use to render the live content
- False: The page is displayed and editable from the CMS

There are 2 more boolean which are there purely to command publishing and approval:

- Publish: it will trigger the generation of a clone published page
- Approval: it will trigger an email (to do!) to whoever has published permission to notify them about the new page.


Revision and versions
---------------------

The system use reversion to track page editions. Though, we create a clone of the page for the published version. 

The editable page will be tracked with reversion, and a published page will be an untracked cloned version of the edited page. The admin list of pages filters out published version to avoid confusion.

The page form has a publish option which when ticked, it will automatically generate a page clone or override the current clone.