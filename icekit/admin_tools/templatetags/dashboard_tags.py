from django import template
from django.apps import apps
from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.db.models.loading import get_model
from django.template.defaultfilters import stringfilter

from icekit import appsettings

register = template.Library()


@register.filter
@stringfilter
def obtain_content_type_id(model_name, app_label):
    """
    Obtains the content type id from the name of a content type.
    :param model_name: The name of the model to look for.
    :param app_label: The name off the app to look for.
    :return: Positive integer id
    """
    return ContentType.objects.get_for_model(get_model(app_label, model_name)).id


class AppObject(object):
    """
    Used by `filter_featured_apps` to assign generic properties to.
    """
    pass


def models_key(model):
    """
    Return verbose name (plural), verbose name, or model name, to use as a
    comparison key when sorting.
    """
    return model.get(
        'verbose_name', model.get(
            'verbose_name_plural', model['object_name']))


@register.filter
def filter_featured_apps(admin_apps, request):
    """
    Given a list of apps return a set of pseudo-apps considered featured.

    Apps are considered featured if the are defined in the settings
    property called `DASHBOARD_FEATURED_APPS` which contains a list of the apps
    that are considered to be featured.

    :param admin_apps: A list of apps.
    :param request: Django request.
    :return: Subset of app like objects that are listed in
    the settings `DASHBOARD_FEATURED_APPS` setting.
    """
    featured_apps = []

    # Build the featured apps list based upon settings.
    for featured_app in appsettings.DASHBOARD_FEATURED_APPS:
        # Create a new pseudo-app-like object we can add attributes to.
        new_app = AppObject()

        # Assign the verbose name to use for the app.
        setattr(new_app, 'verbose_name', featured_app['verbose_name'])
        # Assign the icon to use for the app.
        setattr(new_app, 'icon_html', featured_app['icon_html'])

        # Initial set the models to be empty.
        new_app.models = []

        # Search through each app for the models and change the verbose name,
        # adding it to the models list for a pseudo-app instance.
        for app_and_model, config in featured_app['models'].items():
            app_label, model_name = app_and_model.split('.')

            for app in admin_apps:
                if app['app_label'] == app_label:
                    for model in app['models']:
                        if model['object_name'] == model_name:
                            try:
                                model['verbose_name'] = \
                                    config['verbose_name']
                            except KeyError:
                                pass
                            try:
                                model['verbose_name_plural'] = \
                                    config['verbose_name_plural']
                            except KeyError:
                                pass
                            # Get each of the polymorphic types to allow addition.
                            model_class = apps.get_model(app_and_model)
                            model_admin = admin.site._registry[model_class]

                            if hasattr(model_admin, 'get_child_type_choices'):
                                model['polymorphic_classes'] = model_admin.get_child_type_choices(
                                    request,
                                    'add'
                                )

                            if 'default_poly_child' in config.keys():
                                ct = ContentType.objects.get_by_natural_key(
                                    *config['default_poly_child'].lower().split('.')
                                )

                                new_app.default_poly_child = ct.id

                            new_app.models.append(model)

                    break

        # Only add the panel if at least one model is listed.
        if new_app.models:
            featured_apps.append(new_app)

    return featured_apps


@register.filter
def partition_app_list(app_list, n):
    """
    :param app_list: A list of apps with models.
    :param n: Number of buckets to divide into.
    :return: Partition apps into n partitions, where the number of models in each list is roughly equal. We also factor
    in the app heading.
    """
    num_rows = sum([1 + len(x['models']) for x in app_list]) # + 1 for app title
    num_rows_per_partition = num_rows / n

    result = [[] for i in range(n)] # start with n empty lists of lists
    partition = 0
    count = 0

    for a in app_list:
        # will the app fit in this column or overflow?
        c = len(a['models']) + 1 # the +1 is for the app title
        if (partition + 1 < n) and (count + (c/n) > num_rows_per_partition): # if we're not on the last column, and we overflowed
            # overflow
            partition += 1
            count = 0
        result[partition].append(a)
        count += c

    return result