from .confs import RegsClientConfiguration

from .models import (
    AppInfo,
    Cap,
    City,
    Province,
    Region,
    State,
)


import grpc
from typing import List, Optional

from google.protobuf.empty_pb2 import Empty
from google.protobuf.json_format import MessageToDict

from errepi.gen import generic_regs_pb2 as pb
from errepi.gen import generic_regs_pb2_grpc as pb_grpc


def _parse_message(model, message):
    return model.model_validate(
        MessageToDict(
            message,
            preserving_proto_field_name=True,
            always_print_fields_with_no_presence=True,
        )
    )


class GenericRegsClient:
    """
    Client for interacting with the Errepi Net generic registries microservice
    (GenericRegsService).

    This class provides methods to retrieve application info and search
    states, cities, caps, provinces and regions over gRPC.

    The interface mirrors the RPCs of protos/generic_regs.proto.
    """

    def __init__(self, config: Optional[RegsClientConfiguration] = None) -> None:
        """
        Initialize the GenericRegsClient.

        Args:
            config (Optional[RegsClientConfiguration]): Connection configuration
                (host and port). Defaults to 'localhost:50051'.
        """
        if config is None:
            config = RegsClientConfiguration()
        self.config = config
        self.target = f"{config.host}:{config.port}"
        self._channel = grpc.insecure_channel(self.target)
        self._stub = pb_grpc.GenericRegsServiceStub(self._channel)

    def app_info(self) -> AppInfo:
        """
        Retrieve application build and version information (GetAppInfo).

        Returns:
            AppInfo: Application information object.
        """
        response = self._stub.GetAppInfo(Empty())
        return _parse_message(AppInfo, response)

    def states_list(self, search: Optional[str] = None) -> List[State]:
        """
        List states, optional prefix search on Italian name (StatesList).

        Args:
            search (Optional[str]): Prefix to search on the Italian name.

        Returns:
            List[State]: List of state objects.
        """
        response = self._stub.StatesList(pb.StatesListRequest(search=search))
        return [_parse_message(State, state) for state in response.states]

    def cities_list(self, search: Optional[str] = None) -> List[City]:
        """
        List cities, optional prefix search on municipality name (CitiesList).

        Args:
            search (Optional[str]): Prefix to search on the municipality name.

        Returns:
            List[City]: List of city objects.
        """
        response = self._stub.CitiesList(pb.CitiesListRequest(search=search))
        return [_parse_message(City, city) for city in response.cities]

    def caps_list(self, search: Optional[str] = None) -> List[Cap]:
        """
        List caps, optional prefix search on postal code (CapsList).

        Args:
            search (Optional[str]): Prefix to search on the postal code.

        Returns:
            List[Cap]: List of cap objects.
        """
        response = self._stub.CapsList(pb.CapsListRequest(search=search))
        return [_parse_message(Cap, cap) for cap in response.caps]

    def provinces_list(self, search: Optional[str] = None) -> List[Province]:
        """
        List provinces, optional prefix search on province name (ProvincesList).

        Args:
            search (Optional[str]): Prefix to search on the province name.

        Returns:
            List[Province]: List of province objects.
        """
        response = self._stub.ProvincesList(pb.ProvincesListRequest(search=search))
        return [_parse_message(Province, province) for province in response.provinces]

    def regions_list(self, search: Optional[str] = None) -> List[Region]:
        """
        List regions, optional prefix search on region name (RegionsList).

        Args:
            search (Optional[str]): Prefix to search on the region name.

        Returns:
            List[Region]: List of region objects.
        """
        response = self._stub.RegionsList(pb.RegionsListRequest(search=search))
        return [_parse_message(Region, region) for region in response.regions]
