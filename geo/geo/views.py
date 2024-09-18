from django.shortcuts import redirect


def index(request):
    """Main domain page"""
    return redirect("polygon")
