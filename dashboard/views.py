from django.shortcuts import render
from ccip.forms import ClientForm, ImplantForm, SurgeryForm
from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.conf import settings
from ccip.models import *
from collections import Counter, OrderedDict
from .fusioncharts import FusionCharts
from datetime import datetime, timedelta, date

# Create your views here.

def dashboard(request):
    if not request.user.is_authenticated:
        return render(request, 'busers/register.html')
    else:
        u_email = User.objects.filter(pk = request.user.id).values_list('email', flat=True)[0]
        user = get_object_or_404(User, pk=request.user.id)
        test = Surgery.objects.values_list('date').filter(user = user).order_by('date')
        if test:
            first_surg_dates = Surgery.objects.values_list('date').filter(user = user).order_by('date')[0]
            first_surg_date = first_surg_dates[0].strftime('%Y-%m-%d')
        else:
            first_surg_dates = date.today()
            first_surg_date = first_surg_dates.strftime('%Y-%m-%d')
        
        size_type_list = []
        type_list = []
        size_list = []
        all_sizes = []
        all_types = []
        if request.method == "GET":
            sizes = Surgery.objects.all().filter(user = user)
            surgerys = Surgery.objects.all().filter(user = user).order_by("-date")
        else:
            if request.POST['date_a'] < first_surg_date:
                try:
                    surgerys = Surgery.objects.all().filter(user = user, date__range=(first_surg_date, request.POST['date_z'])).order_by("-date")
                    sizes = Surgery.objects.all().filter(user = user, date__range=(first_surg_date, request.POST['date_z'])).order_by("-date")
                except:
                    return redirect('index')
            elif request.POST['date_a'] and request.POST['date_a'] != "":
                try:
                    surgerys = Surgery.objects.all().filter(user = user, date__range=(request.POST['date_a'], request.POST['date_z'])).order_by("-date")
                    sizes = Surgery.objects.all().filter(user = user, date__range=(request.POST['date_a'], request.POST['date_z'])).order_by("-date")
                except:
                    return redirect('index')
            elif request.POST['date_a'] >= request.POST['date_z']:
                try:
                    surgerys = Surgery.objects.all().filter(user = user, date__range=(request.POST['date_z'], request.POST['date_a'])).order_by("-date")
                    sizes = Surgery.objects.all().filter(user = user, date__range=(request.POST['date_z'], request.POST['date_a'])).order_by("-date")
                except:
                    return redirect('index')
            else:
                try:
                    sizes = Surgery.objects.all().filter(user = user)
                    surgerys = Surgery.objects.all().filter(user = user).order_by("-date")
                except:
                    return redirect('index')
        for i in sizes:
            all_sizes.extend(i.implant_size)
            all_types.extend(i.implant_type)
        imp_dict = dict(Counter(all_sizes))
        type_dict = dict(Counter(all_types))
        sizes = sorted(imp_dict.items(), key=lambda x: x[1], reverse=True)
        types = sorted(type_dict.items(), key=lambda x: x[1], reverse=True)
        size_chart_col = get_size_chart(sizes[0:6])[0]
        size_chart_pie = get_size_chart(sizes[0:6])[1]
        type_chart_pie = get_type_chart(types[0:6])[0]
        type_chart_col = get_type_chart(types[0:6])[1]
        
        
        
        for surgery in surgerys:
            type_list.extend(surgery.implant_type)
            size_list.extend(surgery.implant_size)
        if len(type_list) == len(size_list):
            for i in range(len(type_list)):
                size_type_list.append(str(type_list[i]) + " " + str(size_list[i]))
            size_type_dict =  dict(Counter(size_type_list))
            size_type_sorted = sorted(size_type_dict.items(), key=lambda x: x[1], reverse=True)
            
        else:
            size_type_sorted = []

        
        
        
        n_surg = len(surgerys)
        n = 0
        for i in range(n_surg):
            n += surgerys[i].quantity
        if n > 0:
            ratio = n / n_surg
        else:
            ratio = 0
        area_list = []
        for surgery in surgerys:
            area_list.extend(surgery.area)
        
        area_list_counter =  dict(Counter(area_list))
        area_list_sorted = sorted(area_list_counter.items(), key=lambda x: x[1], reverse=True)
        
        month_lists = []
        for surgery in surgerys:
            month_number = str(surgery.date.month)
            datetime_object = datetime.strptime(month_number, "%m")
            month_name = datetime_object.strftime("%b")
            
            month_lists.append(month_name)

        month_list_a = dict(Counter(month_lists))
        month_list = sorted(month_list_a.items(), key=lambda x: x[1], reverse=True)
        ages = []
        gender = []
        ages_ratio = 0
        date_format = "%Y-%m-%d"
        for surgery in surgerys:
            date_a = datetime.strptime(str(surgery.client.birth_date), date_format )
            date_b = datetime.strptime(str(surgery.date), date_format)
            age = (date_b - date_a)
            ages.append(int(age.days/365))
            ages_ratio = int(sum(ages) / len(ages))
            if ages_ratio > 0:
                ages_ratio = ages_ratio
            elif ages_ratio == None:
                ages_ratio = 0
            else:
                ages_ratio = 0
            gender.append(surgery.client.gender)
        genderss = dict(Counter(gender))
        genders = sorted(genderss.items(), key=lambda x: x[1], reverse=True)
        
        pmus = []
        for surgery in surgerys:
            pmus.append(surgery.pmu)
            
        pmu_counted = dict(Counter(pmus))
        pmu_sorted = sorted(pmu_counted.items(), key=lambda x: x[1], reverse=True)
        
        pmu_chart_col = get_pmu_chart(pmu_sorted)[0]
        pmu_chart_pie = get_pmu_chart(pmu_sorted)[1]
        size_type_chart_col = get_individual_chart(size_type_sorted[0:10])[0]
        size_type_chart_pie = get_individual_chart(size_type_sorted[0:10])[1]
        month_chart_col = get_month_chart(month_list)[0]
        month_chart_pie = get_month_chart(month_list)[1]
        area_chart_col = get_area_chart(area_list_sorted[0:5])[0]
        area_chart_pie = get_area_chart(area_list_sorted[0:5])[1]
        gender_chart_col = get_gender_chart(genders)[0]
        gender_chart_pie = get_gender_chart(genders)[1]
        #age_chart_col = get_age_chart(ages)
        dates = []
        surg_dates = Surgery.objects.values_list('date').filter(user = user).order_by('date')
        for surgery in surgerys:
            dates.append(surgery.date)
        print(dates)
        if dates == []:
            ini_date = " "
            final_date = " "
        elif len(dates) == 1:
            ini_date = dates[0].strftime('%d/%m/%Y')
            final_date = dates[1].strftime('%d/%m/%Y')
        else:
            print('aqui')
            dates.sort()
            ini_date = dates[0].strftime('%d/%m/%Y')
            final_date = dates[len(dates) - 1].strftime('%d/%m/%Y')

        
        return render(request, 'dashboard/dashboard.html', 
        {'size_chart_pie': size_chart_pie.render(), 
        'size_chart_col': size_chart_col.render(), 
        'type_chart_pie': type_chart_pie.render(), 
        'type_chart_col': type_chart_col.render(),
        'size_type_chart_col': size_type_chart_col.render(),
        'size_type_chart_pie': size_type_chart_pie.render(),
        'ratio': round(ratio, 2),
        'n': n,
        'n_surg': n_surg,
        'area_chart_col': area_chart_col.render(),
        'area_chart_pie': area_chart_pie.render(),
        'month_chart_col': month_chart_col.render(),
        'month_chart_pie': month_chart_pie.render(),
        'ages_ratio': ages_ratio,
        'gender_chart_col': gender_chart_col.render(),
        'gender_chart_pie': gender_chart_pie.render(),
        'pmu_chart_col': pmu_chart_col.render(),
        'pmu_chart_pie': pmu_chart_pie.render(),
        'ini_date': ini_date,
        'final_date': final_date,
        'u_email': u_email,
        })

def get_pmu_chart(pmu_sorted):
    
    dataSource0 = OrderedDict()
    chartConfig0 = OrderedDict()
    chartConfig0 = OrderedDict()
    chartConfig0["palettecolors"] = "3C7EDD, 1FD826,E7E422,E74C22,CC4ADE,EAA829,56DFF1,E463CD"
    chartConfig0["caption"] = "Tipo de Reabilitação"
    chartConfig0["subCaption"] = ""
    chartConfig0["xAxisName"] = "Tipo"
    chartConfig0["yAxisName"] = "Quantidade"
    chartConfig0["numberSuffix"] = ""
    chartConfig0["theme"] = "fusion"

    dataSource0["data"] = []
    for k, v in pmu_sorted:
        
        dataSource0['data'].append({"label":'{}'.format(k), "value": '{}'.format(v)} )    
        

    dataSource0["chart"] = chartConfig0

    pmu_chart_pie = FusionCharts("pie2d", "pmu_chart_pie", "100%", "350", "pmu_chart_pie-container", "json", dataSource0)
    pmu_chart_col = FusionCharts("column2d", "pmu_chart_col", "100%", "350", "pmu_chart_col-container", "json", dataSource0)
    return pmu_chart_pie, pmu_chart_col

def get_month_chart(month_list):
    dataSource0 = OrderedDict()
    chartConfig0 = OrderedDict()
    chartConfig0 = OrderedDict()
    chartConfig0["palettecolors"] = "3C7EDD, 1FD826,E7E422,E74C22,CC4ADE,EAA829,56DFF1,E463CD"
    chartConfig0["caption"] = "Meses com Maior Incidência de Cirurgias"
    chartConfig0["subCaption"] = ""
    chartConfig0["xAxisName"] = "Mês"
    chartConfig0["yAxisName"] = "Quantidade"
    chartConfig0["numberSuffix"] = ""
    chartConfig0["theme"] = "fusion"
    chartConfig0["chartType"] = "column2d,pie2d"
    dataSource0["data"] = []
    for k, v in month_list:
        dataSource0['data'].append({"label":'{}'.format(k), "value": '{}'.format(v)} )   
    dataSource0["chart"] = chartConfig0

    month_chart_col = FusionCharts("column2d", "month_chart_col", "100%", "350", "month_chart_col-container", "json", dataSource0)
    month_chart_pie = FusionCharts("pie2d", "month_chart_pie", "100%", "350", "month_chart_pie-container", "json", dataSource0)
    return month_chart_col, month_chart_pie

def get_area_chart(area_list_sorted):
    
    dataSource0 = OrderedDict()
    chartConfig0 = OrderedDict()
    chartConfig0 = OrderedDict()
    chartConfig0["palettecolors"] = "3C7EDD, 1FD826,E7E422,E74C22,CC4ADE,EAA829,56DFF1,E463CD"
    chartConfig0["caption"] = "Regiões Mais Frequentes"
    chartConfig0["subCaption"] = ""
    chartConfig0["xAxisName"] = "Região"
    chartConfig0["yAxisName"] = "Quantidade"
    chartConfig0["numberSuffix"] = ""
    chartConfig0["theme"] = "fusion"
    chartConfig0["chartType"] = "pie2d,column2d"
    dataSource0["data"] = []
    for k, v in area_list_sorted:
        dataSource0['data'].append({"label":'{}'.format(k), "value": '{}'.format(v)} )   
    dataSource0["chart"] = chartConfig0

    area_chart_col = FusionCharts("column2d", "area_chart_col", "100%", "350", "area_chart_col-container", "json", dataSource0)
    area_chart_pie = FusionCharts("pie2d", "area_chart_pie", "100%", "350", "area_chart_pie-container", "json", dataSource0)
    return area_chart_col, area_chart_pie

def get_size_chart(sizes):
    
    dataSource0 = OrderedDict()
    chartConfig0 = OrderedDict()
    chartConfig0 = OrderedDict()
    #chartConfig0["palettecolors"] = "5d62b5,29c3be,f2726f,ff8000,990099,00ffff"
    chartConfig0["palettecolors"] = "3C7EDD, 1FD826,E7E422,E74C22,CC4ADE,EAA829,56DFF1,E463CD"
    chartConfig0["caption"] = "Tamanhos Mais Utilizados"
    chartConfig0["subCaption"] = "Quantidade x Dimensão"
    chartConfig0["xAxisName"] = "Dimensão"
    chartConfig0["yAxisName"] = "Quantidade"
    chartConfig0["numberSuffix"] = ""
    chartConfig0["theme"] = "fusion"
    
    dataSource0["data"] = []
    for k, v in sizes:
        
        dataSource0['data'].append({"label":'{}'.format(k), "value": '{}'.format(v)} )    
        
    
    dataSource0["chart"] = chartConfig0

    size_chart_col = FusionCharts("column2d", "size_chart_col", "100%", "350", "size_chart_col-container", "json", dataSource0)
    size_chart_pie = FusionCharts("pie2d", "size_chart_pie", "100%", "350", "size_chart_pie-container", "json", dataSource0)
    return size_chart_col, size_chart_pie

def get_type_chart(types):
    
    dataSource0 = OrderedDict()
    chartConfig0 = OrderedDict()
    chartConfig0 = OrderedDict()
    chartConfig0["palettecolors"] = "3C7EDD, 1FD826,E7E422,E74C22,CC4ADE,EAA829,56DFF1,E463CD"
    chartConfig0["caption"] = "Espécies Mais Utilizadas"
    chartConfig0["subCaption"] = "Quantidade x Espécie"
    chartConfig0["xAxisName"] = "Espécie"
    chartConfig0["yAxisName"] = "Quantidade"
    chartConfig0["numberSuffix"] = ""
    chartConfig0["theme"] = "fusion"

    dataSource0["data"] = []
    for k, v in types:
        
        dataSource0['data'].append({"label":'{}'.format(k), "value": '{}'.format(v)} )    
        

    dataSource0["chart"] = chartConfig0

    type_chart_pie = FusionCharts("pie2d", "type_chart_pie", "100%", "350", "type_chart_pie-container", "json", dataSource0)
    type_chart_col = FusionCharts("column2d", "type_chart_col", "100%", "350", "type_chart_col-container", "json", dataSource0)
    return type_chart_pie, type_chart_col

def get_individual_chart(size_type_sorted):
    
    dataSource0 = OrderedDict()
    chartConfig0 = OrderedDict()
    chartConfig0 = OrderedDict()
    chartConfig0["palettecolors"] = "3C7EDD, 1FD826,E7E422,E74C22,CC4ADE,EAA829,56DFF1,E463CD"
    chartConfig0["caption"] = "Implantes Mais Utilizados"
    chartConfig0["subCaption"] = "Quantidade x Implante"
    chartConfig0["xAxisName"] = "Dimensão"
    chartConfig0["yAxisName"] = "Quantidade"
    chartConfig0["numberSuffix"] = ""
    chartConfig0["theme"] = "fusion"

    dataSource0["data"] = []
    for k, v in size_type_sorted:
        
        dataSource0['data'].append({"label":'{}'.format(k), "value": '{}'.format(v)} )    
        

    dataSource0["chart"] = chartConfig0

    size_type_chart_col = FusionCharts("column2d", "size_type_chart_col", "100%", "400", "size_type_chart_col-container", "json", dataSource0)
    size_type_chart_pie = FusionCharts("pie2d", "size_type_chart_pie", "100%", "400", "size_type_chart_pie-container", "json", dataSource0)
    return size_type_chart_col, size_type_chart_pie

def get_gender_chart(genders):
    
    dataSource0 = OrderedDict()
    chartConfig0 = OrderedDict()
    chartConfig0 = OrderedDict()
    chartConfig0["palettecolors"] = "3C7EDD, 1FD826,E7E422,E74C22,CC4ADE,EAA829,56DFF1,E463CD"
    chartConfig0["caption"] = "Gêneros"
    chartConfig0["subCaption"] = ""
    chartConfig0["xAxisName"] = "Gênero"
    chartConfig0["yAxisName"] = "Quantidade"
    chartConfig0["numberSuffix"] = ""
    chartConfig0["theme"] = "fusion"

    dataSource0["data"] = []
    for k, v in genders:
        
        dataSource0['data'].append({"label":'{}'.format(k), "value": '{}'.format(v)} )    
        

    dataSource0["chart"] = chartConfig0

    gender_chart_pie = FusionCharts("pie2d", "gender_chart_pie", "100%", "350", "gender_chart_pie-container", "json", dataSource0)
    gender_chart_col = FusionCharts("column2d", "gender_chart_col", "100%", "350", "gender_chart_col-container", "json", dataSource0)
    return gender_chart_pie, gender_chart_col