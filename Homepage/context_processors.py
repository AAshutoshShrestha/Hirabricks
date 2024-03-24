from .models import *
from Inventory.models import BrickCategory

def base_context(request):
    socialmedia = SocialLink.objects.all()
    company_info = Company_info.objects.all()
    Team_info = TeamMember.objects.all()
    categories = BrickCategory.objects.all()
    context = {
        'SocialLink':socialmedia,
        'Company_info':company_info,
        'TeamMember':Team_info,
        'categories':categories,
    }
    return context