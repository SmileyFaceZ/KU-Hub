from django.urls import path
from kuhub import views
from django.views.generic import RedirectView


app_name = "kuhub"
urlpatterns = [
    path('', RedirectView.as_view(url="review-hub/")),
    path('review-hub/', views.ReviewHubView.as_view(), name='review'),
    path('summary-hub/', views.SummaryHubView.as_view(), name='summary'),
    path('tricks-hub/', views.TricksHubView.as_view(), name='tricks'),
    path('encouragement/',
         views.EncouragementView.as_view(),
         name='encouragement'
    ),
]
