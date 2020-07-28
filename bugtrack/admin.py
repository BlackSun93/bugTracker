from django.contrib import admin
from .models import *

admin.site.register(User)
admin.site.register(Bug)
admin.site.register(Solver)

admin.site.register(Follow)
admin.site.register(Comment)
admin.site.register(Update)
admin.site.register(Votes)


# Register your models here.
