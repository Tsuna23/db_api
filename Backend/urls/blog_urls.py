from django.urls import path
from Backend.views.blog_view import*

urlpatterns = [
    # =========================
    # ADMIN — DASHBOARD
    # =========================
    path("blog/create/", BlogCreateView.as_view(), name="blog-create"),  # POST
    path("blog/<slug:slug>/update/", BlogUpdateView.as_view(), name="blog-update"),  # PUT
    path("blog/<slug:slug>/delete/", BlogDeleteView.as_view(), name="blog-delete"),  # DELETE
    path("blog/admin/", BlogListView.as_view(), name="blog-list"),  # GET (admin)
    
    # =========================
    # PUBLIC — SITE VITRINE
    # =========================
    path("blog/", BlogCatalogueView.as_view(), name="blog-catalogue"),  # GET (public)
    path("blog/<slug:slug>/", BlogDetailPublicView.as_view(), name="blog-detail-public"),  # GET (public)
]