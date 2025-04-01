from django.shortcuts import render
from django.http import JsonResponse
from api.models import User
from django.shortcuts import get_object_or_404

from api.serializer import KPISerializer, PlanSerializer, UserSerializer, userRolesSerializer, DeadlineSerializer
from api.serializer import KPISerializer, PlanSerializer, UserSerializer, userRolesSerializer, DeadlineSerializer
from api.serializer import YearSerializer, GoalSerializer, KRASerializer, KPIValueSerializer
from api.serializer import CustomTokenObtainPairSerializer, NotificationSerializer, BudgetSerializer, QuarterlyReportSerializer


from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from .models import Goal, KRA, KPI, Plan, userRoles, Deadline, Year, KPIValue, Notification, Budget, QuarterlyReport
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound

from rest_framework import status, permissions
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from django.http import Http404





class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def testEndPoint(request):
    if request.method == 'GET':
        data = f"Congratulation {request.user}, your API just responded to GET request"
        return Response({'response': data}, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        text = "Hello buddy"
        data = f'Congratulation your API just responded to POST request with text: {text}'
        return Response({'response': data}, status=status.HTTP_200_OK)
    return Response({}, status.HTTP_400_BAD_REQUEST)




class UserListCreateAPIView(APIView):
    # permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        # Get all users
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        # Create a new user
        serializer = UserSerializer(data=request.data)
    def post(self, request):
        # data = request.data.copy()
        # data['parent'] = request.user.parent.id
        newUser = request.data
        serializer = UserSerializer(data=newUser)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class UserDetailAPIView(APIView):
    def get(self, request, pk, *args, **kwargs):
        # Get user by primary key (id)
        user = get_object_or_404(User, pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk, *args, **kwargs):
        # Update the user details
        user = get_object_or_404(User, pk=pk)
        serializer = UserSerializer(user, data=request.data, partial=False)  # Use partial=False for full update
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, *args, **kwargs):
        # Update the user with partial data (for example, just changing the username)
        user = get_object_or_404(User, pk=pk)
        serializer = UserSerializer(user, data=request.data, partial=True)  # Use partial=True for partial update
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        # Delete the user
        user = get_object_or_404(User, pk=pk)
        user.delete()
        return Response({"message": "User deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
    



class NotificationCreateView(generics.CreateAPIView):
    serializer_class = NotificationSerializer

    def post(self, request, *args, **kwargs):
        recipient_ids = request.data.get('recipients', [])  # Assuming recipients are sent as a list of user IDs
        message = request.data.get('message', '')
        attachment = request.data.get('attachment', None)

        # Create a notification for each recipient
        for recipient_id in recipient_ids:
            recipient = get_user_model().objects.get(id=recipient_id)
            notification = Notification.objects.create(recipient=recipient, message=message, attachment=attachment)
            notification.save()

        return Response(status=status.HTTP_201_CREATED)



class NotificationAddRecipientView(generics.UpdateAPIView):
    serializer_class = NotificationSerializer
    queryset = Notification.objects.all()

    def patch(self, request, *args, **kwargs):
        notification_id = kwargs.get('pk')
        recipient_ids = request.data.get('recipients', [])  # Assuming recipients are sent as a list of user IDs

        try:
            notification = self.get_object()

            # Add recipients to the notification
            for recipient_id in recipient_ids:
                recipient = get_user_model().objects.get(id=recipient_id)
                notification.recipients.add(recipient)

            return Response(status=status.HTTP_200_OK)

        except Notification.DoesNotExist:
            return Response({'error': 'Notification not found.'}, status=status.HTTP_404_NOT_FOUND)

# class NotificationListAPIView(APIView):
#     # permission_classes = [IsAuthenticated]
#     def get(self, request):
#         goals = Notification.objects.all()
#         serializer = NotificationSerializer(goals, many=True)
#         return Response(serializer.data)

#     def post(self, request):
#         serializer = NotificationSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class NotificationDetailAPIView(APIView):
#     def get(self, request, pk):
#         try:
#             goal = Notification.objects.get(pk=pk)
#         except Notification.DoesNotExist:
#             return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

#         serializer = NotificationSerializer(goal)
#         return Response(serializer.data)

#     def put(self, request, pk):
#         try:
#             goal = Notification.objects.get(pk=pk)
#         except Notification.DoesNotExist:
#             return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

#         serializer = NotificationSerializer(goal, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, pk):
#         try:
#             goal = Goal.objects.get(pk=pk)
#         except Goal.DoesNotExist:
#             return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

#         goal.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
    















class GoalListView(APIView):
    # permission_classes = [IsAuthenticated]
    def get(self, request):
        goals = Goal.objects.all()
        serializer = GoalSerializer(goals, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = GoalSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class GoalsByYearAPIViewmy(APIView):
    def get(self, request, year):
        try:
            # Get the year object based on the provided year
            year_instance = Year.objects.get(year=year)
            # Serialize the year with related goals
            serializer = YearSerializer(year_instance)
            return Response(serializer.data)
        except Year.DoesNotExist:
            return Response({'error': 'Year not found'}, status=status.HTTP_404_NOT_FOUND)


class GoalDetailView(APIView):
    def get(self, request, pk):
        try:
            goal = Goal.objects.get(pk=pk)
        except Goal.DoesNotExist:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = GoalSerializer(goal)
        return Response(serializer.data)

    def put(self, request, pk):
        try:
            goal = Goal.objects.get(pk=pk)
        except Goal.DoesNotExist:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = GoalSerializer(goal, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            goal = Goal.objects.get(pk=pk)
        except Goal.DoesNotExist:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

        goal.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class KRAListView(APIView):
    def get(self, request):
        kras = KRA.objects.all()
        serializer = KRASerializer(kras, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = KRASerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class KRADetailView(APIView):
    def get(self, request, pk):
        try:
            kra = KRA.objects.get(pk=pk)
        except KRA.DoesNotExist:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = KRASerializer(kra)
        return Response(serializer.data)

    def put(self, request, pk):
        try:
            kra = KRA.objects.get(pk=pk)
        except KRA.DoesNotExist:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = KRASerializer(kra, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            kra = KRA.objects.get(pk=pk)
        except KRA.DoesNotExist:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

        kra.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class KPIListView(APIView):
    # permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        kpis = KPI.objects.all()
        serializer = KPISerializer(kpis, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = KPISerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class KPIDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    # permission_classes = [permissions.IsAuthenticated]
    def get(self, request, pk):
        try:
            kpi = KPI.objects.get(pk=pk)
        except KPI.DoesNotExist:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = KPISerializer(kpi)
        return Response(serializer.data)

    def put(self, request, pk):
        try:
            kpi = KPI.objects.get(pk=pk)
        except KPI.DoesNotExist:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = KPISerializer(kpi, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            kpi = KPI.objects.get(pk=pk)
        except KPI.DoesNotExist:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

        kpi.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class YearListView(APIView):
    def get(self, request):
        years = Year.objects.all()
        serializer = YearSerializer(years, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = YearSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class YearDetailView(APIView):
    def get(self, request, pk):
        try:
            year = Year.objects.get(pk=pk)
        except Year.DoesNotExist:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = YearSerializer(year)
        return Response(serializer.data)

    def put(self, request, pk):
        try:
            year = Year.objects.get(pk=pk)
        except Year.DoesNotExist:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = YearSerializer(year, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            year = Year.objects.get(pk=pk)
        except Year.DoesNotExist:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

        year.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class KPIValueListView(APIView):
    def get(self, request):
        kpi_values = KPIValue.objects.all()
        serializer = KPIValueSerializer(kpi_values, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = KPIValueSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class KPIValueDetailView(APIView):
    def get(self, request, pk):
        try:
            kpi_value = KPIValue.objects.get(pk=pk)
        except KPIValue.DoesNotExist:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = KPIValueSerializer(kpi_value)
        return Response(serializer.data)

    def put(self, request, pk):
        try:
            kpi_value = KPIValue.objects.get(pk=pk)
        except KPIValue.DoesNotExist:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = KPIValueSerializer(kpi_value, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            kpi_value = KPIValue.objects.get(pk=pk)
        except KPIValue.DoesNotExist:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

        kpi_value.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


    

class userRolesListView(APIView):
    def get(self, request):
        items = userRoles.objects.all()
        serializer = userRolesSerializer(items, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = userRolesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Handle detail operations
class userRolesDetailView(APIView):
    def get(self, request, pk):
        role = get_object_or_404(userRoles, pk=pk)
        serializer = userRolesSerializer(role)
        return Response(serializer.data)

    def put(self, request, pk):
        role = get_object_or_404(userRoles, pk=pk)
        serializer = userRolesSerializer(role, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        role = get_object_or_404(userRoles, pk=pk)
        role.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class DeadlineListCreate(APIView):
    def get(self, request):
        deadlines = Deadline.objects.all()
        serializer = DeadlineSerializer(deadlines, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = DeadlineSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeadlineDetail(APIView):
    # Retrieve, update or delete a deadline instance.
    def get_object(self, pk):
        try:
            return Deadline.objects.get(pk=pk)
        except Deadline.DoesNotExist:
            raise NotFound("Deadline not found")

    def get(self, request, pk):
        deadline = self.get_object(pk)
        serializer = DeadlineSerializer(deadline)
        return Response(serializer.data)

    def put(self, request, pk):
        deadline = self.get_object(pk)
        serializer = DeadlineSerializer(deadline, data=request.data, partial=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        deadline = self.get_object(pk)
        serializer = DeadlineSerializer(deadline, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        deadline = self.get_object(pk)
        deadline.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)










class PlanListCreateAPIView(APIView):
    # permission_classes = [IsAuthenticated]
    def get(self, request):
        plans = Plan.objects.all()
        serializer = PlanSerializer(plans, many=True)
        return Response(serializer.data)

    # def post(self, request):
    #     try:
    #         user_id = request.user.id
    #         user = User.objects.get(id=user_id)
    #         print(user_id)
    #     except User.DoesNotExist:
    #         return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    #     if not user.parent:
    #         return Response({'error': 'User has no parent'}, status=status.HTTP_400_BAD_REQUEST)

    #     data = request.data.copy()
    #     data['receivers'] = [request.user.parent.id]
    #     data['sender'] = [request.user.id]  

    #     serializer = PlanSerializer(data=data, context={'request': request})

    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
        
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def post(self, request):
        data = request.data.copy()
        # print(request.user.parent.id)
        # print(request.user.id)

        # Ensure parent exists before accessing id
        if request.user.parent:
            data['receivers'] = [request.user.parent.id]  
        else:
            data['receivers'] = []  

        data['sender'] = [request.user.id]
        serializer = PlanSerializer(data=data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request):
        try:
            year = request.data.get('year')
            sender_ids = request.data.get('sender', [])  # Expecting a list
            kpi_id = request.data.get('kpi')

            # Validate that sender_ids is a list
            if not isinstance(sender_ids, list):
                return Response({'error': 'Sender must be a list of UUIDs.'}, status=status.HTTP_400_BAD_REQUEST)

            # Fetch the QuarterlyReport using filters
            report = Plan.objects.filter(year__id=year, kpi__id=kpi_id).filter(sender__id__in=sender_ids).distinct().first()

            if not report:
                return Response({'error': 'Plan not found.'}, status=status.HTTP_404_NOT_FOUND)

            # Deserialize and update
            serializer = PlanSerializer(report, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except ValueError:
            return Response({'error': 'Invalid UUID format.'}, status=status.HTTP_400_BAD_REQUEST)
        

    def delete(self, request):
        try:
            year = request.data.get('year')
            sender_ids = request.data.get('sender', [])  # This is a list
            kpi_id = request.data.get('kpi')

            # Ensure sender_ids is a list of valid UUIDs
            if not isinstance(sender_ids, list) or not all(isinstance(s, str) for s in sender_ids):
                return Response({'error': 'Invalid sender format.'}, status=status.HTTP_400_BAD_REQUEST)

            # Find the plan where the sender exists in the ManyToMany field
            plan = Plan.objects.filter(year__id=year, kpi__id=kpi_id, sender__id__in=sender_ids).first()

            if not plan:
                return Response({'error': 'Quarterly report not found.'}, status=status.HTTP_404_NOT_FOUND)

            plan.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        except ValueError:
            return Response({'error': 'Invalid data format.'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)








# class UpdatePlanSendersReceiversAPIView(APIView):
#     def patch(self, request):
#         # Extract kpi and year from the request
#         kpi_id = request.data.get('kpi')
#         year_id = request.data.get('year')

#         # Ensure kpi and year are provided in the request
#         if not kpi_id or not year_id:
#             return Response({"detail": "kpi and year are required."}, status=status.HTTP_400_BAD_REQUEST)
        
#         # Fetch the kpi and year objects
#         try:
#             kpi = KPI.objects.get(id=kpi_id)
#             year = Year.objects.get(id=year_id)
#         except KPI.DoesNotExist:
#             return Response({"detail": "KPI not found."}, status=status.HTTP_404_NOT_FOUND)
#         except Year.DoesNotExist:
#             return Response({"detail": "Year not found."}, status=status.HTTP_404_NOT_FOUND)

#         # Try to get the plan object based on kpi and year
#         try:
#             plan = Plan.objects.get(kpi=kpi, year=year)
#         except Plan.DoesNotExist:
#             return Response({"detail": "Plan not found for the specified kpi and year."}, status=status.HTTP_404_NOT_FOUND)
        
#         # Use PlanSerializer to handle the update of the plan fields (excluding senders and receivers)
#         plan_serializer = PlanSerializer(plan, data=request.data, partial=True)
        
#         if plan_serializer.is_valid():
#             # Save the updated plan fields
#             plan_serializer.save()

#             # Handle the senders and receivers
#             senders = request.data.get('senders', [])
#             receivers = request.data.get('receivers', [])
            
#             # Add senders to the plan (ensure that the sender IDs are valid)
#             if senders:
#                 senders_users = get_user_model().objects.filter(id__in=senders)
#                 plan.sender.add(*senders_users)
            
#             # Add receivers to the plan (ensure that the receiver IDs are valid)
#             if receivers:
#                 receivers_users = get_user_model().objects.filter(id__in=receivers)
#                 plan.receivers.add(*receivers_users)
            
#             # Save the plan after adding senders and receivers
#             plan.save()

#             return Response(plan_serializer.data, status=status.HTTP_200_OK)
        
#         return Response(plan_serializer.errors, status=status.HTTP_400_BAD_REQUEST)






class UpdatePlanSendersReceiversAPIView(APIView):
    def patch(self, request):
        # Extract kpi and year from the request
        kpi_id = request.data.get('kpi')
        year_id = request.data.get('year')

        # Ensure kpi and year are provided in the request
        if not kpi_id or not year_id:
            return Response({"detail": "kpi and year are required."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Fetch the kpi and year objects
        try:
            kpi = KPI.objects.get(id=kpi_id)
            year = Year.objects.get(id=year_id)
        except KPI.DoesNotExist:
            return Response({"detail": "KPI not found."}, status=status.HTTP_404_NOT_FOUND)
        except Year.DoesNotExist:
            return Response({"detail": "Year not found."}, status=status.HTTP_404_NOT_FOUND)

        # Try to get the plan object based on kpi and year
        try:
            plan = Plan.objects.get(kpi=kpi, year=year)
        except Plan.DoesNotExist:
            return Response({"detail": "Plan not found for the specified kpi and year."}, status=status.HTTP_404_NOT_FOUND)

        # Copy request data and set sender and receiver
        data = request.data.copy()

        # Ensure parent exists before accessing id
        if request.user.parent:
            data['receivers'] = [request.user.parent.id]
        else:
            data['receivers'] = []  

        data['senders'] = [request.user.id]

        # Use PlanSerializer to handle the update of the plan fields (including senders and receivers)
        plan_serializer = PlanSerializer(plan, data=data, partial=True, context={'request': request})

        if plan_serializer.is_valid():
            # Save the updated plan fields
            plan_serializer.save()

            return Response(plan_serializer.data, status=status.HTTP_200_OK)

        return Response(plan_serializer.errors, status=status.HTTP_400_BAD_REQUEST)







class QuarterlyReportAPIView(APIView):
    # Retrieve a specific QuarterlyReport
    def get(self, request):
        report = QuarterlyReport.objects.all()
        serializer = QuarterlyReportSerializer(report, many=True)
        return Response(serializer.data)

    # Create a new QuarterlyReport
    def post(self, request):
        data = request.data.copy()

        if request.user.parent:
            data['receivers'] = [request.user.parent.id]
        else:
            data['receivers'] = []

        data['sender'] = [request.user.id]
        serializer = QuarterlyReportSerializer(data=data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        
    def put(self, request):
        try:
            quarter = request.data.get('quarter')
            year = request.data.get('year')
            sender_ids = request.data.get('sender', [])  # Expecting a list
            kpi_id = request.data.get('kpi')

            # Validate that sender_ids is a list
            if not isinstance(sender_ids, list):
                return Response({'error': 'Sender must be a list of UUIDs.'}, status=status.HTTP_400_BAD_REQUEST)

            # Fetch the QuarterlyReport using filters
            report = QuarterlyReport.objects.filter(quarter=quarter, year__id=year, kpi__id=kpi_id).filter(sender__id__in=sender_ids).distinct().first()

            if not report:
                return Response({'error': 'Quarterly report not found.'}, status=status.HTTP_404_NOT_FOUND)

            # Deserialize and update
            serializer = QuarterlyReportSerializer(report, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except ValueError:
            return Response({'error': 'Invalid UUID format.'}, status=status.HTTP_400_BAD_REQUEST)


    # Delete a QuarterlyReport based on filters
    # def delete(self, request):
    #     try:
    #         quarter = request.data.get('quarter')
    #         year = request.data.get('year')
    #         sender_id = request.data.get('sender')
    #         kpi_id = request.data.get('kpi')

    #         report = QuarterlyReport.objects.get(quarter=quarter, year__id=year, sender__id=sender_id, kpi__id=kpi_id)
    #         report.delete()

    #         return Response(status=status.HTTP_204_NO_CONTENT)

    #     except QuarterlyReport.DoesNotExist:
    #         return Response({'error': 'Quarterly report not found.'}, status=status.HTTP_404_NOT_FOUND)


    def delete(self, request):
        try:
            year = request.data.get('year')
            sender_ids = request.data.get('sender', [])  # This is a list
            kpi_id = request.data.get('kpi')

            # Ensure sender_ids is a list of valid UUIDs
            if not isinstance(sender_ids, list) or not all(isinstance(s, str) for s in sender_ids):
                return Response({'error': 'Invalid sender format.'}, status=status.HTTP_400_BAD_REQUEST)

            # Find the plan where the sender exists in the ManyToMany field
            report = QuarterlyReport.objects.filter(year__id=year, kpi__id=kpi_id, sender__id__in=sender_ids).first()

            if not report:
                return Response({'error': 'Quarterly report not found.'}, status=status.HTTP_404_NOT_FOUND)

            report.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        except ValueError:
            return Response({'error': 'Invalid data format.'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        



class KPIValueByKPIAndYearAPIView(APIView):
    def get(self, request, kpi_id, year_id):
        """Retrieve KPIValue records by kpi_id and year_id.""" 
        kpi_values = KPIValue.objects.filter(kpi_id=kpi_id, year_id=year_id)

        if not kpi_values.exists():
            return Response({"message": "No KPI values found for the given KPI and Year."}, status=status.HTTP_404_NOT_FOUND)

        serializer = KPIValueSerializer(kpi_values, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, kpi_id, year_id):
        """Update KPIValue for a given kpi_id and year_id (full update)."""
        kpi_value = get_object_or_404(KPIValue, kpi_id=kpi_id, year_id=year_id)
        serializer = KPIValueSerializer(kpi_value, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, kpi_id, year_id):
        """Partially update KPIValue for a given kpi_id and year_id."""
        kpi_value = get_object_or_404(KPIValue, kpi_id=kpi_id, year_id=year_id)
        serializer = KPIValueSerializer(kpi_value, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, kpi_id, year_id):
        """Delete KPIValue for a given kpi_id and year_id."""
        kpi_value = get_object_or_404(KPIValue, kpi_id=kpi_id, year_id=year_id)
        kpi_value.delete()
        return Response({"message": "KPI Value deleted successfully."}, status=status.HTTP_204_NO_CONTENT)




class PlanRetrieveUpdateDeleteAPIView(APIView):
    def get(self, request, kpi_id):
        kpi_values = KPIValue.objects.filter(kpi=kpi_id)
        if not kpi_values.exists():
            raise Http404("No KPI values found for the given KPI ID")
        
        serializer = KPIValueSerializer(kpi_values, many=True)
        return Response(serializer.data, status=200)

    def get(self, request, pk):
        plan = self.get_object(pk)
        serializer = PlanSerializer(plan)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        plan = self.get_object(pk)
        serializer = PlanSerializer(plan, data=request.data, partial=True)  # Allows partial updates
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        plan = self.get_object(pk)
        plan.delete()
        return Response({"message": "Plan deleted successfully"}, status=status.HTTP_204_NO_CONTENT)



    

class BudgetListAPIView(APIView):
    # permission_classes = [IsAuthenticated]
    def get(self, request):
        goals = Budget.objects.all()
        serializer = BudgetSerializer(goals, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = BudgetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BudgetDetailAPIView(APIView):
    def get(self, request, pk):
        try:
            goal = Budget.objects.get(pk=pk)
        except Budget.DoesNotExist:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = BudgetSerializer(goal)
        return Response(serializer.data)

    def put(self, request, pk):
        try:
            goal = Budget.objects.get(pk=pk)
        except Budget.DoesNotExist:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = BudgetSerializer(goal, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            goal = Goal.objects.get(pk=pk)
        except Goal.DoesNotExist:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

        goal.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class NotificationCreateAPIView(APIView):
    def post(self, request, *args, **kwargs):
        # Get the list of recipient ids from the request
        recipient_ids = request.data.get('recipient', [])
        if not recipient_ids:
            return Response({"error": "At least one recipient is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Fetch the User model and check if all recipients exist
        User = get_user_model()
        recipients = User.objects.filter(id__in=recipient_ids)
        
        if recipients.count() != len(recipient_ids):
            return Response({"error": "One or more recipients not found."}, status=status.HTTP_404_NOT_FOUND)

        # Prepare notification data with correct recipient format
        notification_data = request.data.copy()
        notification_data['recipient'] = recipient_ids  # Use the list of IDs
        
        serializer = NotificationSerializer(data=notification_data)
        if serializer.is_valid():
            notification = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NotificationListAPIView(APIView):
    def get(self, request, *args, **kwargs):
        notifications = Notification.objects.all()
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data)


# Retrieve a single notification by ID
class NotificationDetailAPIView(APIView):
    def get(self, request, pk, *args, **kwargs):
        try:
            notification = Notification.objects.get(id=pk)
        except Notification.DoesNotExist:
            return Response({"error": "Notification not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = NotificationSerializer(notification)
        return Response(serializer.data)


# Update an existing notification (mark as read)
class NotificationUpdateAPIView(APIView):
    def patch(self, request, pk, *args, **kwargs):
        try:
            notification = Notification.objects.get(id=pk)
        except Notification.DoesNotExist:
            return Response({"error": "Notification not found."}, status=status.HTTP_404_NOT_FOUND)

        # Mark notification as read
        notification.mark_as_read()

        serializer = NotificationSerializer(notification)
        return Response(serializer.data, status=status.HTTP_200_OK)


# Delete a notification
class NotificationDeleteAPIView(APIView):
    def delete(self, request, pk, *args, **kwargs):
        try:
            notification = Notification.objects.get(id=pk)
        except Notification.DoesNotExist:
            return Response({"error": "Notification not found."}, status=status.HTTP_404_NOT_FOUND)

        notification.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class NotificationForReceiverAPIView(APIView):
    def get(self, request, recipient_id, *args, **kwargs):
        try:
            # Fetch the user (receiver) by their ID
            User = get_user_model()
            recipient = User.objects.get(id=recipient_id)
        except User.DoesNotExist:
            return Response({"error": "Recipient not found."}, status=status.HTTP_404_NOT_FOUND)

        # Get all notifications for the given recipient
        notifications = Notification.objects.filter(recipient=recipient)

        # Serialize and return the notifications
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class KPIValueListCreateAPIView(APIView):
    def get(self, request, *args, **kwargs):
        # List all KPIValues
        kpivalues = KPIValue.objects.all()
        serializer = KPIValueSerializer(kpivalues, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        # Create a new KPIValue
        serializer = KPIValueSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class KPIValueRetrieveUpdateDestroyAPIView(APIView):
    def get_object(self, pk):
        try:
            return KPIValue.objects.get(pk=pk)
        except KPIValue.DoesNotExist:
            return None

    def get(self, request, pk, *args, **kwargs):
        # Retrieve a single KPIValue
        kpivalue = self.get_object(pk)
        if not kpivalue:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = KPIValueSerializer(kpivalue)
        return Response(serializer.data)

    def put(self, request, pk, *args, **kwargs):
        # Update a single KPIValue (replace it entirely)
        kpivalue = self.get_object(pk)
        if not kpivalue:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = KPIValueSerializer(kpivalue, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, *args, **kwargs):
        # Partially update a single KPIValue
        kpivalue = self.get_object(pk)
        if not kpivalue:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = KPIValueSerializer(kpivalue, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        # Delete a single KPIValue
        kpivalue = self.get_object(pk)
        if not kpivalue:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        kpivalue.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class KPIValueAPIView(APIView):

    def get(self, request, year, kpi_name):
        try:
            # Get the Year and KPI objects based on the input
            year_instance = Year.objects.get(year=year)
            kpi_instance = KPI.objects.get(name=kpi_name)

            # Retrieve the related KRA and Goal for the KPI
            kra_instance = kpi_instance.kra
            goal_instance = kra_instance.goal

            # Retrieve the KPIValue for the given Year and KPI
            kpi_value = KPIValue.objects.get(kpi=kpi_instance, kpi__kra=kra_instance, kpi__kra__goal=goal_instance, kpi__kra__goal__year=year_instance)

            # Serialize the KPIValue instance
            serializer = KPIValueSerializer(kpi_value)

            return Response(serializer.data)

        except Year.DoesNotExist:
            raise NotFound(f"Year {year} not found.")
        except KPI.DoesNotExist:
            raise NotFound(f"KPI {kpi_name} not found.")
        except KPIValue.DoesNotExist:
            raise NotFound(f"No KPI value found for KPI '{kpi_name}' in Year {year}.")



class PlanByYearKPIAPIView(APIView):
    def get(self, request, year, kpi_id):
        year_obj = get_object_or_404(Year, year=year)

        # Get the KPI object linked to the given year
        kpi = get_object_or_404(KPI, id=kpi_id, kra__goal__year=year_obj)

        # Retrieve the Plan for this KPI
        plan = get_object_or_404(Plan, kpi=kpi)

        # Serialize the Plan data
        serializer = PlanSerializer(plan)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PlanRetrieveBySenderAPIView(APIView):
    def get(self, request, sender_id):
        plans = Plan.objects.filter(sender__id=sender_id)
        serializer = PlanSerializer(plans, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class PlanRetrieveByReceiverAPIView(APIView):
    def get(self, request, receiver_id):
        plans = Plan.objects.filter(receivers__id=receiver_id)
        serializer = PlanSerializer(plans, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    




# class QuarterlyReportAPIView(APIView):
#     # permission_classes = [IsAuthenticated]
#     def get(self, request):
#         plans = QuarterlyReport.objects.all()
#         serializer = QuarterlyReportSerializer(plans, many=True)
#         return Response(serializer.data)

#     def post(self, request):
#         data = request.data.copy()
#         # print(request.user.parent.id)
#         # print(request.user.id)

#         # Ensure parent exists before accessing id
#         if request.user.parent:
#             data['receivers'] = [request.user.parent.id]  
#         else:
#             data['receivers'] = []  

#         data['sender'] = [request.user.id]
#         serializer = QuarterlyReportSerializer(data=data, context={'request': request})

#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
    











# class UpdateQuarterlyReportAPIView(APIView):
#     def put(self, request, kpi_id, year_id, quarter, sender_id):
#         # Get the sender user instance
#         sender = get_user_model().objects.get(id=sender_id)

#         # Get the report by kpi, year, quarter, and sender
#         report = get_object_or_404(QuarterlyReport, kpi_id=kpi_id, year_id=year_id, quarter=quarter)

#         # Check if the sender is part of the 'sender' field in the report
#         if sender not in report.sender.all():
#             return Response({"detail": "Sender is not authorized to update this report."}, status=status.HTTP_403_FORBIDDEN)

#         # Update the report fields with the data from the request
#         serializer = QuarterlyReportSerializer(report, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)











class PlanUpdateDeleteView(APIView):

    # Update the plan
    def put(self, request, pk):
        try:
            plan = Plan.objects.get(id=pk)
        except Plan.DoesNotExist:
            return Response({"detail": "Plan not found."}, status=status.HTTP_404_NOT_FOUND)
        
        # allowed_fields = ['name', 'description']  
        
        serializer = PlanSerializer(plan, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Delete the plan
    def delete(self, request, pk):
        try:
            plan = Plan.objects.get(id=pk)
        except Plan.DoesNotExist:
            return Response({"detail": "Plan not found."}, status=status.HTTP_404_NOT_FOUND)

        plan.delete()
        return Response({"detail": "Plan deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
    

class ReportUpdateDeleteView(APIView):

    # Update the plan
    def put(self, request, pk):
        try:
            report = QuarterlyReport.objects.get(id=pk)
        except Plan.DoesNotExist:
            return Response({"detail": "Report not found."}, status=status.HTTP_404_NOT_FOUND)
        
        # allowed_fields = ['name', 'description']  
        
        serializer = QuarterlyReportSerializer(report, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Delete the plan
    def delete(self, request, pk):
        try:
            report = QuarterlyReport.objects.get(id=pk)
        except QuarterlyReport.DoesNotExist:
            return Response({"detail": "Report not found."}, status=status.HTTP_404_NOT_FOUND)

        report.delete()
        return Response({"detail": "Report deleted successfully."}, status=status.HTTP_204_NO_CONTENT)


class ReportRetrieveBySenderAPIView(APIView):
    def get(self, request, sender_id):
        reports = QuarterlyReport.objects.filter(sender__id=sender_id)
        serializer = QuarterlyReportSerializer(reports, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ReportRetrieveByReceiverAPIView(APIView):
    def get(self, request, receiver_id):
        reports = QuarterlyReport.objects.filter(receivers__id=receiver_id)
        serializer = QuarterlyReportSerializer(reports, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)