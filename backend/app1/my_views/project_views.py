from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView, ListAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework import serializers
from rest_framework import status
from rest_framework.response import Response

from django.db.models import Q
from django.http import JsonResponse

from app1.models import Project, ROLE_CHOICES
from app1.serializers import *

class ProjectPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 10

class ProjectListCreateAPIView(ListCreateAPIView):
    queryset = Project.objects.all().prefetch_related('roles') # prefetch_related('roles'):optimizes retrieval of Project instances along with their related Role instances
    pagination_class = ProjectPagination

    def get_serializer_class(self):
        if self.request.method == 'GET':
            ser_class =  ProjectListSerializer
        else :
            ser_class = ProjectSerializer
        return ser_class

    def get_queryset(self):
        order_by_param = self.request.query_params.get('order_by')
        if not order_by_param or order_by_param not in [field.name for field in Project._meta.fields] :
            order_by_param = 'approx_completion_date'
        order_by_param = '-' + order_by_param # to reverse order

        queryset = self.queryset.order_by(order_by_param)
        return queryset

class ProjectRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all().prefetch_related('roles')
    serializer_class = ProjectSerializer

    # get admin-user
    admin_user = BaseUser.objects.filter(is_superuser=True).first()
    admin_username = None
    if admin_user :
        admin_username = admin_user.username
    print("Admin username:", admin_username)

    def delete(self, request, *args, **kwargs):
        # Retrieve the object by specific value of 'username' and 'title'
        queryset = self.queryset # get_queryset()

        print(f'{request.query_params=}')
        project_id = request.query_params['project_id']
        username = request.query_params['username']

        project = queryset.filter(pk=project_id).first()  
        if project :
            if username == self.admin_username :
                print(f'admin will delete ---> {project}')
                # project.delete()
                print(Project.Status.DELETED)
                project.status = Project.Status.DELETED
                project.save()
                # put project-delete job in job-Q
            elif username == project.owner.username :
                print(f'{username} will delete ---> {project}')
                # project.delete()
                print(Project.Status.DELETED)
                project.status = Project.Status.DELETED
                print(project.status)
                project.save()
                # put project-delete job in job-Q
            else :
                print('delete error')
                return Response({"detail": "permission denied to delete"}, status=status.HTTP_404_NOT_FOUND)
        else :
            return Response({"detail": "Object not found."}, status=status.HTTP_404_NOT_FOUND)

        return Response(status=status.HTTP_204_NO_CONTENT)

    def update(self, request, *args, **kwargs):
        # Retrieve the object by specific value of fld1
        queryset = self.get_queryset()
        instance = queryset.filter(fld1=request.data['fld1']).first()
        if instance:
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data)
        else:
            return Response({"detail": "Object not found."}, status=status.HTTP_404_NOT_FOUND)

    def retrieve(self, request, *args, **kwargs):
        # Retrieve the object by specific value of fld4
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class ProjectListByOwnerAPIView(ListAPIView):
    serializer_class = ProjectListSerializer
    pagination_class = ProjectPagination

    def get_queryset(self):
        username = self.kwargs['username']  # Assuming the URL pattern includes 'owner_id'
        order_by_param = self.request.query_params.get('order_by')
        if not order_by_param or order_by_param not in [field.name for field in Project._meta.fields] :
            order_by_param = 'approx_completion_date'
        order_by_param = '-' + order_by_param # to reverse order

        if not PassionUser.objects.filter(username=username).exists():
            print('NO SUCH USER')
            #raise NotFound("No such user")

        queryset = Project.objects.filter(owner__username=username).prefetch_related('roles').order_by(order_by_param)
        return queryset

# project details by owner
class ProjectOwnerView(RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all().prefetch_related('roles')
    serializer_class = ProjectDetailOwnerSerializer
    lookup_field = 'id' # by default looks up for 'pk'

# project details by applicant
class ProjectApplicantView(RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all().prefetch_related('roles')
    serializer_class = ProjectDetailApplicantSerializer
    lookup_field = 'id' # by default looks up for 'pk'

class ProjectSearchListView(ListAPIView):
    serializer_class = ProjectListSerializer
    pagination_class = ProjectPagination

    def get_queryset(self):
        # Split the search term into individual terms
        search_term = self.request.query_params.get('terms', '')
        terms = search_term.split(' ')

        order_by_param = self.request.query_params.get('order_by')
        if not order_by_param or order_by_param not in [field.name for field in Project._meta.fields] :
            order_by_param = 'approx_completion_date'
        order_by_param = '-' + order_by_param # to reverse order

        queryset = Project.objects.all()

        # Create a Q object to filter on each term for title, owner__username, medium and role
        title_q = Q()
        username_q = Q()
        medium_q = Q()
        role_q = Q()
        for term in terms:
            title_q |= Q(title__icontains=term)
            username_q |= Q(owner__username__icontains=term)
            medium_q |= Q(medium__icontains=term)
            for ch1, ch2 in ROLE_CHOICES :
                if ch2.upper() == term.upper() : # introduce tokenizer here
                    print(ch1, ch2)
                    role_q |= Q(roles__role_type__iexact=ch1)
                    break
            
        print(f'{title_q=}')

        # Combine all filters 
        from itertools import combinations
        from functools import reduce
        q_objs = [title_q, username_q, medium_q, role_q]
        combinations_list = []
        for i in range(len(q_objs)+1, 0, -1) :
            combinations_list += list(combinations(q_objs, i))

        for combination in combinations_list :
            if all(combination) :
                combined_q = reduce(lambda x, y: x | y, combination)
                queryset = queryset.filter(combined_q).distinct()
                break

        queryset = queryset.order_by(order_by_param)
        return queryset

        ####
        # Following huge code has been replaced by the above scalable code section
        # This must be removed after the above scalable section has been well tested
        ####
        #queryset = Project.objects.all()
        #ABCD
        #if title_q and username_q and medium_q and role_q :
            #print('ABCD')
            #queryset = queryset.filter(title_q | username_q | medium_q | role_q)
        # ABC, ABD, ACD, BCD, 
        #elif title_q and username_q and medium_q :
            #print('ABC')
            #queryset = queryset.filter(title_q | username_q | medium_q)
        #elif title_q and username_q and role_q :
            #print('ABD')
            #queryset = queryset.filter(title_q | username_q | role_q)
        #elif title_q and medium_q and role_q:
            #print('ACD')
            #queryset = queryset.filter(title_q | medium_q | role_q)
        #elif username_q and medium_q and role_q :
            #print('BCD')
            #queryset = queryset.filter(username_q | medium_q | role_q)
        # AB, AC, AD, BC, BD, CD
        #elif title_q and username_q :
            #print('AB')
            #queryset = queryset.filter(title_q | username_q)
        #elif title_q and medium_q :
            #print('AC')
            #queryset = queryset.filter(title_q | medium_q)
        #elif title_q and role_q :
            #print('AD')
            #queryset = queryset.filter(title_q | role_q)
        #elif username_q and medium_q :
            #print('BC')
            #queryset = queryset.filter(username_q | medium_q)
        #elif username_q and role_q :
            #print('BD')
            #queryset = queryset.filter(username_q | role_q)
        #elif medium_q and role_q :
            #print('CD')
            #queryset = queryset.filter(medium_q | role_q)
        # A, B, C, D
        #elif title_q:
            #print('A')
            #queryset = queryset.filter(title_q)
        #elif username_q:
            #print('B')
            #queryset = queryset.filter(username_q)
        #elif medium_q:
            #print('C')
            #queryset = queryset.filter(medium_q)
        #elif role_q:
            #print('D')
            #queryset = queryset.filter(role_q)

        #print(queryset.query)
        #print('==========================================')
        #print()
        #return queryset

# Following SEARCH function assumes that there are 4 separate search bars (one for each category
# This assumes that api could be invoked as :-
#       http://127.0.0.1:8000/app1/projects/search/?owner=kanika&role=dj
#       http://127.0.0.1:8000/app1/projects/search/?owner=kanika&title=p
# This is not used presently
# Can be removed later if not required
class ProjectMultiSearchView(ListAPIView):
    serializer_class = ProjectListSerializer
    pagination_class = ProjectPagination

    def get_queryset(self):
        queryset = Project.objects.all()
        print(queryset)
        title = self.request.query_params.get('title', '')
        medium = self.request.query_params.get('medium', '')
        owner_username = self.request.query_params.get('owner', '')
        role = self.request.query_params.get('role', '')

        title_q = Q()
        medium_q = Q()
        username_q = Q()
        role_q = Q()
        if title :
            title_q |= Q(title__icontains=title)
        if medium :
            medium_q |= Q(medium__icontains=medium)
        if owner_username :
            username_q |= Q(owner__username__icontains=owner_username)
        if role :
            role_q |= Q(roles__role_type__iexact=role)

        queryset = queryset.filter(title_q & medium_q & username_q & role_q)
        print(queryset)
        print(queryset.query)

        return queryset

class ProjectCreateFilterView(ListAPIView):
    # Filter based on following attributes
    # Role - multi-select ---> role_type in Role
    # Paid/Unpaid/Collaboration - multi-select ---> collab_type in Role
    # Completion Date  - date range ---> approx_completion_date in Project TODO
    # In Person / Virtual - multi-select ---> exec_mode in Role
    serializer_class = CreateProjectFilterSerializer

    def get(self, request):
        queryset = self.get_queryset()
        serialized_data = CreateProjectFilterSerializer(queryset, many=True)
        print(f'{serialized_data=}')
        print('*********************************')
        print('*********************************')
        print()
        print(f'{serialized_data.data=}')
        print('*********************************')
        print('*********************************')
        print()
        
        # Get the combined result here before sending it to the client
        combined_result = [item for item in serialized_data.data]
        print()
        print(f'{combined_result=}')
        print()
        role_types = []
        collab_types = []
        completion_date = []
        exec_modes = []
        approx_completion_dates = []
        for res in combined_result :
            role_types += res['role_type']
            collab_types += res['collab_type']
            exec_modes += res['exec_mode']
            approx_completion_dates += [res['project'][0]['approx_completion_date']]
        role_types = [x for i, x in enumerate(role_types) if role_types.index(x) == i] # find uniq items
        collab_types = [x for i, x in enumerate(collab_types) if collab_types.index(x) == i] # find uniq items
        exec_modes = [x for i, x in enumerate(exec_modes) if exec_modes.index(x) == i] # find uniq items
        approx_completion_dates = [x for i, x in enumerate(approx_completion_dates) if approx_completion_dates.index(x) == i] # find uniq items

        for inx, r in enumerate(role_types) :
            for role in ROLE_CHOICES :
                if role[0] == r :
                    role_types[inx] = role[1]

        for inx, c in enumerate(collab_types) :
            for collab in Role.CollabTypes.choices :
                if collab[0] == c :
                    collab_types[inx] = collab[1]

        for inx, m in enumerate(exec_modes) :
            print(inx, m)
            for ex_mode in Role.ExecModes.choices :
                if ex_mode[0] == m :
                    exec_modes[inx] = ex_mode[1]
        filters = {'role_types' : role_types, 'collab_types' : collab_types, 'exec_modes' : exec_modes, 'approx_completion_date' : approx_completion_dates}

        return Response({'filters': filters})

    def handle_exception(self, exc):
        if isinstance(exc, ValidationError):
            return Response({'error': str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        # For other exceptions, use default exception handler
        return super().handle_exception(exc)

    def get_queryset(self):
        queryset = Role.objects.all()

        params = self.request.query_params
        role_types = params.getlist('role_types')
        collab_types = params.getlist('collab_types')
        completion_date_min = params.get('completion_date_min')
        completion_date_max = params.get('completion_date_max')
        exec_modes = params.getlist('exec_modes')

        print(f'present filters --> {role_types=}, {collab_types=}, {exec_modes=}, {completion_date_min=}, {completion_date_max=}')

        values = ['role_type', 'collab_type', 'exec_mode', 'project']
        roletype_q = Q()
        collabtype_q = Q()
        exectype_q = Q()
        completiondate_q = Q()

        if role_types :
            types = [rtype for rtype in role_types[0].split(',')]
            #values.remove('role_type')
            for roletype in types :
                value = None
                for role in ROLE_CHOICES :
                    if role[1] == roletype :
                        value = role[0]
                        break
                roletype_q |= Q(role_type__iexact=value)

        if collab_types :
            types = [ctype for ctype in collab_types[0].split(',')]
            #values.remove('collab_type')
            for collabtype in types :
                value = None
                for collab in Role.CollabTypes.choices :
                    if collab[1] == collabtype :
                        value = collab[0]
                        break
                collabtype_q |= Q(collab_type__iexact=value)

        if completion_date_max :
            if not completion_date_min :
                raise ValidationError('"completion_date_min" parameter is required in the query parameters.')
            completiondate_q = Q(project__approx_completion_date__gte=completion_date_min)

        if completion_date_min :
            if not completion_date_max :
                raise ValidationError('"completion_date_max" parameter is required in the query parameters.')
            completiondate_q &= Q(project__approx_completion_date__lte=completion_date_max)

        if exec_modes :
            types = [extype for extype in exec_modes[0].split(',')]
            #values.remove('exec_mode')
            for execmode in types :
                value = None
                for exmode in Role.ExecModes.choices :
                    if exmode[1] == execmode :
                        value = exmode[0]
                        break
                exectype_q |= Q(exec_mode__iexact=value)

        q = roletype_q & collabtype_q & exectype_q & completiondate_q

        print('======================')
        print(f'{q=}')
        print('======================')

        queryset = queryset.filter(q).values(*values)#.distinct()
        print('======================')
        print(queryset.query)
        print('======================')
        print('======================')
        print()
        return queryset


class ProjectFilteredListView(ListAPIView):
    serializer_class = ProjectListSerializer
    pagination_class = ProjectPagination

    def get_queryset(self):
        queryset = Project.objects.all().prefetch_related('roles')

        params = self.request.query_params
        role_types = params.getlist('role_types')
        collab_types = params.getlist('collab_types')
        completion_dates = params.getlist('completion_dates')
        exec_modes = params.getlist('exec_modes')

        order_by_param = self.request.query_params.get('order_by')
        if not order_by_param or order_by_param not in [field.name for field in Project._meta.fields] :
            order_by_param = 'approx_completion_date'
        order_by_param = '-' + order_by_param # to reverse order

        print(f'present filters --> {role_types=}, {collab_types=}, {exec_modes=}, {completion_dates=}')

        #values = ['role_type', 'collab_type', 'exec_mode']
        roletype_q = Q()
        collabtype_q = Q()
        exectype_q = Q()
        completiondate_q = Q()

        if role_types:
            types = [rtype for rtype in role_types[0].split(',')]
            ##values.remove('role_type')
            for roletype in types :
                value = None
                for role in ROLE_CHOICES :
                    if role[1] == roletype :
                        value = role[0]
                        break
                roletype_q |= Q(roles__role_type__iexact=value)

        if collab_types:
            types = [ctype for ctype in collab_types[0].split(',')]
            ##values.remove('collab_type')
            for collabtype in types :
                value = None
                for collab in Role.CollabTypes.choices :
                    if collab[1] == collabtype :
                        value = collab[0]
                        break
                collabtype_q |= Q(roles__collab_type__iexact=value)

        if completion_dates:
            types = [datetype for datetype in completion_dates[0].split(',')]
            for datetype in types :
                completiondate_q |= Q(approx_completion_date__iexact=datetype)

        if exec_modes:
            types = [extype for extype in exec_modes[0].split(',')]
            ##values.remove('exec_mode')
            for execmode in types :
                value = None
                for exmode in Role.ExecModes.choices :
                    if exmode[1] == execmode :
                        value = exmode[0]
                        break
                exectype_q |= Q(role__exec_mode__iexact=value)

        q = roletype_q & collabtype_q & exectype_q & completiondate_q
        print('================================')
        print(f'FINAL {q=}')

        queryset = queryset.filter(q).distinct().order_by(order_by_param)
        print(queryset.query)
        print('================================')
        print('================================')
        print()
        return queryset

