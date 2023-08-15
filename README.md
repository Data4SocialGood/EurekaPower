# EurekaPower
## Deep Learning-based residential energy consumption prediction 

EurekaPower is a novel web application that enables residential electrical
consumption management and smart monitoting. Fueled by the recent
advancements in Artificial Intelligence & Machine Learning, the application
harnesses historical user data to provide insightful data analytics, future predictions
and personalized suggestions in terms of energy saving. EurekaPower is deployed
as an end-to-end solution tailored to the energy sector. As such, it can be utilized
both by individual users to achieve home energy efficiency and by energy providers
to further optimize the grid network, enhance their pricing strategies and develop
user-centric marketing policies.
Main features:
* Data analytics and visualization: a rich set of interactive graphical tools that
allow the user to monitor home energy consumption, perform spatio-temporal
comparisons and unveil consumption patterns that facilitate mitigation of
energy waste.
* Energy consumption prediction: a well-informed forecast on the user's future
consumption (12-month horizon), via a state-of-the-art prediction model that is
based on each individual user's historical data, geolocation and residential
characteristics.
* Discount Gamification: a simulation playground that allows the user to
experiment with various consumption scenarios and obtain potential discount
offers by the energy provider, based on the achieved energy-efficiency.
* API exposure: all major services are available via web-APIs to third-parties, to
support automatic statistic collection and enable data leveraging by centralized
entities.
* Data Protection: a solid, battle-tested access management framework based on
a commercial toolchain, to solidify privacy and security for sensitive user data.


## Installation
### Prerequisites
Before we start please install [Docker](https://docs.docker.com/engine/install/) and [Python](https://www.python.org/) (Recommended version 3.9.17)

Clone the project and unzip it: \
``` git clone https://github.com/Data4SocialGood/EurekaPower.git ``` \
``` unzip EurekaPower-main.zip ``` \
We have to deploy the backend, frontend and the Authorization server (Keycloak) 

### Keycloak
Change directory: ``` cd EurekaPower/keycloak/ ``` \
Deploy: ``` docker run  -p 8080:8080 -e KEYCLOAK_ADMIN=admin -e KEYCLOAK_ADMIN_PASSWORD=admin \``` \
```-v ./realm/:/opt/keycloak/data/import quay.io/keycloak/keycloak:latest  start-dev --import-realm ```

### Backend
Change directory: ``` cd EurekaPower/backend/ ``` \
Install requirements: ``` pip install -r requirements.txt ```  
Initialize the database: ``` flask --app app/ init-db ``` \
Deploy: ``` flask --app app/ run --port 5000 ```
### Frontend
Change directory: ``` cd EurekaPower/frontend/ ``` \
Install requirements: ``` pip install -r requirements.txt ```  
Deploy: ``` flask --app eurekapower_plotly_code run --port 5001 ```

[EurekaPower](http://127.0.0.1:5001/home) is ready!

You can navigate in our demo as: \
Username: giorgos123 \
password: 123 

## Contact
Georgios Drainakis: [gdrainakis@mail.ntua.gr](mailto:gdrainakis@mail.ntua.gr)
## License
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
