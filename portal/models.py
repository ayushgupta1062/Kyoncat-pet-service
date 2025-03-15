from django.db import models
from kyonkat.models import AuditFields, MetaFields
from django.contrib.auth.models import User
from enum import IntEnum

class NAVIGATIONTYPE(IntEnum):
    TOP_MENU = 0

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]
    
    
class MENUTYPE(IntEnum):
    PAGE                = 0
    BLOG                = 1
    SERVICES            = 2
    GALLERY             = 3

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]

class POSITION(IntEnum):
    NONE = 0
    LEFT = 1
    RIGHT = 2

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]


class PAGESECTION(IntEnum):
    DEFAULT     = 0
    SERVICE     = 1
    BLOG        = 2
    CLIENT      = 3
    GALLERY     = 4
    TESTIMOIALS = 5

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]


class Navigation(AuditFields, MetaFields):
    type        = models.PositiveSmallIntegerField(choices=NAVIGATIONTYPE.choices(), default=NAVIGATIONTYPE.TOP_MENU)
    menu        = models.PositiveSmallIntegerField(choices=MENUTYPE.choices(), default=MENUTYPE.PAGE)
    priority    = models.PositiveSmallIntegerField(default=0)
    name        = models.CharField(max_length=255, blank=False, null=False)
    level       = models.PositiveIntegerField(default=0)
    parent      = models.ForeignKey("self", on_delete = models.DO_NOTHING, blank=True, null=True)
    banner      = models.ImageField(blank=True, null=True)
    is_active   = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'navigation'
        verbose_name = 'Navigation'
        verbose_name_plural = 'Navigations'
    
    def __str__(self):
        return str(self.name)
 
class Pages(AuditFields):
    navigation      = models.ForeignKey(Navigation, on_delete=models.DO_NOTHING, blank=True, null=True)
    page_section    = models.PositiveSmallIntegerField(choices=PAGESECTION.choices(), default=PAGESECTION.DEFAULT)
    priority        = models.PositiveSmallIntegerField(default=0)
    name            = models.CharField(max_length=355, blank=False, null=False)
    is_home         = models.BooleanField(default=False)
    is_service      = models.BooleanField(default=False)
    is_client       = models.BooleanField(default=False)
    is_testimoinals = models.BooleanField(default=False)    
    is_active       = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'pages'
        verbose_name = 'Pages'
        verbose_name_plural = 'Pages'
    
    def __str__(self):
        return str(self.name)
    
class ImageDirectory(AuditFields):
    name        = models.CharField(max_length=355, blank=False, null=False)
    image       = models.ImageField(blank=True, null=True)
    is_client   = models.BooleanField(default=True)
    is_gallery  = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'image_directory'
        verbose_name = 'Image Directory'
        verbose_name_plural = 'Image Directory'
    
    def __str__(self):
        return str(self.name)

class SectionDefault(AuditFields):
    page            = models.ForeignKey(Pages, on_delete=models.DO_NOTHING, blank=True, null=True)
    image_directory = models.ForeignKey(ImageDirectory, on_delete=models.DO_NOTHING, blank=True, null=True)
    image_position  = models.PositiveSmallIntegerField(choices=POSITION.choices(), default=POSITION.NONE)
    title           = models.CharField(max_length=355, blank=False, null=False)
    sub_title       = models.CharField(max_length=355, blank=False, null=False)
    content         = models.TextField(blank=False, null=False)
    image           = models.ImageField(blank=True, null=True)
    is_html         = models.BooleanField(default=True)
    is_active       = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'section_default'
        verbose_name = 'Section Default'
        verbose_name_plural = 'Section Default'
    
    def __str__(self):
        return str(self.title)
    
class Blog(AuditFields):
    navigation      = models.ForeignKey(Navigation, on_delete=models.DO_NOTHING, blank=True, null=True)
    image_directory = models.ForeignKey(ImageDirectory, on_delete=models.DO_NOTHING, blank=True, null=True)
    image_position  = models.PositiveSmallIntegerField(choices=POSITION.choices(), default=POSITION.NONE)
    title           = models.CharField(max_length=355, blank=False, null=False)
    sub_title       = models.CharField(max_length=355, blank=False, null=False)
    content         = models.TextField(blank=False, null=False)
    image           = models.ImageField(blank=True, null=True)
    is_html         = models.BooleanField(default=True)
    is_home         = models.BooleanField(default=False)
    is_active       = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'blog'
        verbose_name = 'Blog'
        verbose_name_plural = 'Blog'
    
    def __str__(self):
        return str(self.title)

class Testimoinals(AuditFields):
    image_directory = models.ForeignKey(ImageDirectory, on_delete=models.DO_NOTHING, blank=True, null=True)
    name        = models.CharField(max_length=355, blank=False, null=False)
    content     = models.TextField(blank=False, null=False)
    image       = models.ImageField(blank=True, null=True)
    is_home     = models.BooleanField(default=False)
    is_active   = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'testimoinals'
        verbose_name = 'Testimoinals'
        verbose_name_plural = 'Testimoinals'
    
    def __str__(self):
        return str(self.title)

class Features(AuditFields):
    name        = models.CharField(max_length=355, blank=False, null=False)
    
    class Meta:
        db_table = 'features'
        verbose_name = 'Features'
        verbose_name_plural = 'Features'
    
    def __str__(self):
        return str(self.name)

class Packages(AuditFields):
    features    = models.ManyToManyField(Features)
    name        = models.CharField(max_length=355, blank=False, null=False)
    discount    = models.CharField(max_length=355, blank=True, null=True)
    priorty     = models.IntegerField(default=0, blank=False, null=False)
    price        = models.DecimalField(default=0, max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        db_table = 'packages'
        verbose_name = 'Packages'
        verbose_name_plural = 'Packages'
    
    def __str__(self):
        return str(self.name)

    def get_features_ids_set(self):
        return self.features.filter(is_valid=True).values_list('id', flat=True)

class Services(AuditFields):
    navigation      = models.ForeignKey(Navigation, on_delete=models.DO_NOTHING, blank=True, null=True)
    image_directory = models.ForeignKey(ImageDirectory, on_delete=models.DO_NOTHING, blank=True, null=True)
    title           = models.CharField(max_length=355, blank=False, null=False)
    content         = models.TextField(blank=False, null=False)
    image           = models.ImageField(blank=True, null=True)
    is_home         = models.BooleanField(default=True)
    packages        = models.ManyToManyField(Packages)
    
    class Meta:
        db_table = 'services'
        verbose_name = 'Services'
        verbose_name_plural = 'Services'
    
    def __str__(self):
        return str(self.title)
    
class Config(AuditFields):
    banner_title        = models.CharField(max_length=355, blank=False, null=False)
    banner_sub_title    = models.CharField(max_length=355, blank=False, null=False)
    banner_content      = models.TextField(blank=False, null=False)
    banner_image_one    = models.ImageField(blank=True, null=True)
    banner_image_two    = models.ImageField(blank=True, null=True)
    use_layout_two      = models.BooleanField(default=False)
    
    fb_link         = models.CharField(max_length=355, blank=False, null=False)
    x_link          = models.CharField(max_length=355, blank=False, null=False)
    linkedin_link   = models.CharField(max_length=355, blank=False, null=False)
    youtube_link    = models.CharField(max_length=355, blank=False, null=False)
    instagram_link  = models.CharField(max_length=355, blank=False, null=False)
    whatsapp_link   = models.CharField(max_length=355, blank=False, null=False)

    whatsapp_number   = models.CharField(max_length=25, blank=True, null=True)

    white_logo   = models.ImageField(blank=True, null=True)
    color_logo   = models.ImageField(blank=True, null=True)

    name        = models.TextField(blank=False, null=False)
    about_us    = models.TextField(blank=False, null=False)
    email       = models.TextField(blank=False, null=False)
    mobile      = models.TextField(blank=False, null=False)
    address     = models.TextField(blank=False, null=False)
    opening_hours     = models.TextField(blank=False, null=False)

    footer_script     = models.TextField(blank=True, null=True)
    
    email_to        = models.CharField(max_length=355, blank=True, null=True)
    email_cc        = models.CharField(max_length=355, blank=True, null=True)
    smtp_name        = models.CharField(max_length=50)
    smtp_host        = models.CharField(max_length=20)
    smtp_port        = models.CharField(max_length=20)
    smtp_username    = models.CharField(max_length=200)
    smtp_password    = models.CharField(max_length=200)

    class Meta:
        db_table = 'config'
        verbose_name = 'Config'
        verbose_name_plural = 'Config'
    
    def __str__(self):
        return str(self.id)
    
    
class Booking(AuditFields):
    user        = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True)
    name        = models.CharField(max_length=100, blank=False, null=False)
    email       = models.CharField(max_length=50, blank=True, null=True)
    mobile      = models.CharField(max_length=50, blank=False, null=False)
    service     = models.CharField(max_length=250, blank=False, null=False)
    pet_type    = models.CharField(max_length=50, blank=False, null=False)
    breed       = models.CharField(max_length=50, blank=False, null=False)
    pet_age     = models.CharField(max_length=50, blank=False, null=False)
    aggressive  = models.CharField(max_length=50, blank=False, null=False)
    vaccinations    = models.CharField(max_length=50, blank=False, null=False)
    date    = models.DateField(blank=False, null=False)
    time    = models.CharField(max_length=50, blank=False, null=False)
    address     = models.TextField(blank=False, null=False)
    location_link    = models.TextField(blank=False, null=False)
    
    class Meta:
        db_table = 'booking'
        verbose_name = 'Booking'
        verbose_name_plural = 'Bookings'
    
    def __str__(self):
        return str(self.name)

        
class Career(AuditFields):
    name        = models.CharField(max_length=100, blank=False, null=False)
    mobile      = models.CharField(max_length=50, blank=False, null=False)
    job_role    = models.CharField(max_length=250, blank=False, null=False)
    job_type    = models.CharField(max_length=50, blank=False, null=False)
    experience  = models.CharField(max_length=50, blank=False, null=False)
    company     = models.CharField(max_length=50, blank=False, null=False)
    
    class Meta:
        db_table = 'career'
        verbose_name = 'Career'
        verbose_name_plural = 'Career'
    
    def __str__(self):
        return str(self.name)