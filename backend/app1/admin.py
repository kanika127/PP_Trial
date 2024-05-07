from django.contrib import admin
from django.db.models import Q

from .models import *
# Register your models here.

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email')
    list_filter = ('is_staff', 'is_superuser', 'is_active')

class ProjectAdmin(admin.ModelAdmin):
    search_fields = ('title', 'owner__username') # ('field1', 'field2')  # Add the fields you want to enable search for
    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)

        # Split the search term into individual terms
        terms = search_term.split(' ')

        # If search bar must rceive project-title AND owner-username
        # Create a Q object to filter on each term for field1 and field2__username
        # for term in terms:
            # queryset = queryset.filter(Q(title__icontains=term) | Q(owner__username__icontains=term))

        # return queryset, use_distinct

        # If search bar must rceive EITHER project-title OR owner-username OR BOTH
        # Create a Q object to filter on each term for title and owner__username
        title_q = Q()
        username_q = Q()
        for term in terms:
            title_q |= Q(title__icontains=term)
            username_q |= Q(owner__username__icontains=term)

        # Combine title and username filters
        if title_q and username_q:
            queryset = queryset.filter(title_q | username_q)
        elif title_q:
            queryset = queryset.filter(title_q)
        elif username_q:
            queryset = queryset.filter(username_q)

        return queryset, use_distinct

admin.site.register(BaseUser)
admin.site.register(PassionUser)
admin.site.register(SuperUser)
admin.site.register(Client)
admin.site.register(Creator)
admin.site.register(UserSampleWorkTable)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Role)
admin.site.register(Application)
admin.site.register(ProjectSampleWorkTable)
admin.site.register(User, CustomUserAdmin)

