from django.contrib.auth import get_user_model
import graphene
from graphene_django import DjangoObjectType
from graphql_jwt.decorators import login_required, staff_member_required, superuser_required

class UserType(DjangoObjectType):
	class Meta:
		model = get_user_model()

class Query(graphene.ObjectType):
	users =graphene.List(UserType)
	user = graphene.Field(UserType,id=graphene.Int(required=True))
	me = graphene.Field(UserType)

	@login_required
	def resolve_users(self,info):
		return get_user_model().objects.all()

	def resolve_user(self,info,id):
		return get_user_model().objects.get(id=id)

	@login_required
	def resolve_me(self,info):
		user = info.context.user

		if user.is_anonymous:
			raise Exception('Not Logged In !')

		return user


class CreateUser(graphene.Mutation):
	user = graphene.Field(UserType)

	class Arguments:
		username = graphene.String(required=True)
		password = graphene.String(required=True)
		email = graphene.String(required=True)


	def mutate(self,info,username,password,email):
		user = get_user_model()(
			username=username,
			email=email,
			password=password
			)
		user.set_password(password)
		user.save()

		return CreateUser(user=user)

### Update Category
class UserUpdate(graphene.Mutation):
    class Arguments:
        # The input arguments for this mutation
        username = graphene.String(required=True)
        email = graphene.String(required=True)
        password = graphene.String(required=True)
        id = graphene.ID()

    # The class attributes define the response of the mutation
    user = graphene.Field(UserType)

    def mutate(self, info, username,email,password, id):
        user = get_user_model().objects.get(pk=id)
        user.username = username
        user.email = email
        user.password = password
        user.save()
        # Notice we return an instance of this mutation
        return UserUpdate(user=user)

# Delete Category
class Deleteuser(graphene.Mutation):
	class Arguments:
		id = graphene.ID()

	user = graphene.Field(UserType)

	def mutate(root, info, **kwargs):
		obj = get_user_model().objects.get(pk=kwargs["id"])
		obj.delete()
		# return cls(ok=True)
		return Deleteuser(user=obj)

class Mutation(graphene.ObjectType):
	create_user = CreateUser.Field()
	update_user = UserUpdate.Field()
	delete_user = Deleteuser.Field()