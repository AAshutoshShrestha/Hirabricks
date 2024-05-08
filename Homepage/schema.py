import graphene
from graphene_django import DjangoObjectType

from .models import *


class ContactMessageType(DjangoObjectType):
    class Meta:
        model = ContactMessage
        fields = ("id", "name", "email", "message", "created_at")

class SocialLinkType(DjangoObjectType):
    class Meta:
        model = SocialLink
        fields = ("id", "name", "url", "icon")


class CompanyinfoType(DjangoObjectType):
    class Meta:
        model = Company_info
        fields = ("id", "name","address","phone_number","email")

class TeamMemberType(DjangoObjectType):
    class Meta:
        model = TeamMember
        fields = ("id", "name","position","image_url")



class Company_Info_Query(graphene.ObjectType):
	all_Company_info = graphene.List(CompanyinfoType)
	
	def resolve_all_Company_info(root,info):
		return Company_info.objects.all()

class TeamMember_Query(graphene.ObjectType):
	all_Team_members = graphene.List(TeamMemberType)
	
	def resolve_all_Team_members(root,info):
		return TeamMember.objects.all()

class ContactMessage_Query(graphene.ObjectType):
    all_contact_messages = graphene.List(ContactMessageType)
    
    def resolve_all_contact_messages(root, info):
        return ContactMessage.objects.all()

class SocialLink_Query(graphene.ObjectType):
    all_social_links = graphene.List(SocialLinkType)
    
    def resolve_all_social_links(root, info):
        return SocialLink.objects.all()


class Query(Company_Info_Query,TeamMember_Query,ContactMessage_Query, SocialLink_Query):
    pass

schema = graphene.Schema(query=Query)

