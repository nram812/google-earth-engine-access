import json
class GetBandsMetaData:

    def __init__(self, sat_name):
        if 'sentinel' in sat_name:
            metadata_file = "satellite_data/satellite_metadata/Sentinel2_metadata.json"

        elif 'landsat7' in sat_name:
            metadata_file = "satellite_data/satellite_metadata/LandSat7_metadata.json"

        elif 'landsat8' in sat_name:
            metadata_file = "satellite_data/satellite_metadata/LandSat8_metadata.json"
        try:
            with open(metadata_file) as f:
                self.band_metadata = json.load(f)
                self.bands_list = [key for key in self.band_metadata.keys()]

        except NameError:
            self.band_metadata = {sat_name}
