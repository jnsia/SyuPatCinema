from models import *
from rest_framework.response import Response

def theaterDataSetting(request):
    import csv

    with open('./Theaters.csv', newline='', encoding='utf-8') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        regions = ['서울', '경기/인천', '충청/대전', '전라/광주', '경북/대구', '경남/부산/울산', '강원', '제주']

        for region_name in regions:
            region = Regions()
            region.name = region_name
            region.save()

        for row in spamreader:
            row_data = row[0].split(',')

            if row_data[4] == '롯데시네마':
                region, location = row_data[10], row_data[5]
                
                theater = Theater()
                theater.name = row_data[5]

                if region in ['서울특별시']:
                    region = Regions.objects.get(pk=1)
                    theater.regions = region
                    # print(regions[0], location)
                elif region in ['경기도', '인천광역시']:
                    region = Regions.objects.get(pk=2)
                    theater.regions = region
                    # print(regions[1], location)
                elif region in ['충청북도', '충청남도', '대전광역시']:
                    region = Regions.objects.get(pk=3)
                    theater.regions = region
                    # print(regions[2], location)
                elif region in ['전라북도', '전라남도', '광주광역시']:
                    region = Regions.objects.get(pk=4)
                    theater.regions = region
                    # print(regions[3], location)
                elif region in ['경상북도', '대구광역시']:
                    region = Regions.objects.get(pk=5)
                    theater.regions = region
                    # print(regions[4], location)
                elif region in ['경상남도', '부산광역시', '울산광역시']:
                    region = Regions.objects.get(pk=6)
                    theater.regions = region
                    # print(regions[5], location)
                elif region in ['강원도']:
                    region = Regions.objects.get(pk=7)
                    theater.regions = region
                    # print(regions[6], location)
                elif region in ['제주특별자치도']:
                    region = Regions.objects.get(pk=8)
                    theater.regions = region
                    # print(regions[7], location)

                theater.save()

                movies = Movie.objects.all()

                for movie in movies:
                    theater.movies.add(movie)


def datatimeDataSetting(request):
    dates = ['11/24', '11/25', '11/26', '11/27', '11/28']
    times = ["9:30", "12:00", "14:30", "17:00", "20:30", "23:00"]
    
    movies = Movie.objects.all()
    theaters = Theater.objects.all()
    
    playDates = PlayDate.objects.all()
    
    for playDate in playDates:
        playDate.delete()

    cnt = 0
    
    for date_data in dates:
        for time_data in times:
            for movie in movies:
                for theater in theaters:
                    playDate = PlayDate()
                    cnt += 1
                    
                    playDate.date = date_data
                    playDate.time = time_data
                    playDate.movie = movie
                    playDate.theater = theater

                    playDate.save()
    
    return Response({'msg' : cnt})