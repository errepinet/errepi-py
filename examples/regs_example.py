"""
Examples of using the GenericRegsClient class to interact with the Errepi Net
generic registries microservice over gRPC (GenericRegsService).

Shows every RPC of the service, both without filter and with the optional
prefix search filter.
"""

from errepi.regs import GenericRegsClient
from errepi.regs.models import RegsClientConfiguration

# Instantiate with a connection configuration (host and port) or use the default
regs = GenericRegsClient(RegsClientConfiguration(host="localhost", port=50051))

# 1. Get application info
info = regs.app_info()
print("App info:", info)

# 2. List states (no filter)
states = regs.states_list()
print("States (no filter):", states)
print("States count:", len(states))

# 3. List states, optional prefix search on Italian name
states_filtered = regs.states_list("Ita")
print("States (search='Ita'):", states_filtered)
print("States filtered count:", len(states_filtered))

# 4. List cities (no filter)
cities = regs.cities_list()
print("Cities (no filter):", cities)
print("Cities count:", len(cities))

# 5. List cities, optional prefix search on municipality name
cities_filtered = regs.cities_list("Roma")
print("Cities (search='Roma'):", cities_filtered)
print("Cities filtered count:", len(cities_filtered))

# 6. List caps (no filter)
caps = regs.caps_list()
print("Caps (no filter):", caps)
print("Caps count:", len(caps))

# 7. List caps, optional prefix search on postal code
caps_filtered = regs.caps_list("001")
print("Caps (search='001'):", caps_filtered)
print("Caps filtered count:", len(caps_filtered))

# 8. List provinces (no filter)
provinces = regs.provinces_list()
print("Provinces (no filter):", provinces)
print("Provinces count:", len(provinces))

# 9. List provinces, optional prefix search on province name
provinces_filtered = regs.provinces_list("Roma")
print("Provinces (search='Roma'):", provinces_filtered)
print("Provinces filtered count:", len(provinces_filtered))

# 10. List regions (no filter)
regions = regs.regions_list()
print("Regions (no filter):", regions)
print("Regions count:", len(regions))

# 11. List regions, optional prefix search on region name
regions_filtered = regs.regions_list("Lazio")
print("Regions (search='Lazio'):", regions_filtered)
print("Regions filtered count:", len(regions_filtered))
