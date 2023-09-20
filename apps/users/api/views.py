from rest_framework import status  # noqa: F401
from rest_framework.decorators import action  # noqa: F401
from rest_framework.permissions import AllowAny
from rest_framework.response import Response  # noqa: F401
from rest_framework.viewsets import ModelViewSet
from djoser.compat import get_user_email


from .serializers import (
    UserSerializer,
    InviteUserSerializer,
    InviteUserActivationSerializer,
    ProfileSerializer,
    SettingSerializer,
)
from apps.users.models import User, Profile, Settings
from apps.users.email import InvitationEmail, ConfirmationEmail


class UserViewset(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_queryset(self):
        user = self.get_instance()
        queryset = super().get_queryset()
        # TODO: JUST RETURN USERS OF THE SAME ACCOUNT AND OR COLLABORATION GROUP
        return queryset

    def get_permissions(self):
        """remove require auth permission on invited user activation view."""
        if self.action == "activation":
            self.permission_classes = [AllowAny]
        return super().get_permissions()

    def get_instance(self):
        return self.request.user

    def perform_create(self, serializer):
        user = serializer.save(created_by=self.request.user)
       
    def get_serializer(self, *args, **kwargs):
        if isinstance(kwargs.get("data", {}), list):
            kwargs["many"] = True
        return super().get_serializer(*args, **kwargs)

    def get_serializer_class(self):
        if self.action == "create":
            return UserSerializer
        elif self.action == "invitation":
            return InviteUserSerializer
        elif self.action == "activation":
            return InviteUserActivationSerializer
        elif self.action == "resend_invitation":
            raise NotImplementedError("This Functionality has not been implimented")
        return self.serializer_class

    @action(methods=["POST"], detail=False)
    def invitation(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data, context={"request": request}
        )
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        user = serializer.save(created_by=request.user)

        # send email to user
        context = {"user": user, "from_user": request.user.email}
        to = [get_user_email(user)]
        try:
            InvitationEmail(self.request, context).send(to)
        except (Exception) as e:
            print(str(e))
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(methods=["POST"], detail=True)
    def resend_invitation(self, request, id=None, *args, **kwargs):
        # TODO: IN FRONTEND FOR USER HAVE LIST ON INVITATIONS AND OPTION TO RESEND
        raise NotImplementedError("This method has not been implimented")

    @action(methods=["POST"], detail=False)
    def activation(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.user
        user.set_password(serializer.data["new_password"])
        user.is_active = True
        user.save()
        # TODO: SEND EMAIL TO USER AND NOTIFICATION TO INVITEE
        
        context = {"user": user}
        to = [get_user_email(user)]
        try:
            ConfirmationEmail(self.request, context).send(to)
        except Exception as e:
            print(str(e))

        return Response(status=status.HTTP_204_NO_CONTENT)


class UserProfileViewset(ModelViewSet):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()


class UserSettingsViewset(ModelViewSet):
    serializer_class = SettingSerializer
    queryset = Settings.objects.all()
