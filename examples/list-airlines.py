from duffel_api import Duffel


if __name__ == "__main__":
    print("Duffel Flights API - List airlines example")
    client = Duffel()
    for airline in client.airlines.list():
        print(airline.name)
