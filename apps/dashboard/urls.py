from django.urls import path

from apps.dashboard import views



urlpatterns = [
    
    path('', views.dashboard, name="index"),
    # path('orders-summary/', views.orders_summary, name='orders-summary'),
    # path('charts/orders-growth/', views.orders_growth_chart, name='orders-growth'),
    # path('charts/monthly-revenue/', views.monthly_revenue_chart, name='monthly-revenue'),
    # path('orders/recent/', views.recent_orders_api, name='recent-orders'),
    # path('workers/top/', views.top_workers_api, name='top-workers'),
    # path('active-workers/', views.active_workers_count, name='active-workers'),
    # path('average-rating/', views.average_customer_rating, name='average-rating'),
    # path('total-revenue/', views.total_revenue_view, name='total-revenue'),
]