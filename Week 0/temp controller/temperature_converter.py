class TemperatureConverter:
    __temperature: float

    def __init__(self):
        self.__temperature = 0.0

    def setTemperature(self, temp: float) -> None:
        self.__temperature = temp
        return None
    
    def toCelsius(self) -> float:
        Celcius = self.__temperature
        return print(f"Temperature in Celsius: {Celcius}")
    
    def toFahrenheit(self) -> float:
        Fahrenheit = self.__temperature * 1.8 + 32
        return print(f"Temperature in Fahrenheit: {Fahrenheit}")
    
    def toKelvin(self) -> float:
        Kelvin = self.__temperature + 273.15
        return print(f"Temperature in Kelvin: {Kelvin}")