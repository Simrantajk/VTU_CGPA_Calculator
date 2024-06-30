from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.utils.datastructures import MultiValueDictKeyError
from .models import Scheme, Branch, Sem, Subject

def welcome(request):
    return render(request, 'welcome.html')

def calculate(request):
    schemes = Scheme.objects.all()
    branches = Branch.objects.all()
    semesters = Sem.objects.all()

    context = {
        'schemes': schemes,
        'branches': branches,
        'semesters': semesters,
    }
    
    return render(request, 'calculate.html', context)

def fetch_subjects(request):
    scheme_id = request.GET.get('scheme')
    branch_id = request.GET.get('branch')
    semester_id = request.GET.get('semester')

    try:
        subjects = Subject.objects.filter(
            sem__branch__scheme_id=scheme_id,
            sem__branch_id=branch_id,
            sem_id=semester_id
        )
        subjects_data = [
            {
                'course_id': subject.sub_id,
                'title': subject.sub_name,
                'credits': subject.credits,
                'max_marks': subject.max_marks
            }
            for subject in subjects
        ]
        return JsonResponse(subjects_data, safe=False)
    except Subject.DoesNotExist:
        return JsonResponse([], safe=False)

def add(request):
    if request.method == 'POST':
        try:
            # Get data from form
            scheme_id = int(request.POST['scheme'])
            branch_name = request.POST['branch_name']
            branch_code = request.POST['branch_code']
            sem_number = int(request.POST['sem'])
            num_subjects = int(request.POST['num_subjects'])
            
            # Get or create scheme
            scheme_instance, _ = Scheme.objects.get_or_create(scheme=scheme_id)
            
            # Get or create branch within the scheme
            branch_instance, _ = Branch.objects.get_or_create(
                name=branch_name,
                code=branch_code,
                scheme=scheme_instance
            )
            
            # Get or create semester within the branch
            semester_instance, _ = Sem.objects.get_or_create(
                sem=sem_number,
                branch=branch_instance
            )
            
            # Loop through subjects and create them
            for i in range(num_subjects):
                sub_code = request.POST[f'sub_code_{i}']
                sub_name = request.POST[f'sub_name_{i}']
                credits = int(request.POST[f'credits_{i}'])
                max_marks = int(request.POST[f'max_marks_{i}'])
                
                # Create subject linked to the semester
                Subject.objects.create(
                    sub_code=sub_code,
                    sub_name=sub_name,
                    credits=credits,
                    max_marks=max_marks,
                    sem=semester_instance
                )
            
            return redirect('calculate')  # Redirect to the calculate page after submission
        
        except MultiValueDictKeyError:
            # Handle the case where 'num_subjects' or any other expected key is missing
            # You can redirect to the form page with an error message or handle it as needed
            return render(request, 'add.html', {'error_message': 'Form data missing or invalid.'})
    
    return render(request, 'add.html')

def cgpa(request):
    return render(request, 'cgpa.html')
