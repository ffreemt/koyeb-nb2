
echo to test: curl "127.0.0.1:8680/nb2chan/?qq=41947782&msg=hello" -H "token: DEMO_TOKEN"
echo run poetry export --without-hashes -o requirements.txt before deploying to koyeb

poetry run python start_nb2.py