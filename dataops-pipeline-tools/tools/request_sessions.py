import sys
import logging

from requests import Session, Response
from requests.adapters import HTTPAdapter
from requests.exceptions import HTTPError
from requests.packages.urllib3.util.retry import Retry


def perform_get(session: Session, url: str, params: str = None) -> Response:
    """Performs HTTPS GET request using python Requests.

    Args:
        session: python Requests session
        url: the FQDN to perform the GET request against
    Returns:
        The requests Response object
    """
    retries = Retry(total=20, backoff_factor=.1,
                    status_forcelist=[429, 503, 503, 504])
    session.mount('https://', HTTPAdapter(max_retries=retries))
    try:
        if params:
            response = session.get(url, params=params)
        else:
            response = session.get(url)
        response.raise_for_status()
    except HTTPError as err:
        logging.error(err)
        sys.exit(1)

    return response.json()