Revision and versions
---------------------

The system use reversion to track page editions. Though, we create a clone of the page for the published version. 

The editable page will be tracked with reversion, and a published page will be an untracked cloned version of the edited page. The admin list of pages filters out published version to avoid confusion.

The page form has a publish option which when ticked, it will automatically generate a page clone or override the current clone.
