from django.db import models

class District(models.Model):
    """
    This is our "Route Wealth" database.
    It will hold all the curated data for each district.
    """
    
    name = models.CharField(max_length=100, unique=True)
    
    top_sights = models.TextField(
        blank=True, 
        help_text="Enter a comma-separated list of sights."
    )
    
    famous_food = models.TextField(
        blank=True, 
        help_text="Enter a comma-separated list of famous foods/items."
    )

    def __str__(self):
        return self.name