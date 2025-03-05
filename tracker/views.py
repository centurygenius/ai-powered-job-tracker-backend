from django.shortcuts import render
from .models import JobApplication, User
from rest_framework import generics
from .serializers import JobApplicationSerializer, UserSerializer, UserRegisterSerializer, CustomTokenObtainPairSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import api_view
from rest_framework.response import Response
import random
import requests
from django.conf import settings


# ====================== View for job recommendation =======================
rapidapi_key = settings.RAPIDAPI_KEY  # Access API key

@api_view(['GET'])
def job_recommendations(request):
    query = request.GET.get('query')
    url = "https://jsearch.p.rapidapi.com/search"
    headers = {
        "x-rapidapi-key": rapidapi_key,
        "x-rapidapi-host": "jsearch.p.rapidapi.com"
    }
    queryString = {"query": query, "page": "1", "num_pages": "1", "country": "US", "date_posted": "all"}

    response = requests.get(url, headers=headers, params=queryString)
    return Response({"recommendations": response.json()})


# ====================== View for resume feedback =======================
IMPROVEMENTS = [
    "Add measurable achievements in work experience.",
    "Use more action verbs to describe accomplishments.",
    "Ensure consistent formatting and fonts.",
    "Include a professional summary at the top.",
    "Optimize resume with keywords from job descriptions."
]

@api_view(['POST'])
def resume_feedback(request):
    resumeText = request.data.get('resumeText')
    if not resumeText:
        return Response({"feedback": "Resume text is required."}, status=400)
    feedback = random.sample(IMPROVEMENTS, k=3)
    return Response({"feedback": feedback})


# ====================== View for token =======================
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer



# ====================== View for user registeration =======================
class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]



# ====================== View for job applications =======================
class JobApplicationView(generics.ListCreateAPIView):
    queryset = JobApplication.objects.all()
    serializer_class = JobApplicationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save(user=self.request.user)
        else:
            print(serializer.errors)

class JobApplicationDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = JobApplication.objects.all()
    serializer_class = JobApplicationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return self.queryset.filter(user=user)
