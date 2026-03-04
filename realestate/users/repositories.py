from django.contrib.auth.hashers import check_password, make_password

from .models import CustomUser

from realestate.globals import logger

class UserRepository:
    # Main
    def find_by_pk(self, pk):
        # 1 Parametrized queries
        user = CustomUser.objects.get(pk=pk)

        # 5 Security logging
        logger.info("User with the ID %d fetched from the database.", pk)
        return user
        
    def create(self, data):
        password = make_password(data["password1"])

        # 1 Parametrized queries
        user = CustomUser.objects.create(
            email=data["email"],
            password=password,
            phone=data["phone"],
            first_name=data["first_name"],
            last_name=data["last_name"],
            birth_date=data["birth_date"]
        )

        # 5 Security logging
        logger.info("User with the given data added to the database.")
        return user
    
    def update(self, user: CustomUser, data):
        # 1 Parametrized queries
        if "password" in data:
            password = make_password(data["password"])
            CustomUser.objects.filter(pk=user.pk).update(email=data["email"], password=password)
        else:
            CustomUser.objects.filter(pk=user.pk).update(email=data["email"])
        
        # 5 Security logging
        logger.info("Credentials of user with the ID %d updated in the database.", user.pk)
    
    def update2(self, user: CustomUser, data):
        # 1 Parametrized queries
        CustomUser.objects.filter(pk=user.pk).update(
            phone=data["phone"],
            first_name=data["first_name"],
            last_name=data["last_name"],
            birth_date=data["birth_date"]
        )

        # 5 Security logging
        logger.info("User with the ID %d updated in the database.", user.pk)
    
    def delete(self, user: CustomUser):
        # 1 Parametrized queries
        user.delete()

        # 5 Security logging
        logger.warning("User with the ID %d deleted from the database.", user.pk)
    
    # Other
    def find_by_email(self, email):
        # 1 Parametrized queries
        user = CustomUser.objects.get(email=email)

        # 5 Security logging
        logger.info("User with the email address %s fetched from the database.", email)
        return user

    def is_registered(self, email):
        user = self.find_by_email(email)
        return user and user.email and user.email.strip() != ""
    
    def passwords_match(self, password, password2):
        return check_password(password, password2)

user_repo = UserRepository()