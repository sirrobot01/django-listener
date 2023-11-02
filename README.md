### Django Listener

Django Listener is a Django app that listens to and process webhooks from different providers.

### Installation

Install using pip

```bash
pip install django-listener
```

### Usage

Add `'listener'` to your `INSTALLED_APPS` in settings.py.

    INSTALLED_APPS = [
        ...
        'listener',
        ...
    ]

Run migrations, `python manage.py migrate listener`

Go to your admin page and add a new `Source` object.

- **Name**: Name of the source
- **Slug**: Slug of the source(automatically generated, but can be changed)
- **Url**: Url of the source
- **Username**: Username for basic authentication (if any)
- **Password**: Password for basic authentication (if any)
- **Token**: Token for authentication (if any)
- **Token Header**: Header to be used for token authentication (defaults to `HTTP_AUTHORIZATION`)
- **Active**: Whether the source is active or not
- **Unique ID Field**: The field to be used as the unique identifier for the object (defaults to `id`)
- **HTTP Method**: The HTTP method to be used for the webhook (defaults to `POST`)
- **Content Type**: The content type to be used for the webhook (defaults to `application/json`)


Set up your webhook in the source provider to point to the url `https://yourdomain.com/listener/webhooks/<source_slug>/` where `<source_slug>` is the slug of the source you created.

Example: `http://localhost:8080/listener/webhooks/github/`

### Customization (Optional)

You can customize your webhook processor by changing the LISTENER setting in your settings.py

    LISTENER = {
        "PROCESSOR": {
            "default": "listener.processor.DefaultProcessor",
            "github": "path.to.GithubProcessor",
            "shopify": "path.to.ShopifyProcessor",
        }   
        },
    }


Your processor should be a function that takes in the following parameters:

- **event**: The event object

Your processor class **must** have a `process` method. 

For example

    class GithubProcessor:
        def process(self, event):
            # Do something with the event
            pass


### Contributing

Please feel free to fork this package and contribute by submitting a pull request to enhance the functionalities.

### License

The MIT License (MIT). Please see [License File](LICENSE) for more information.

