import graphene
from graphene_django import DjangoObjectType

from .models import Company_info,TeamMember

class CompanyinfoType(DjangoObjectType):
    class Meta:
        model = Company_info
        fields = ("id", "name","address","phone_number","email")

class Company_Info_Query(graphene.ObjectType):
	all_Company_info = graphene.List(CompanyinfoType)
	
	def resolve_all_Company_info(root,info):
		return Company_info.objects.all()

schema = graphene.Schema(query=Company_Info_Query)


class TeamMemberType(DjangoObjectType):
    class Meta:
        model = TeamMember
        fields = ("id", "name","position","image_url")

class TeamMember_Query(graphene.ObjectType):
	all_Team_members = graphene.List(TeamMemberType)
	
	def resolve_all_Team_members(root,info):
		return TeamMember.objects.all()

schema = graphene.Schema(query=TeamMember_Query)