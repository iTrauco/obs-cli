
# commands/camera_controls/utils/conversion.py
class AngleConverter:
   """Convert between raw values and degrees"""
   
   def to_degrees(self, raw_value, control_type):
       """Convert raw values to degrees"""
       if control_type == "pan":
           return round((raw_value / 468000) * 180, 1)
       elif control_type == "tilt":
           return round((raw_value / 324000) * 180, 1)
       return raw_value

   def from_degrees(self, degrees, control_type):
       """Convert degrees to raw values"""
       if control_type == "pan":
           return int((degrees / 180) * 468000)
       elif control_type == "tilt":
           return int((degrees / 180) * 324000)
       return degrees