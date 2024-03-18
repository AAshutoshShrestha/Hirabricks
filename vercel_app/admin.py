from django.contrib import admin

class CustomAdminSite(admin.AdminSite):
    def get_app_list(self, request):
        app_list = super().get_app_list(request)
        # Define your custom order of app names
        custom_order = [
            'Authentication and Authorization',
            'docs',
            'example',
            'conditions',
            'Resources',
            'Machines'
        ]
        sorted_app_list = sorted(app_list, key=lambda x: custom_order.index(x['name']) if x['name'] in custom_order else float('inf'))
        return sorted_app_list

# Register your custom admin site
admin.site = CustomAdminSite()