from .models import *

from realestate.globals import logger
from users.models import CustomUser

from .helpers.helpers import order_by, where

class TermsRepository:
    # Main
    def find_or_create(self, data):
        # 2 Parametrized queries
        terms = Terms.objects.get_or_create(**data)[0]

        # 5 Security logging
        logger.info("New terms with given data fetched or added to the database.")
        return terms

    def update(self, terms: Terms, data):
        # 2 Parametrized queries
        Terms.objects.filter(pk=terms.pk).update(**data)

        # 5 Security logging
        logger.info("Terms with the ID %d updated in the database.", terms.pk)

    def delete(self, terms: Terms):
        # 2 Parametrized queries
        if Listing.objects.filter(terms__pk=terms.pk).count() == 0:
            terms.delete()
            
            # 5 Security logging
            logger.warning("Terms with the ID %d deleted from the database.", terms.pk)


class ListingRepository:
    # Main
    def find_all(self, order: str):
        # 2 Parametrized queries
        listings = Listing.objects.all().order_by(order_by(order))

        # 5 Security logging
        logger.info("Listings fetched from the database.")
        return listings
    
    def find_by_pk(self, pk: int):
        # 2 Parametrized queries
        listing = Listing.objects.get(pk=pk)
        
        # 5 Security logging
        logger.info("Listings fetched from the database.")
        return listing

    def create(self, items, terms: Terms, poster: CustomUser, data):
        # 2 Parametrized queries
        listing = Listing.objects.create(**data, terms=terms, poster=poster)
        listing.items.set(items)

        # 5 Security logging
        logger.info("New listing added to the database.")

    def update(self, items, listing: Listing, data):
        # 2 Parametrized queries
        Listing.objects.filter(pk=listing.pk).update(**data)
        listing.items.set(items)

        # 5 Security logging
        logger.info("Listing with the ID %d updated in the database.", listing.pk)

    def delete(self, listing: Listing):
        # 2 Parametrized queries
        listing.items.clear()
        listing.saves.clear()
        listing.delete()

        # 5 Security logging
        logger.warning("Listing with the ID %d deleted from the database.", listing.pk)

    # Other
    def filter(self, data, order: str):
        # 2 Parametrized queries
        listings = Listing.objects.filter(where(data)).order_by(order_by(order))

        # 5 Security logging
        logger.info("Listing with the query fetched from the database.")
        return listings

    def find_by_user(self, user: CustomUser, order: str):
        # 2 Parametrized queries
        listings = Listing.objects.filter(poster=user).order_by(order_by(order))
        
        # 5 Security logging
        logger.info("Listings of %s deleted from the database.")
        return listings
    
    def find_saved(self, user: CustomUser, order: str):
        # 2 Parametrized queries
        listings = Listing.objects.filter(saves=user.pk).order_by(order_by(order))

        # 5 Security logging
        return listings
    
    def save(self, listing: Listing, user: CustomUser):
        # 2 Parametrized queries
        if listing.is_saved(user):
            listing.saves.add(user)


terms_repo = TermsRepository()
listing_repo = ListingRepository()