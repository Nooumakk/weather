import asyncio
from aiohttp import ClientSession
from root.settings import APPID_KEY
from .models import City
from .forms import CityForm
from django.urls import reverse
from django.views.generic import FormView


class WeatherView(FormView):
    form_class = CityForm
    template_name = "index.html"


    async def get_data(self, url, session):
        req = await (await session.get(url)).json()
        self.citys.append(
            {
            "city": req["name"],
            "description": req["weather"][0]["description"].capitalize(),
            "icon": req["weather"][0]["icon"],
            "temp": round(req["main"]["temp"])
            }
        )

    async def query(self, url):
        async with ClientSession() as sess:
            return await self.get_data(url, sess)

    async def gather(self, urls):
        self.citys = []
        await asyncio.gather(*[self.query(url) for url in urls])

    def get_context_data(self, **kwargs):
        context = super(WeatherView, self).get_context_data(**kwargs)
        city_list = City.objects.all()
        appid = APPID_KEY
        all_citys = []
        for city in city_list:
            all_citys.append(
                f"https://api.openweathermap.org/data/2.5/weather?q={city},&lang=ru&appid={appid}&units=metric"
            )
        asyncio.run(self.gather(all_citys))
        context["all_city"] = self.citys
        return context
    
    def get_success_url(self):
         return self.request.GET.get("next", reverse("weather_page"))