from django.core.exceptions import ValidationError
from django.http import HttpResponseNotFound
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from queuedapi.models import HistoricalWait

import schedule
import time
import requests
import threading


class WaitSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = HistoricalWait
        fields = ("ride", "created_on", "wait")


class HistoricalWaits(ViewSet):
    def create(self, request):
        historical_wait = HistoricalWait()
        historical_wait.ride = request.data["ride"]
        
        historical_wait.wait = request.data["wait"]
        try:
            historical_wait.save()
            serializer = WaitSerializer(historical_wait, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)  


    def list(self, request):
        historical_waits = HistoricalWait.objects.all()

        ride = self.request.query_params.get('ride', None)
        by_date = self.request.query_params.get('date', None)

        if ride is not None:
            historical_waits = historical_waits.filter(ride=ride)
        
        if by_date is not None:
            historical_waits = historical_waits.filter(created_on__contains=by_date)

        serializer = WaitSerializer(historical_waits, many=True,
        context={'request': request})
        return Response(serializer.data)

    
    # def get_historical_waits():
    ##just testing
    #     url = 'https://api.themeparks.wiki/preview/parks/WaltDisneyWorldMagicKingdom/waittime'
    #     res = requests.get(url)
    #     waits = res.json()
    #     wait_times = []
    #     for ride in waits:
    #         each_ride = {'ride' : ride['id'], 'wait': ride['waitTime'] }
    #         wait_times.append(each_ride)
    #     print(wait_times)

    
    
    # schedule.every(1).minutes.do(get_mk_waits)
    ##works on local, breaks digital ocean server
    #     while True:
    #         schedule.run_pending()
    #         time.sleep(1)
def get_mk_waits():
    url = 'https://api.themeparks.wiki/preview/parks/WaltDisneyWorldMagicKingdom/waittime'
    res = requests.get(url)
    waits = res.json()
    for testing in waits:
        each_ride = HistoricalWait()
        each_ride.ride = testing['id']
        each_ride.wait = testing['waitTime']
        each_ride.save()

def get_ak_waits():
    url = 'https://api.themeparks.wiki/preview/parks/WaltDisneyWorldAnimalKingdom/waittime'
    res = requests.get(url)
    waits = res.json()
    for testing in waits:
        each_ride = HistoricalWait()
        each_ride.ride = testing['id']
        each_ride.wait = testing['waitTime']
        each_ride.save()

def get_epcot_waits():
    url = 'https://api.themeparks.wiki/preview/parks/WaltDisneyWorldEpcot/waittime'
    res = requests.get(url)
    waits = res.json()
    for testing in waits:
        each_ride = HistoricalWait()
        each_ride.ride = testing['id']
        each_ride.wait = testing['waitTime']
        each_ride.save()

def get_hs_waits():
    url = 'https://api.themeparks.wiki/preview/parks/WaltDisneyWorldHollywoodStudios/waittime'
    res = requests.get(url)
    waits = res.json()
    for testing in waits:
        each_ride = HistoricalWait()
        each_ride.ride = testing['id']
        each_ride.wait = testing['waitTime']
        each_ride.save()

        
class ContinuousScheduler(schedule.Scheduler):
    def run_continuously(self, interval=1):
        cease_continuous_run = threading.Event()
        class ScheduleThread(threading.Thread):
            @classmethod
            def run(cls):
                while not cease_continuous_run.is_set() and self.jobs:
                    self.run_pending()
                    time.sleep(interval)
        
        continuous_thread = ScheduleThread()
        continuous_thread.start()
        return cease_continuous_run



mk_wait = ContinuousScheduler()
ak_wait = ContinuousScheduler()
ep_wait = ContinuousScheduler()
hs_wait = ContinuousScheduler()

mk_wait.every(30).minutes.do(get_mk_waits)
ak_wait.every(30).minutes.do(get_ak_waits)
ep_wait.every(30).minutes.do(get_epcot_waits)
hs_wait.every(30).minutes.do(get_hs_waits)



getting_mk_waits = mk_wait.run_continuously()
getting_ak_waits = ak_wait.run_continuously()
getting_ep_waits = ep_wait.run_continuously()
getting_hs_waits = hs_wait.run_continuously()


    




    


    
    
       

    
    
    
    