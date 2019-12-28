# Lusha API Wrapper for Python

B2B contact information at your fingertips.

## Requirements
* [Python](https://www.python.org/) >= 2.6
* Business email to register an account with Lusha
* Api key from [Lusha](https://dashboard.lusha.co/signup)
 
## Getting Started

1) Get some coffee.
2) Go to https://dashboard.lusha.co/signup and register an account to get your api key
3) Clone the repo and install requirements.
    ```commandline
    git clone https://github.com/GrilledChickenThighs/lusha_api_wrapper.git
    cd lusha_api_wrapper
    pip install -r requirements.txt
    ```
4) Open up the lusha_api_wrapper.py file add your api key and play with the examples at the bottom
    ```python
    LUSHA_API_KEY = "your-api-key"
    lush = LushaAPI(LUSHA_API_KEY)
   
    response_person = lush.person(first_name='Elon', last_name='Musk', company='Tesla')
    response_person_phone = lush.person(first_name='Elon', last_name='Musk', company='Tesla', property='phoneNumbers')
    response_person_email = lush.person(first_name='Elon', last_name='Musk', company='Tesla', property='emailAddresses')
    response_company_domain = lush.company(domain="www.facebook.com")
    response_company_name = lush.company(company="facebook")
    number_of_calls_remaining = response_person['meta'].get('matches_this_month')   
    ```

## API

[docs](https://www.lusha.co/docs/)

