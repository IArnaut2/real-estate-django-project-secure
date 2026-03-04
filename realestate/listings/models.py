from django.db import models

# Create your models here.
class Item(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        db_table = "item"

    def __str__(self):
        return self.name
 
class Terms(models.Model):
    move_in_date = models.DateField()
    deposit = models.BooleanField()
    for_students = models.BooleanField()
    for_workers = models.BooleanField()
    smoking_allowed = models.BooleanField()
    pets_allowed = models.BooleanField()

    class Meta:
        db_table = "terms"

class Listing(models.Model):
    # Address
    city = models.CharField(max_length=255)
    street = models.CharField(max_length=255)

    # Building
    story_count = models.PositiveIntegerField()
    elevator = models.BooleanField()
    parking = models.BooleanField()
    garage = models.BooleanField()
    cctv = models.BooleanField()
    intercom = models.BooleanField()

    # Apartment
    room_count = models.PositiveIntegerField()
    area = models.PositiveIntegerField()
    story = models.PositiveIntegerField()
    condition = models.CharField(max_length=255)
    heating = models.CharField(max_length=255)
    furnishings = models.CharField(max_length=255)
    
    # Listing
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    items = models.ManyToManyField(Item, blank=True)
    saves = models.ManyToManyField("users.CustomUser", related_name="listing_saves", blank=True)
    terms = models.ForeignKey(Terms, on_delete=models.CASCADE)
    poster = models.ForeignKey("users.CustomUser", on_delete=models.CASCADE, db_column="poster_id")

    class Meta:
        db_table = "listing"

    def get_address(self):
        return f"{self.street}, {self.city}"

    def get_room_count(self):
        return self.room_count if self.room_count > 0 else "Garsonjera"
    
    def get_story(self):
        return "Prizemlje" if self.story == 0 else self.story
    
    def get_area(self):
        return f"{self.area} m2"
    
    def get_story(self):
        story = self.story if self.story > 0 else "Prizemlje"
        return f"{story}/{self.story_count}"
    
    def get_move_in_date(self):
        comparison = self.terms.move_in_date > self.created_at
        date = self.terms.move_in_date.strftime("%d.%m.%Y")
        text = date if comparison else "odmah"
        return f"Useljiv {text}"
    
    def get_price(self):
        return f"{self.price} EUR"
    
    def is_updated(self):
        return self.updated_at > self.created_at
    
    def is_saved(self, user):
        return self.saves.filter(pk=user.pk).exists()

    def __str__(self):
        return self.title
