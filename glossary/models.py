from django.db import models
from django.core.exceptions import ValidationError

class GlossaryEntry(models.Model):
    # Defines a model for an entry in the glossary that is displayed in the app.
    term    = models.CharField(max_length=100)
    text    = models.TextField()
    img     = models.ImageField(upload_to="glossary/images/", null=True, blank=True)
    img_alt = models.CharField(max_length=200, blank=True, default="", validators=[validate_img_is_not_empty])
    links   = models.ManyToManyField("self", symmetrical=False, blank=True)
    
    # Validation if an image is used but no alternate text is specified for the image.
    def validate_img_is_not_empty(img, img_alt):
        if len(img) > 0 and len(img_alt) < 1:
            raise ValidationError(_("No alternate text specified for the image."))
            
