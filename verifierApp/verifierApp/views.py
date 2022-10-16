from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages

from .forms import urlForm
from .src.verify import get_results, is_valid_URL, get_trust_stores

lista_urls = []
lista_colors = []
lista_browsers = ['Microsoft Edge', 'Google Chrome', 'Mozilla Firefox']

microsoft_store, google_store, mozilla_store = get_trust_stores()

def index(request):
  global lista_colors
  global lista_urls
  display = True
  if request.method == 'POST':
    form = urlForm(request.POST)
    if form.is_valid():

      # Obteniendo URL como string
      url_string = form.cleaned_data['url']

      # validación de URL
      valid_url, response = is_valid_URL(url_string)

      # si es válida y existe la URL
      if valid_url == True:
        lista_urls.insert(0, url_string)

         # Funcion que verifica el nivel de confianza
        lista_browsers_colors = get_results(url_string)
        lista_colors.insert(0, lista_browsers_colors)

        # para mostrar el nivel de confianza con colores
        results = zip(lista_urls, lista_colors)
        context = {'form': form,
                    'lista_browsers':lista_browsers,
                    'results':results,
                    'display': display}
      # si no es válida y no existe la URL
      else:
        # Para mostrar mensajes de error
        messages.add_message(request, messages.ERROR, response)

        # si la lista de URLs esta vacia
        if len(lista_urls) == 0:
          display = False
          context = {'form': form,
                      'display': display}
        # si la lista de URLs no esta vacia
        else:
          results = zip(lista_urls, lista_colors)
          context = {'form': form,
                      'lista_browsers':lista_browsers,
                      'results':results,
                      'display': display}
      return render(request, 'form.html', context)
  elif request.method == 'GET':
    form = urlForm()
    results = zip(lista_urls, lista_colors)

    if len(lista_urls) == 0:
      display = False
      context = {'form': form, 'display': display}
    else:
      display = True
      context = {'form': form,
                'lista_browsers':lista_browsers,
                'results':results,
                'display': display}
    return render(request, 'form.html', context)

def clean(request):
  global lista_colors
  global lista_urls
  lista_urls = []
  lista_colors = []
  return redirect('index')

def google_trust_Store(request):
  return render(request, "google_trust_store/google_trust_store.html", {'certificates': google_store})

def microsoft_trust_Store(request):
  return render(request, "microsoft_trust_store/microsoft_trust_store.html", {'certificates': microsoft_store})

def mozilla_trust_Store(request):
  return render(request, "mozilla_trust_store/mozilla_trust_store.html", {'certificates': mozilla_store})