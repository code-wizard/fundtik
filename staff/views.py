
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.db.models import Q
from .models import Staff
from django import forms

class StaffForm(forms.ModelForm):
	class Meta:
		model = Staff
		fields = ['first_name', 'last_name', 'email', 'position']

def staff_list(request):
	search_query = request.GET.get('search', '')
	staff_list = Staff.objects.all()
	
	if search_query:
		staff_list = staff_list.filter(
			Q(first_name__icontains=search_query) |
			Q(last_name__icontains=search_query) |
			Q(email__icontains=search_query) |
			Q(position__icontains=search_query)
		)
	
	staff_list = staff_list.order_by('-created_at')
	context = {
		'staff_list': staff_list,
		'search_query': search_query
	}
	return render(request, 'staff/list.html', context)

def staff_create(request):
	if request.method == 'POST':
		form = StaffForm(request.POST)
		if form.is_valid():
			form.save()
			if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
				return JsonResponse({'success': True})
			return redirect('staff_list')
		else:
			if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
				return JsonResponse({'success': False, 'errors': form.errors})
	else:
		form = StaffForm()
	return render(request, 'staff/form.html', {'form': form, 'action': 'Add'})

def staff_edit(request, pk):
	staff = get_object_or_404(Staff, pk=pk)
	if request.method == 'POST':
		form = StaffForm(request.POST, instance=staff)
		if form.is_valid():
			form.save()
			if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
				return JsonResponse({'success': True})
			return redirect('staff_list')
		else:
			if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
				return JsonResponse({'success': False, 'errors': form.errors})
	else:
		form = StaffForm(instance=staff)
	return render(request, 'staff/form.html', {'form': form, 'action': 'Edit'})

def staff_delete(request, pk):
	staff = get_object_or_404(Staff, pk=pk)
	if request.method == 'POST':
		staff.delete()
		return redirect('staff_list')
	return render(request, 'staff/confirm_delete.html', {'staff': staff})
