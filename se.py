import logging
from typing import Any
import asyncio
import json
import requests

_LOGGER = logging.getLogger(__name__)
_LOGGER.setLevel(logging.DEBUG)


class SolarEdge:
    _base_url = 'https://monitoringapi.solaredge.com'

    def __init__(
            self,
            api_key: str,
            site_id: int,
            timeout: int = 10,
    ) -> None:
        self.api_key = api_key
        self.session = requests.Session()
        self.timeout = timeout
        self.site_url = f'{SolarEdge._base_url}/site/{site_id}'

    async def get_current_power_flow(self) -> dict[str, Any]:
        return self.__get_json(f'{self.site_url}/currentPowerFlow')

    def close(self) -> None:
        self.session.close()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close()

    def __get_json(
            self, url: str,
            params: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        return self.session.get(
            url,
            params={'api_key': self.api_key, **(params or {})},
            timeout=self.timeout,
        ).json()


async def main(**kwargs) -> dict[str, Any]:
    with SolarEdge(**kwargs) as solar_edge:
        result = await solar_edge.get_current_power_flow()
    return result


if '__main__' == __name__:
    print(json.dumps(asyncio.run(main(
        api_key='ECJPGALR6K41RE2JC43TNA6J2ZNLCOJ2',
        site_id=771710,
        timeout=60
    ))))
