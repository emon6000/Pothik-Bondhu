# main/models.py

from django.db import models

class District(models.Model):
    """
    This is our "Route Wealth" database.
    It will hold all the curated data for each district.
    """
    
    # Example: "Cumilla"
    name = models.CharField(max_length=100, unique=True)
    
    # We use a TextField because you might want to add a lot of sights.
    # We will store them as a comma-separated list.
    # Example: "Shalban Bihar, Maynamati Museum, Dharma Sagar Dighi"
    top_sights = models.TextField(
        blank=True, 
        help_text="Enter a comma-separated list of sights."
    )
    
    # Example: "Rosh malai (from Matri Bhandar), Khadi Fabrics"
    famous_food = models.TextField(
        blank=True, 
        help_text="Enter a comma-separated list of famous foods/items."
    )

    def __str__(self):
        # This just tells Django to use the district's name
        # as its label in the admin panel, which is very helpful.
        return self.name