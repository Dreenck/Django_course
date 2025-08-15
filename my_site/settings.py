import os
from pathlib import Path
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

# Use os.environ.get for all sensitive/configurable variables
SECRET_KEY = os.environ.get("SECRET_KEY")
DEBUG = os.environ.get("DEBUG", "False").lower() == "true" # Use .lower() for safer boolean conversion

# Allowed hosts should be dynamic for Render
ALLOWED_HOSTS = []
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)
else:
    ALLOWED_HOSTS.append("localhost") # For local development

INSTALLED_APPS = [
    'blog',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles', # Keep this as it's needed for collectstatic
    'cloudinary',
    'cloudinary_storage',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # Removed whitenoise.middleware.WhiteNoiseMiddleware - Cloudinary will serve static files
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'my_site.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug', # Useful for debugging
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'my_site.wsgi.application'

DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get("DATABASE_URL"),
        conn_max_age=600 # Optional: connection pooling for Render's PostgreSQL
    )
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# --- Cloudinary Configuration ---
# The CLOUDINARY_URL should already be set in your Render environment variables.
# If you are using a different method to provide credentials, adjust accordingly.
# CLOUDINARY_URL = os.environ.get("CLOUDINARY_URL") # This line is fine if env var is set

# This tells Django to use Cloudinary for storing media files (e.g., uploaded images)
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# This is the CRUCIAL part for serving static files (CSS, JS, images in static/) via Cloudinary
# If you don't want to serve static files from Cloudinary, you would keep whitenoise.
# For a more robust setup, serving static files from Cloudinary is recommended.
STATICFILES_STORAGE = 'cloudinary_storage.storage.StaticHashedCloudinaryStorage'

# When using STATICFILES_STORAGE with Cloudinary, STATIC_ROOT is still needed for collectstatic
# to gather all static files into one place before uploading them to Cloudinary.
# Cloudinary_storage will handle the upload and CDN mapping.
STATIC_ROOT = BASE_DIR / "staticfiles"
STATIC_URL = '/static/' # This will be overridden by Cloudinary's CDN URL for your static files.
                         # The actual URL served will be from Cloudinary.

# For Cloudinary, you might want to explicitly set the CDN URL if it's different from your Cloudinary URL.
# Often, django-cloudinary-storage handles this automatically, but you can be explicit:
# CLOUDINARY_STATIC_URL = CLOUDINARY_URL

# Optional: Configure Cloudinary's upload settings if needed
# CLOUDINARY_CONFIG = {
#     'cloud_name': 'YOUR_CLOUD_NAME',
#     'api_key': 'YOUR_API_KEY',
#     'api_secret': 'YOUR_API_SECRET',
#     'secure': True, # Use HTTPS
# }


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Make sure your image field uses the correct storage:
# In your models.py:
# image = models.ImageField(upload_to="images", null=True, storage=default_storage)
# Note: With DEFAULT_FILE_STORAGE set, Django automatically uses it for ImageField
# unless you explicitly specify a different storage. So, this might not be strictly necessary
# if you're not using multiple storage backends.