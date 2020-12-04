from django.contrib.auth import authenticate
from django.conf import settings
import graphene
import jwt
from users.models import User


class CreateUserMutaion(graphene.Mutation):
    class Arguments:
        first_name = graphene.String()
        last_name = graphene.String()
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    ok = graphene.Boolean()
    error = graphene.String()

    def mutate(root, info, email, password, first_name=None, last_name=None):
        try:
            User.objects.get(email=email)
            return CreateUserMutaion(ok=False, error="User already exist.")
        except User.DoesNotExist:
            try:
                User.objects.create_user(email, email, password)
                return CreateUserMutaion(ok=True)
            except Exception:
                return CreateUserMutaion(ok=False, error="Can't create User.")


class UserLoginMutation(graphene.Mutation):
    class Arguments:
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    token = graphene.String()
    error = graphene.String()
    pk = graphene.Int()

    def mutate(root, info, email, password):
        user = authenticate(username=email, password=password)
        if user:
            token = jwt.encode({"pk": user.pk}, settings.SECRET_KEY, algorithm="HS256")
            return UserLoginMutation(token=token.decode("utf-8"), pk=user.pk)
        else:
            return UserLoginMutation(error="Username/Password is wrong")