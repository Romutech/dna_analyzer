from django.shortcuts import render, redirect, get_object_or_404

def matching(request):
    return render(request, 'dna_matching/matching.html')
