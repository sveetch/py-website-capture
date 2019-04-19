DUMPS_PATH = "/home/thenonda/Essais/shooting_pages/outputs/"

URLS = {
    "djangodoc": "http://192.168.0.103/doc/django-docs/",
    "splinter": "https://splinter.readthedocs.io/en/latest/screenshot.html",
    #"emencia": "https://www.emencia.com/fr/",
    "richie-education": "https://richie.education/en/",
}

SIZES = [
    (330, 768),
    (1440, 768),
]

PAGES = [
    {
        "name": "perdu.com",
        "url": "http://perdu.com/",
    },
    {
        "name": "djangodoc",
        #"url": "http://192.168.0.103/doc/django-docs/",
        "url": "http://192.168.0.103/doc/zouip/",
        "sizes": SIZES,
    },
    {
        "name": "splinter",
        "url": "https://splinter.readthedocs.io/en/latest/screenshot.html",
        "sizes": [
            (1920, 800),
        ],
    },
    {
        "name": "emencia",
        "url": "https://www.emencia.com/fr/",
        "sizes": [
            (1440, 768),
        ],
    },
    {
        "name": "richie-education",
        "url": "https://richie.education/en/",
        "sizes": SIZES,
    },
]
