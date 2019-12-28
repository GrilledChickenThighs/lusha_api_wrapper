"""
Lusha api wrapper to query a dataset of business profiles and companies
and receive and get an enriched profile of the item you were looking for
"""
import requests
import logging

logger = logging.getLogger(__name__)


class LushaAPI:
    """https://www.lusha.co/docs/"""
    _apis = frozenset(("person", "company"))

    EMPTY_PERSON = {
        "data": {
            "firstName": "",
            "lastName": "",
            "fullName": "",
            "emailAddresses": [{"email": ""}],
            "phoneNumbers": [
                {
                    "countryCallingCode": "",
                    "countryCode": "",
                    "countryName": "",
                    "internationalNumber": "+# ###-###-####",
                    "localizedNumber": "(###) ###-####",
                }
            ],
            "company": {"domain": "", "name": ""},
        },
        "meta": {"matches_this_month": 0},
    }
    EMPTY_COMPANY = {
        "data": {
            "address": "",
            "categories": [""],
            "description": "",
            "domain": "",
            "employees": "",
            "founded": "",
            "founders": [""],
            "logo": "",
            "name": "",
            "social": {
                "facebook": {"url": ""},
                "linkedin": {"url": ""},
                "twitter": {"url": ""},
            },
            "website": "",
        },
        "meta": {"matches_this_month": 0},
    }

    def __init__(self, api_key: str):
        self.base_url = "https://api.lusha.co"
        self._token = api_key

    def api(self, name, **kwargs):
        """Generic API method."""
        if name not in self._apis:
            raise ValueError(
                "API name must be one of {0}, not {1!r}.".format(
                    tuple(self._apis), name
                )
            )

        headers = {"api_key": self._token}
        params = kwargs
        url = self.endpoint(name)

        return self._get(url, params=params, headers=headers)

    def endpoint(self, name):
        """Generate the URL endpoint for the given API."""
        return f"{self.base_url}/{name}"

    @staticmethod
    def _get(url, params=None, headers=None):
        """HTTP GET request."""
        try:
            response = requests.get(url, params=params, headers=headers)
            response.raise_for_status()
            # If JSON fails, return raw data
            try:
                return response.json()
            except ValueError:
                return response.text
        except NameError:
            return url, params

    def company(self, company: str = None, domain: str = None, **kwargs):
        """The company API provides information about any organization you look for to help you get a complete picture,
         such as overview, social network presence and location.
         https://www.lusha.co/docs/#block-6
         """
        if company and domain:
            raise NotImplementedError(
                "API can only handle company OR domain; not both!"
            )
        elif not (company or domain):
            raise TypeError(
                "CompanyAPI found No variables were passed. Need company OR domain, not None!"
            )

        if company:
            kwargs.update({"company": company})
        elif domain:
            kwargs.update({"domain": domain})

        response = self.api("company", **kwargs)
        if "errors" in response:
            logger.error(response['errors'].get("message"))
            return self.EMPTY_COMPANY
        else:
            return response

    def person(self, first_name, last_name, company, prop=None, **kwargs):
        """Person API.
        https://www.lusha.co/docs/#block-4
        """
        kwargs.update(
            {"firstName": first_name, "lastName": last_name, "company": company}
        )
        if prop and prop in ("phoneNumbers", "emailAddresses"):
            kwargs.update({"property": prop})
        elif prop:
            raise TypeError(
                f"property: {prop} does not match api format. Please check https://www.lusha.co/docs/#block-4"
            )

        response = self.api("person", **kwargs)

        if "errors" in response:
            logger.error(response['errors'].get("message"))
            return self.EMPTY_PERSON
        else:
            return response


if __name__ == "__main__":
    LUSHA_API_KEY = "your-api-key"
    lush = LushaAPI(LUSHA_API_KEY)
    response_person = lush.person(first_name='Elon', last_name='Musk', company='Tesla')
    response_person_phone = lush.person(first_name='Elon', last_name='Musk', company='Tesla', property='phoneNumbers')
    response_person_email = lush.person(first_name='Elon', last_name='Musk', company='Tesla', property='emailAddresses')
    response_company_domain = lush.company(domain="www.facebook.com")
    response_company_name = lush.company(company="facebook")
    number_of_calls_remaining = response_person['meta'].get('matches_this_month')
