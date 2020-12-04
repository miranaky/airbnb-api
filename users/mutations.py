import graphene
from users.models import User


class CreateUserMutaion(graphene.Mutation):
    class Arguments:
        first_name = graphene.String()
        last_name = graphene.String()
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    ok = graphene.Boolean()
    error = graphene.String()

    def mutate(self, info, email, password, first_name=None, last_name=None):
        try:
            User.objects.get(email=email)
            return CreateUserMutaion(ok=False, error="User already exist.")
        except User.DoesNotExist:
            try:
                User.objects.create_user(email, email, password)
                return CreateUserMutaion(ok=True)
            except Exception:
                return CreateUserMutaion(ok=False, error="Can't create User.")
