# Django Privacy Analytics

Django Privacy Analytics is a minimalist, performant, and privacy-focused analytics system that runs in your Django app.

### Do Not Track
Django Privacy Analytics fully respects the 'Do Not Track' (DNT) header; if a request has DNT enabled, Django Privacy Analytics _will not_ store a page view.

### Installation

1. Install Django Privacy Analytics by running `pip install django-privacy-analytics` or adding `django-privacy-analytics` to your `requirements.txt`
2. Add `privacy_analytics` to your `INSTALLED_APPS` setting.
3. Add `privacy_analytics.middleware.AnalyticsMiddleware` to your `MIDDLEWARE` setting, ideally somewhere towards the end (and after `AuthenticationMiddleware`).
4. Create the new necessary models by running `python3 manage.py migrate`.
5. _Optionally_ add a place to view the analytics by adding `path('analytics/', include('privacy_analytics.urls'))` to your URL routing configuration.

### Access

Currently, the dashboard is only visible to superusers. This will be configurable in a future version.

### Settings

In `settings.py`, you can set the following:

* `ANALYTICS_IGNORE_PATHS`: ignore requests whose paths start with members of this **list**
