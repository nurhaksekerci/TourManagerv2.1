from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *
from .serializers import *

@api_view(['GET', 'POST', 'DELETE'])
def note_list(request):
    # GET request: Email'e göre notları döndür
    if request.method == 'GET':
        email = request.query_params.get('email', None)  # GET isteği ile gelen email parametresini al
        if email:
            notes = Note.objects.filter(email=email)  # Email'e göre filtrele
            if notes.exists():
                serializer = NoteSerializer(notes, many=True)
                return Response(serializer.data)
            else:
                return Response({"detail": "No notes found for this email."}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"detail": "Email query parameter is required."}, status=status.HTTP_400_BAD_REQUEST)

    # POST request: Yeni bir not oluştur (Email ile birlikte)
    elif request.method == 'POST':
        email = request.data.get('email', None)  # POST isteği ile gelen email parametresini al
        if email:
            serializer = NoteSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"detail": "Email field is required in POST request."}, status=status.HTTP_400_BAD_REQUEST)

    # DELETE request: ID ve Email'e göre belirli bir notu sil
    elif request.method == 'DELETE':
        print(f' body:  {request.body}')  # Ham isteği görmek için
        note_id = request.query_params.get('id', None)  # Query parametresi ile ID al
        if note_id:
            try:
                note = Note.objects.get(id=note_id)
                note.delete()
                return Response({"detail": "Note deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
            except Note.DoesNotExist:
                return Response({"detail": "Note not found."}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"detail": "ID is required in DELETE request."}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST', 'DELETE'])
def task_list(request):
    # GET request: Email'e göre görevleri döndür
    if request.method == 'GET':
        email = request.query_params.get('email', None)  # GET isteği ile gelen email parametresini al
        if email:
            tasks = Task.objects.filter(email=email)  # Email'e göre filtrele
            if tasks.exists():
                serializer = TaskSerializer(tasks, many=True)  # tasks olarak düzeltildi
                return Response(serializer.data)
            else:
                return Response({"detail": "No tasks found for this email."}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"detail": "Email query parameter is required."}, status=status.HTTP_400_BAD_REQUEST)

    # POST request: Yeni bir görev oluştur (Email ile birlikte)
    elif request.method == 'POST':
        email = request.data.get('email', None)  # POST isteği ile gelen email parametresini al
        if email:
            serializer = TaskSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"detail": "Email field is required in POST request."}, status=status.HTTP_400_BAD_REQUEST)

    # DELETE request: ID'ye göre belirli bir görevi sil
    elif request.method == 'DELETE':
        print(f' body: {request.body}')  # Ham isteği görmek için
        task_id = request.query_params.get('id', None)  # Query parametresi ile ID al
        if task_id:
            try:
                task = Task.objects.get(id=task_id)  # Task modelinden id'ye göre görev bul
                task.delete()
                return Response({"detail": "Task deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
            except Task.DoesNotExist:  # Task modelinden Not modeline düzeltildi
                return Response({"detail": "Task not found."}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"detail": "ID is required in DELETE request."}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST', 'DELETE'])
def shortcut_list(request):
    # GET request: Email'e göre görevleri döndür
    if request.method == 'GET':
        email = request.query_params.get('email', None)  # GET isteği ile gelen email parametresini al
        if email:
            shortcuts = Shortcut.objects.filter(email=email)  # Email'e göre filtrele
            if shortcuts.exists():
                serializer = ShortcutSerializer(shortcuts, many=True)  # tasks olarak düzeltildi
                return Response(serializer.data)
            else:
                return Response({"detail": "No shortcuts found for this email."}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"detail": "Email query parameter is required."}, status=status.HTTP_400_BAD_REQUEST)

    # POST request: Yeni bir görev oluştur (Email ile birlikte)
    elif request.method == 'POST':
        email = request.data.get('email', None)  # POST isteği ile gelen email parametresini al
        if email:
            serializer = ShortcutSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"detail": "Email field is required in POST request."}, status=status.HTTP_400_BAD_REQUEST)

    # DELETE request: ID'ye göre belirli bir görevi sil
    elif request.method == 'DELETE':
        print(f' body: {request.body}')  # Ham isteği görmek için
        shortcut_id = request.query_params.get('id', None)  # Query parametresi ile ID al
        if shortcut_id:
            try:
                shortcut = Shortcut.objects.get(id=shortcut_id)  # Task modelinden id'ye göre görev bul
                shortcut.delete()
                return Response({"detail": "Shortcut deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
            except Shortcut.DoesNotExist:  # Task modelinden Not modeline düzeltildi
                return Response({"detail": "Shortcut not found."}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"detail": "ID is required in DELETE request."}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST', 'DELETE'])
def alarm_list(request):
    # GET request: Email'e göre alarmları döndür
    if request.method == 'GET':
        email = request.query_params.get('email', None)  # GET isteği ile gelen email parametresini al
        if email:
            alarms = Alarm.objects.filter(email=email)  # Email'e göre filtrele
            if alarms.exists():
                serializer = AlarmSerializer(alarms, many=True)  # Alarmları döndür
                return Response(serializer.data)
            else:
                return Response({"detail": "No alarms found for this email."}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"detail": "Email query parameter is required."}, status=status.HTTP_400_BAD_REQUEST)

    # POST request: Yeni bir alarm oluştur
    elif request.method == 'POST':
        serializer = AlarmSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # DELETE request: ID'ye göre belirli bir alarmı sil
    elif request.method == 'DELETE':
        print(f' body: {request.body}')  # Ham isteği görmek için
        alarm_id = request.query_params.get('id', None)  # Query parametresi ile ID al
        if alarm_id:
            try:
                alarm = Alarm.objects.get(id=alarm_id)  # ID'ye göre alarm bul
                alarm.delete()
                return Response({"detail": "Alarm deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
            except Alarm.DoesNotExist:
                return Response({"detail": "Alarm not found."}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"detail": "ID is required in DELETE request."}, status=status.HTTP_400_BAD_REQUEST)


