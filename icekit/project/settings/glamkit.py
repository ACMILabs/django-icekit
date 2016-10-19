from .icekit import *

# DJANGO ######################################################################

INSTALLED_APPS += (
    'sponsors',
    'press_releases',

    'icekit_events',
    'icekit_events.event_types.simple',
    'icekit_events.page_types.eventlistingfordate',
)

ROOT_URLCONF = "icekit.project.glamkit_urls"

# ICEKIT PRESS RELEASES #######################################################

ICEKIT['DASHBOARD_FEATURED_APPS'][0]['models'].update({
    'icekit_press_releases.PressRelease': {
        'verbose_name_plural': 'Press releases',
    },
})

# ICEKIT EVENTS ###############################################################

ICEKIT['DASHBOARD_FEATURED_APPS'] = (
    {
        'verbose_name': 'Events',
        'icon_html': '<i class="content-type-icon fa fa-calendar-o"></i>',
        'models': {
            'icekit_events.EventBase': {
            },
        },
    },


) + ICEKIT['DASHBOARD_FEATURED_APPS']


# GLAMKIT SPONSORS ############################################################
_SPONSOR_PLUGINS = [
    'BeginSponsorBlockPlugin',
    'EndSponsorBlockPlugin',
    'SponsorPromoPlugin',
]
DEFAULT_PLUGINS += _SPONSOR_PLUGINS

# CONFIGURE PLACEHOLDERS ######################################################

FLUENT_CONTENTS_PLACEHOLDER_CONFIG.update({
    'main': {'plugins': DEFAULT_PLUGINS },
    'pressrelease_contacts': {
        'plugins': (
            'ContactItemPlugin',
            'TextPlugin',
        ),
    },
})
