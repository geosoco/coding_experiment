from django.conf.urls import patterns, include, url
from rest_framework import routers
import views

router = routers.DefaultRouter()
router.register(r'turkuser', views.TurkUserViewSet)
router.register(r'tweet', views.TweetViewSet)
router.register(r'codescheme', views.CodeSchemeViewSet, base_name="CodeScheme" )
router.register(r'code', views.CodeViewSet, base_name="Code")
router.register(r'codeinstance', views.CodeInstanceViewSet, base_name="CodeInstance")
router.register(r'assignment', views.AssignmentViewSet, base_name="Assignment")
router.register(r'dataset', views.DatasetViewSet)
#router.register(r'currentuser', views.CurrentTurkUserViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = patterns('',
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
)
