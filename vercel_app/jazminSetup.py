JAZZMIN_SETTINGS ={
    "site_title": "Hirabricks",
    "site_header": "TunnelKiln",
    "site_brand": "Hirabricks",
    "site_logo_classes": "admin-logo",
    "site_logo":"image/factoryicon-white.png",
    
    "site_icon":"image/favicon.png",

    "copyright": "Aashutosh Shrestha © Hirabricks 2024",

    "navbar": "navbar-light",

    #############
    # Side Menu #
    #############

    "sidebar": "sidebar-light-orange",
    "show_sidebar" : True,
    "hide_apps": [],
    "order_with_respect_to": ["auth","Homepage","Inventory","docs","example","conditions","Resources","Machines"],

    "brand_colour": "navbar-orange",

    "usermenu_links": [
        {"model": "auth.user"}
    ],
    "custom_links": {
    "books": [{
        "name": "Make Messages"
    }]
    },

    "changeform_format": "horizontal_tabs",

    "topmenu_links": [

        # Url that gets reversed (Permissions can be added)
        {"name": "Open Dashboard",  "url": "/Dashboard", "permissions": ["auth.view_user"]},
        {"name": "Home page",  "url": "/", "permissions": ["auth.view_user"]},

        # Url that gets reversed (Permissions can be added)
        {"name": "Register",  "url": "/register", "permissions": ["auth.view_user"]},

        # App with dropdown menu to all its models pages (Permissions checked against models)
        {"app": "example"},

        # model admin to link to (Permissions checked against model)
        {"model": "auth.User"},
    ],

    'MENU_ICONS': True,
    'MENU_OPEN_FIRST_CHILD': True,

    "dark_mode_theme": None,
     "language_chooser": False,
     
}

JAZZMIN_UI_TWEAKS = {
    'MENU_COLLAPSED': True,
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": True,
    "brand_small_text": False,
    "brand_colour": False,
    "accent": "accent-danger",
    "navbar": "navbar-white navbar-light",
    "no_navbar_border": False,
    "navbar_fixed": True,
    "layout_boxed": False,
    "footer_fixed": True,
    "sidebar_fixed": True,
    "sidebar": "sidebar-dark-danger",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": True,
    "sidebar_nav_child_indent": True,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": True,
    "sidebar_nav_flat_style": False,
    "theme": "default",
    "dark_mode_theme": None,
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success"
    }
}
