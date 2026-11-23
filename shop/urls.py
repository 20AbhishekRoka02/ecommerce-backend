from rest_framework import routers
from shop.views import ProductViewSet, CategoryViewSet, ComapanyConfigViewSet

router = routers.SimpleRouter()
router.register(r'product', ProductViewSet)
router.register(r'category', CategoryViewSet)
router.register(r'companyconfig', ComapanyConfigViewSet)
urlpatterns = router.urls
