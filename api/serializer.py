from api.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Goal, KRA, KPI, Plan, userRoles, Deadline, Year, KPIValue, Notification, Budget, QuarterlyReport

# class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
#     def validate(self, attrs):
#         # Get the token data from parent class
#         data = super().validate(attrs)

#         # Add custom claims
#         data['username'] = self.user.username
#         data['role'] = self.user.role.roles if self.user.role else None

#         # Add claims to the token
#         token = self.get_token(self.user)
#         token['username'] = self.user.username
#         token['role'] = self.user.role.roles if self.user.role else None

#         # Update the token data
#         data['access'] = str(token.access_token)
#         data['refresh'] = str(token)

#         return data
    

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        # Get the token data from parent class
        data = super().validate(attrs)

        # Add claims to the token
        token = self.get_token(self.user)
        token['username'] = self.user.username
        token['role'] = self.user.role.roles if self.user.role else None
        token['parent'] = str(self.user.parent.id) if self.user.parent else None  

        # Update the token data
        data['access'] = str(token.access_token)
        data['refresh'] = str(token)

        return data




# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('id', 'username', 'email', 'role', 'password')
#         extra_kwargs = {'password': {'write_only': True}}

#     def create(self, validated_data):
#         user = User.objects.create_user(
#             username=validated_data['username'],
#             email=validated_data['email'],
#             password=validated_data['password']
#         )
#         if 'role' in validated_data:
#             user.role = validated_data['role']
#             user.save()
#         return user

#     def update(self, instance, validated_data):
#         # Extract password from the validated data
#         password = validated_data.pop('password', None)

#         # Update other fields
#         for attr, value in validated_data.items():
#             setattr(instance, attr, value)

#         # If password is provided, set it (this will hash it)
#         if password:
#             instance.set_password(password)
        
#         # Save the updated instance
#         instance.save()
        
#         return instance
    

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__' 

    def create(self, validated_data):
        # Extract password from the validated data
        password = validated_data.pop('password', None)

        # Create the user instance without the password
        user = User(**validated_data)

        # If password is provided, set it (this will hash it)
        if password:
            user.set_password(password)
        user.save()
        
        return user

    def update(self, instance, validated_data):
        # Extract password from the validated data
        password = validated_data.pop('password', None)

        # Update other fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        # If password is provided, set it (this will hash it)
        if password:
            instance.set_password(password)
        
        # Save the updated instance
        instance.save()
        
        return instance

class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = '__all__'

class QuarterlyReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = '__all__'

class BudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget
        fields = '__all__'

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'

class QuarterlyReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuarterlyReport
        fields = '__all__'  # Includes all model fields


class DeadlineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deadline
        fields = '__all__'


    
# Serializers for Goal, KRA, and KPI
class KPISerializer(serializers.ModelSerializer):
    class Meta:
        model = KPI
        fields = '__all__'


class KRASerializer(serializers.ModelSerializer):
    kpis = KPISerializer(many=True, read_only=True)  # Nested KPIs

    class Meta:
        model = KRA
        fields = '__all__'


class GoalSerializer(serializers.ModelSerializer):
    kras = KRASerializer(many=True, read_only=True)  # Nested KRAs

    class Meta:
        model = Goal
        fields = '__all__'


class KPISerializer(serializers.ModelSerializer):
    class Meta:
        model = KPI
        fields = ('id', 'name')

class KRASerializer(serializers.ModelSerializer):
    kpis = KPISerializer(many=True, read_only=True)

    class Meta:
        model = KRA
        fields = ('id', 'name', 'kpis')

class GoalSerializer(serializers.ModelSerializer):
    kras = KRASerializer(many=True, read_only=True)

    class Meta:
        model = Goal
        fields = ('id', 'name', 'kras') 


class YearSerializer(serializers.ModelSerializer):
    # goals = GoalSerializer(many=True)  

    class Meta:
        model = Year
        fields = ['id', 'year']


class KPIValueSerializer(serializers.ModelSerializer):
    kpi = serializers.PrimaryKeyRelatedField(queryset=KPI.objects.all())
    # year = YearSerializer(many=True, read_only=True)
    # year = serializers.PrimaryKeyRelatedField(queryset=Year.objects.all())

    class Meta:
        model = KPIValue
        # fields = ('id', 'kpi', 'value', 'year')
        fields = '__all__'



class userRolesSerializer(serializers.ModelSerializer):
    role_display = serializers.CharField(source='get_roles_display', read_only=True)

    class Meta:
        model = userRoles
        fields = '__all__'



class GoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = '__all__'

class KRASerializer(serializers.ModelSerializer):
    class Meta:
        model = KRA
        fields = '__all__'

class KPISerializer(serializers.ModelSerializer):
    class Meta:
        model = KPI
        fields = '__all__'