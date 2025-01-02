import xml.etree.ElementTree as ET
import json

def kml_to_json(kml_file, output_file, default_color="red"):
    try:
        # Parse the KML file
        tree = ET.parse(kml_file)
        root = tree.getroot()

        # Define the namespaces for KML
        namespaces = {
            'kml': 'http://www.opengis.net/kml/2.2'
        }

        # Find all placemarks in the KML
        placemarks = root.findall('.//kml:Placemark', namespaces)

        features = []

        for placemark in placemarks:
            name = placemark.find('kml:name', namespaces)
            point = placemark.find('.//kml:Point/kml:coordinates', namespaces)
            timestamp = placemark.find('.//kml:TimeStamp/kml:when', namespaces)

            if point is not None:
                coords = point.text.strip().split(',')
                longitude = float(coords[0])
                latitude = float(coords[1])

                date = timestamp.text if timestamp is not None else "unknown"

                # Build the JSON feature
                feature = {
                    "type": "Feature",
                    "properties": {
                        "date": date,
                        "color": default_color
                    },
                    "geometry": {
                        "type": "Point",
                        "coordinates": [longitude, latitude]
                    }
                }
                features.append(feature)

        # Write features to JSON file
        with open(output_file, 'w') as json_file:
            json.dump(features, json_file, indent=4)

        print(f"Successfully converted KML to JSON. Output saved to {output_file}.")

    except Exception as e:
        print(f"An error occurred: {e}")

# Usage example
kml_to_json("2025.kml", "/out/2025.json")
