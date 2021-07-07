from ccip.forms import ClientForm, ImplantForm, SurgeryForm
from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .models import *

# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return render(request, 'busers/register.html')
    else:
        user = get_object_or_404(User, pk=request.user.id)
        u_email = User.objects.filter(pk = request.user.id).values_list('email', flat=True)[0]
        
        surgerys = Surgery.objects.all().filter(user = user).order_by("-date")
        n_surg = len(surgerys)
        n = 0
        for i in range(n_surg):
            n += surgerys[i].quantity
        if n > 0:
            ratio = n / n_surg
        else:
            ratio = 0

        return render(request, 'ccip/index.html', {'user': user,'u_email':u_email, 'surgerys': surgerys, 'n_surg': n_surg, 'n': n, 'ratio': round(ratio, 2)})

def quant(request):
    if not request.user.is_authenticated:
        return render(request, 'busers/register.html')
    else:
        if request.method == "GET":
            u_email = User.objects.filter(pk = request.user.id).values_list('email', flat=True)[0]
            return render(request, 'ccip/quant.html', {'u_email': u_email})
        if request.method == "POST":
            u_email = User.objects.filter(pk = request.user.id).values_list('email', flat=True)[0]
            user = get_object_or_404(User, pk=request.user.id)
            quant = request.POST['quant']
            if not quant or int(quant) <= 0:
                return redirect('quant')
            else:
                clients = Client.objects.filter(user = user).values('full_name')
                stageOpt = ['Espera','Andamento','Finalizado']
                return render(request, 'ccip/add_surgery.html', {'quant': quant, 'clients': clients, 'stageOpt': stageOpt,'u_email': u_email})

def add_surgery(request):
    if not request.user.is_authenticated:
        return render(request, 'busers/register.html')
    else:
        if request.method == 'GET':
            u_email = User.objects.filter(pk = request.user.id).values_list('email', flat=True)[0]
            return render(request, 'ccip/add_surgery.html', {'u_email': u_email} )
        else:
            u_email = User.objects.filter(pk = request.user.id).values_list('email', flat=True)[0]
            user = get_object_or_404(User, pk=request.user.id)
            client_name = request.POST['client']
            clients = Client.objects.filter(full_name = client_name)
            client = clients[0]
            date = request.POST['date']
            quantity = request.POST['quantity']
            obs = request.POST['obs']
            stage = request.POST['stage']
            prot = request.POST['prot']
            
            areaList = []
            typeList = []
            sizeList = []
            implanteList = []
            stock = list(Implant.objects.all().filter(user = user))
            
            for i in range(int(quantity)):
                j = i + 1

                type = request.POST['type' + str(j)]
                size = request.POST['size' + str(j)]
                
                areaList.append(request.POST['area' + str(j)])
                typeList.append(type)
                sizeList.append(size)
                implante = str(typeList[i]) + ' ' + str(sizeList[i])
                implanteList.append(implante)
                imp = list(Implant.objects.all().filter(user = user, type = type, size = size))
                
                if imp == []:
                    messages.warning(request, "Checar estoque de implantes.")
                    
                else:
                    quant = imp[0].quantity
                    
                    Implant.objects.filter(user = user, type = type, size = size).update(quantity = (quant - 1) )
                    impl = Implant.objects.filter(user = user, type = type, size = size)
                    if impl[0].quantity <= 0:
                        Implant.objects.filter(user = user, type = type, size = size).update(quantity = 0 )
                        
                        messages.warning(request, 'Checar estoque de implantes.')
                        
                
            
            user = get_object_or_404(User, pk=request.user.id)
            surgery = Surgery.objects.create(
                user = user,
                client = client,
                date = date,
                quantity = quantity,
                implant_type = typeList,
                implant_size = sizeList,
                obs = obs,
                area = areaList,
                stage = stage,
                pmu = prot
            )
            try:
                surgery.save()
            except:
                messages.error(request, "Erro ao cadastrar nova cirurgia.")
                return redirect('quant')
            messages.success(request, "Cirurgia adicionada com sucesso!")
            return redirect('index')

def update_surgery(request, surgery_id):
    if not request.user.is_authenticated:

        return render(request, 'busers/register.html',)
    else:
        if request.method == "GET":
            u_email = User.objects.filter(pk = request.user.id).values_list('email', flat=True)[0]
            u_email = User.objects.filter(pk = request.user.id).values_list('email', flat=True)[0]
            user = get_object_or_404(User, pk=request.user.id)
            surgery = Surgery.objects.get(user=user, pk=surgery_id)
            form = SurgeryForm(instance=surgery)
            types = surgery.implant_type
            sizes = surgery.implant_size
            areas = surgery.area
            
            return render(request, "ccip/update_surgery.html", {'form': form, 'types': types, 'sizes': sizes, 'areas': areas, 'u_email': u_email})
        else:
            areaList = []
            typeList = []
            sizeList = []
            
            user = get_object_or_404(User, pk=request.user.id)
            surgery = Surgery.objects.get(user=user, pk=surgery_id)
            client = request.POST['client']
            
            date = request.POST['date']
            quantity = request.POST['quantity']
            for i in range(int(quantity)):
                areaList.append(request.POST["area" + str(i+1)])
                typeList.append(request.POST["type" + str(i+1)])
                sizeList.append(request.POST["size" + str(i+1)])
            obs = request.POST['obs']
            stage = request.POST['stage']
            pmu = request.POST['pmu']

            
            surgery = Surgery.objects.filter(user=user, pk=surgery_id).update(date=date, client=client, quantity=quantity, area=areaList,implant_type=typeList, implant_size=sizeList, obs=obs, stage=stage, pmu=pmu)
            messages.success(request, 'Cirurgia atualizada com sucesso!')
            return redirect('index')

def delete_surgery(request, surgery_id):
    user = get_object_or_404(User, pk=request.user.id)
    surg = Surgery.objects.get(user = user, pk=surgery_id)
    surg.delete()
    return redirect('index')

def add_implant(request):
    if not request.user.is_authenticated:
        return render(request, 'busers/register.html')
    else:
        if request.method == "POST":
            user = get_object_or_404(User, pk=request.user.id)
            u_email = User.objects.filter(pk = request.user.id).values_list('email', flat=True)[0]
            type = request.POST['type']
            size = request.POST['size']
            quantity = request.POST['quantity']
            imp = list(Implant.objects.all().filter(user = user, type = type, size = size))
            if imp == []:
                messages.success(request, "Implante adicionado com sucesso!")
                Implant.objects.create(
                    user = user,
                    type = type,
                    size = size,
                    quantity = quantity
                )
            else:
                implant_to_update = Implant.objects.all().filter(user = user, type = type, size = size)
                add = implant_to_update[0].quantity
                implant_to_update.update(quantity = int(add) + int(quantity))
                messages.success(request, "Implante atualizado com sucesso!")
            return redirect('stock')
        else:
            u_email = User.objects.filter(pk = request.user.id).values_list('email', flat=True)[0]
            form = ImplantForm
            return render(request, "ccip/add_implant.html", {'form': form, 'u_email': u_email})

def stock(request):
    if not request.user.is_authenticated:
        return render(request, 'busers/register.html')
    else:
        if request.method == "GET":
            u_email = User.objects.filter(pk = request.user.id).values_list('email', flat=True)[0]
            user = get_object_or_404(User, pk=request.user.id)
            stock = Implant.objects.all().filter(user = user)
            return render(request, 'ccip/stock.html', {'stock': stock, 'u_email': u_email})

def delete_implant(request, implant_id):
    if not request.user.is_authenticated:
        return render(request, 'busers/register.html')
    else:
        user = get_object_or_404(User, pk=request.user.id)
        imp_to_delete = Implant.objects.get(user = user, pk = implant_id)
        imp_to_delete.delete()
        return redirect('stock')

def update_implant(request, implant_id):
    if not request.user.is_authenticated:
        return render(request, 'busers/register.html')
    else:
        if request.method == "GET":
            u_email = User.objects.filter(pk = request.user.id).values_list('email', flat=True)[0]
            user = get_object_or_404(User, pk=request.user.id)
            implants = Implant.objects.get(user=user, pk=implant_id)
            form = ImplantForm(instance=implants)
            return render(request, 'ccip/update_implant.html', {'form': form, 'u_email': u_email})
        if request.method == "POST":
            user = get_object_or_404(User, pk=request.user.id)
            type = request.POST['type']
            size = request.POST['size']
            quant = request.POST['quantity']
            implants = Implant.objects.all().filter(user=user, pk=implant_id).update(quantity = quant, type = type, size = size)
            return redirect('stock')

def add_client(request):
    if not request.user.is_authenticated:
        return render(request, 'busers/register.html')
    else:
        if request.method == "GET":
            u_email = User.objects.filter(pk = request.user.id).values_list('email', flat=True)[0]
            form = ClientForm
            return render(request, 'ccip/add_client.html', {'form': form, 'u_email': u_email})
        else:
            user = get_object_or_404(User, pk=request.user.id)
            name = request.POST['full_name']
            birth = request.POST['birth_date']
            gender = request.POST['gender']
            phone = request.POST['phone']
            obs = request.POST['obs']
            client_name = list(Client.objects.all().filter(user = user, full_name = name))
            
            if client_name == []:
                Client.objects.create(
                    user = user,
                    full_name = name,
                    birth_date = birth,
                    gender = gender,
                    phone = phone,
                    obs = obs,
                )
                messages.success(request, "Cliente cadastrado com sucesso!")
                return redirect('client_list')
            else:
                Client.objects.create(
                    user = user,
                    full_name = name,
                    birth_date = birth,
                    phone = phone,
                    obs = obs,
                )
                messages.warning(request, "Cliente possivelmente já cadastrado.")
                return redirect("client_list")

def client_list(request):
    if not request.user.is_authenticated:
        return render(request, 'busers/register.html')
    else:
        u_email = User.objects.filter(pk = request.user.id).values_list('email', flat=True)[0]
        user = get_object_or_404(User, pk=request.user.id)
        clients = Client.objects.all().filter(user = user).order_by('full_name')
        return render(request, 'ccip/client_list.html', {'clients': clients, 'u_email': u_email})

def delete_client(request, client_id):
    if not request.user.is_authenticated:
        return render(request, 'busers/register.html')
    else:
        user = get_object_or_404(User, pk=request.user.id)
        client = Client.objects.all().filter(user=user, pk=client_id)
        client.delete()
        messages.warning(request, "Cliente excluído.")
        return redirect('client_list')

def update_client(request, client_id):
    if not request.user.is_authenticated:
        return render(request, 'busers/register.html')
    else:
        if request.method == "GET":
            u_email = User.objects.filter(pk = request.user.id).values_list('email', flat=True)[0]
            user = get_object_or_404(User, pk=request.user.id)
            clients = Client.objects.get(user=user, pk=client_id)
            form = ClientForm(instance=clients)
            return render(request, 'ccip/update_client.html', {'form': form, 'u_email': u_email})
        if request.method == "POST":
            user = get_object_or_404(User, pk=request.user.id)
            name = request.POST['full_name']
            birth = request.POST['birth_date']
            phone = request.POST['phone']
            obs = request.POST['obs']
            clients = Client.objects.all().filter(user=user, pk=client_id).update(full_name = name, birth_date = birth, phone = phone, obs = obs)
            messages.success(request, "Dados do cliente atualizados com sucesso!")
            return redirect('client_list')