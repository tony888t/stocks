from django.urls import path, include

from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r"stocks", views.StockViewSet, basename="stock")
router.register(
    r"admin-stocks", views.StockAdminViewSet, basename="admin-stock"
)
router.register(
    r"transactions", views.TransactionViewSet, basename="transaction"
)
router.register(r"portfolio", views.PortfolioViewSet, basename="portfolio")

urlpatterns = [
    path("", include(router.urls)),
]
