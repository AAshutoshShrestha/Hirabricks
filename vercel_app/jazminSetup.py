JAZZMIN_SETTINGS = {
    # Site settings
    "site_title": "Hirabricks",
    "site_header": "TunnelKiln",
    "site_brand": "Hirabricks",
    "site_logo_classes": "admin-logo",
    "site_logo": "image/factoryicon-white.png",
    "site_icon": "image/favicon.png",
    "copyright": "Aashutosh Shrestha © Hirabricks 2024",

    # Navbar settings
    "navbar": "navbar-light",

    # Sidebar settings
    "sidebar": "sidebar-light-orange",
    "show_sidebar": True,
    "hide_apps": [],
    "order_with_respect_to": ["auth", "Homepage", "Inventory", "docs", "example", "conditions", "Resources", "Machines"],
    "brand_colour": "navbar-orange",

    # User menu settings
    "usermenu_links": [{"model": "auth.user"}],
    "custom_links": {"books": [{"name": "Make Messages"}]},

    # Form settings
    "changeform_format": "horizontal_tabs",

    # Top menu settings
    "topmenu_links": [
        {"name": "Open Dashboard", "url": "/Dashboard", "permissions": ["auth.view_user"]},
        {"name": "Home page", "url": "/", "permissions": ["auth.view_user"]},
        {"name": "Register", "url": "/register", "permissions": ["auth.view_user"]},
        {"app": "example"},
        {"model": "auth.User"},
    ],

    # UI tweaks
    "MENU_ICONS": True,
    "MENU_OPEN_FIRST_CHILD": True,
    "dark_mode_theme": None,
    "language_chooser": False,
}

JAZZMIN_UI_TWEAKS = {
    # Navbar and sidebar settings
    "MENU_COLLAPSED": True,
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

    # Button classes
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success"
    }
}
