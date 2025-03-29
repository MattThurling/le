Django application with combination of web templates and Vue Components on the Front End.

To run front end assets for development

cd frontend

npm run dev

Notes:

- Was having a problem referencing front end assets so disabled cache busting hashes in Vite.
- Django templates are in the frontend folder so that style changes are picked up by Vite.