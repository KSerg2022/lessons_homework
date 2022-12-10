import pytest

from weather.getting_weather import *


class TestGettingWeather:

    def setup_method(self):
        self.city = 'Mariupol'
        self.api_id = '402d150cc39854f9d464c714a56dcf36'
        self.url = f'http://api.openweathermap.org/data/2.5/weather?q={self.city}&appid={self.api_id}&units=metric'
        self.response = get_weather(self.city, self.api_id)

    def test_get_weather_200(self):
        response = requests.get(self.url)
        assert response.status_code == 200

    def test_get_weather_error(self):
        city = "Kyev"
        with pytest.raises(RuntimeError, match='openweathermap.org returned non-200 code'):
            get_weather(city, self.api_id)

    def test_get_weather_error1(self):
        city = "Kyev"
        with pytest.raises(RuntimeError) as context_error:
            get_weather(city, self.api_id)
        assert 'openweathermap.org returned non-200 code' in str(context_error.value)

    @pytest.mark.parametrize('value', [{'main': {'temp': 30}}, {'main': {'temp': 15}},
                                       {'main': {'temp': 0}}, {'main': {'temp': -15}}])
    def test_determine_temperature(self, value):
        result = determine_temperature(value)
        assert result in ( 'hot', 'warm', 'cool', 'cold')

    def test_main(self):
        result = main(self.city, self.api_id)
        assert result in ('warm', 'cool', 'cold', 'strong cold')


if __name__ == '__main__':
    pytest.main()
