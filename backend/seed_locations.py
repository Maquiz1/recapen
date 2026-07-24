from locations.models import Country, Zone, Region, District, Ward
from sites.models import Site

def run():
    print("Seeding locations and sites...")

    # Tanzania
    country, _ = Country.objects.get_or_create(name='Tanzania')

    # Central Zone -> Dodoma -> Kondoa -> Kondoa Ward -> Kondoa Hospital
    central_zone, _ = Zone.objects.get_or_create(name='Central', country=country)
    dodoma, _ = Region.objects.get_or_create(name='Dodoma', zone=central_zone)
    kondoa_dist, _ = District.objects.get_or_create(name='Kondoa', region=dodoma)
    kondoa_ward, _ = Ward.objects.get_or_create(name='Kondoa', district=kondoa_dist)

    kondoa_hospital, _ = Site.objects.get_or_create(
        name='Kondoa Hospital',
        defaults={
            'country': country,
            'zone': central_zone,
            'region': dodoma,
            'district': kondoa_dist,
            'ward': kondoa_ward
        }
    )

    # Northern Zone -> Arusha -> Karatu -> Karatu Ward -> Karatu Hospital
    northern_zone, _ = Zone.objects.get_or_create(name='Northern', country=country)
    arusha, _ = Region.objects.get_or_create(name='Arusha', zone=northern_zone)
    karatu_dist, _ = District.objects.get_or_create(name='Karatu', region=arusha)
    karatu_ward, _ = Ward.objects.get_or_create(name='Karatu', district=karatu_dist)

    karatu_hospital, _ = Site.objects.get_or_create(
        name='Karatu Hospital',
        defaults={
            'country': country,
            'zone': northern_zone,
            'region': arusha,
            'district': karatu_dist,
            'ward': karatu_ward
        }
    )

    print("Seed complete.")
    print(f"Sites: {kondoa_hospital}, {karatu_hospital}")

if __name__ == '__main__':
    run()
