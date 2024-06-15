python manage.py distill-local --force --settings=wiki.settings_static
python manage.py collectstatic --settings=wiki.settings_static
mv ./docs/igem-2024-website/note ./docs
mv ./docs/igem-2024-website/notebook ./docs
rm ./docs/igem-2024-website