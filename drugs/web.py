

from django.shortcuts import render, redirect, get_object_or_404
from .models import Drug
from .forms import DrugForm

# عرض جميع الأدوية
def drug_list(request):
    drugs = Drug.objects.all()
    return render(request, 'drugs/drug_list.html', {'drugs': drugs})

# إضافة دواء جديد
def add_drug(request):
    if request.method == 'POST':
        form = DrugForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('drug_list')  # تأكد من أن الاسم مطابق في urls
    else:
        form = DrugForm()
    return render(request, 'drugs/add_drug.html', {'form': form})


def edit_drug(request, id):
    drug = get_object_or_404(Drug, id=id)
    form = DrugForm(request.POST or None, instance=drug)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('drug_list')
    return render(request, 'drugs/edit_drug.html', {'form': form})


def delete_drug(request, id):
    drug = get_object_or_404(Drug, id=id)
    if request.method == 'POST':
        drug.delete()
        return redirect('drug_list')
    return render(request, 'drugs/delete_confirm.html', {'drug': drug})
