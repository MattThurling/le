Django application with combination of web templates and Vue Components on the Front End.

To deploy, first build frontend assets

cd frontend

npm run build

Notes:

- At the moment, styles used in Django templates need to be referenced in StylerForDjango component, until I find a way to get Vite (and Rollup) to watch for them.

- Was having a problem referencing front end assets so disable cache busting hashes in Vite.  