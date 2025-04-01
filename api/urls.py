from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter  # <-- Add this line
from django.urls import include, path
# from .views import GoalViewSet, KRAViewSet, KPIViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView




from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    # path('token/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('users/', views.UserListCreateAPIView.as_view(), name='user-list-create'),
    path('users/<uuid:pk>/', views.UserDetailAPIView.as_view(), name='user-detail'),

    path('roles/', views.userRolesListView.as_view(), name='user-list-create'),
    path('roles/<uuid:pk>/', views.userRolesDetailView.as_view(), name='user-detail'),

    path('deadlines/', views.DeadlineListCreate.as_view(), name='deadline-list-create'),
    path('deadlines/<int:pk>/', views.DeadlineDetail.as_view(), name='deadline-detail'),

    path('notifications/', views.NotificationListAPIView.as_view(), name='notification-list'),
    path('notifications/create/', views.NotificationCreateAPIView.as_view(), name='notification-create'),
    path('notifications/<uuid:pk>/', views.NotificationDetailAPIView.as_view(), name='notification-detail'),
    path('notifications/<uuid:pk>/update/', views.NotificationUpdateAPIView.as_view(), name='notification-update'),
    path('notifications/<uuid:pk>/delete/', views.NotificationDeleteAPIView.as_view(), name='notification-delete'), 
    path('notifications/receiver/<uuid:recipient_id>/', views.NotificationForReceiverAPIView.as_view(), name='notification-for-receiver'),
    
    path('goals/', views.GoalListView.as_view(), name='goal-list'),
    path('goals/<uuid:pk>/', views.GoalDetailView.as_view(), name='goal-detail'),
    path('goals/year/<int:year>/', views.GoalsByYearAPIViewmy.as_view(), name='goals-by-year'),

    path('kras/', views.KRAListView.as_view(), name='kra-list'),
    path('kras/<uuid:pk>/', views.KRADetailView.as_view(), name='kra-detail'),

    path('kpis/', views.KPIListView.as_view(), name='kpi-list'),
    path('kpis/<uuid:pk>/', views.KPIDetailView.as_view(), name='kpi-detail'), 

    path('years/', views.YearListView.as_view(), name='year-list'),
    path('years/<int:pk>/', views.YearDetailView.as_view(), name='year-detail'),

    path('budget/', views.BudgetListAPIView.as_view(), name='notification-list'),
    path('budget/<uuid:pk>/', views.BudgetDetailAPIView.as_view(), name='notification-detail'),

    path('kpivalues/', views.KPIValueListCreateAPIView.as_view(), name='kpivalue-list-create'),
    path('kpi-values/<uuid:kpi_id>/<uuid:year_id>/', views.KPIValueByKPIAndYearAPIView.as_view(), name='kpi-values-by-kpi-year'),

    path('plans/', views.PlanListCreateAPIView.as_view(), name='plan-list-create'),
    path('plans/<int:pk>/', views.PlanRetrieveUpdateDeleteAPIView.as_view(), name='plan-retrieve-update-delete'),


    # Retrieve plan by sender/receiver id
    path('plans/sender/<uuid:sender_id>/', views.PlanRetrieveBySenderAPIView.as_view(), name='plan-list-by-sender'),
    path('plans/receiver/<uuid:receiver_id>/', views.PlanRetrieveByReceiverAPIView.as_view(), name='plan-list-by-receiver'),

    # Report
    path('reports/', views.QuarterlyReportAPIView.as_view(), name='plan-list-create'),
    path('reports/<uuid:pk>/', views.PlanRetrieveUpdateDeleteAPIView.as_view(), name='plan-retrieve-update-delete'),

    # Retrieve report by sender/receiver id
    path('reports/sender/<uuid:sender_id>/', views.ReportRetrieveBySenderAPIView.as_view(), name='plan-list-by-sender'),
    path('reports/receiver/<uuid:receiver_id>/', views.ReportRetrieveByReceiverAPIView.as_view(), name='plan-list-by-receiver'),

    # path('report/<int:kpi_id>/<int:year_id>/<int:quarter>/<int:sender_id>/', views.UpdateQuarterlyReportAPIView.as_view(), name='update-quarterly-report'),
    # path('report/', views.UpdateQuarterlyReportAPIView.as_view(), name='update-quarterly-report'),
    path('plans/update/', views.UpdatePlanSendersReceiversAPIView.as_view(), name='update-plan-senders-receivers'),

    path('plan/<uuid:pk>/', views.PlanUpdateDeleteView.as_view(), name='plan-update-delete'),

        
    path('report/<uuid:pk>/', views.ReportUpdateDeleteView.as_view(), name='plan-update-delete'), 


]
