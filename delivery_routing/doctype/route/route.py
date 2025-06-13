import frappe
import json

@frappe.whitelist()
def get_location_coordinates(sender, receiver):
    sender_doc = frappe.get_doc("Route Location", sender)
    receiver_doc = frappe.get_doc("Route Location", receiver)

    def parse_coords(geo_str):
        try:
            # Parse GeoJSON from Geolocation field
            geojson = json.loads(geo_str)
            coords = geojson['features'][0]['geometry']['coordinates']
            return float(coords[1]), float(coords[0])  # return lat, lng
        except Exception:
            return None, None

    sender_lat, sender_lng = parse_coords(sender_doc.location)
    receiver_lat, receiver_lng = parse_coords(receiver_doc.location)

    return {
        "sender_lat": sender_lat,
        "sender_lng": sender_lng,
        "receiver_lat": receiver_lat,
        "receiver_lng": receiver_lng
    }
@frappe.whitelist()
def calculate_carbon_emission(distance, fuel_type, mileage):
    try:
        distance = float(distance)
        mileage = float(mileage)
        if mileage == 0:
            return {"carbon_kg": 0.0}

        # Approx. CO₂ emission factors in kg per litre of fuel
        emission_factors = {
            "Petrol": 2.33,
            "Diesel": 2.68,
            "CNG": 2.05,
            "Electric": 0.0  # Assume renewable; else multiply grid factor
        }

        fuel_used = distance / mileage  # Litres
        carbon_kg = fuel_used * emission_factors.get(fuel_type, 0)

        return {"carbon_kg": round(carbon_kg, 3)}
    except Exception as e:
        frappe.log_error(f"Carbon Calc Error: {e}")
        return {"carbon_kg": 0.0}


