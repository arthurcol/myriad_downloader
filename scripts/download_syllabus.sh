export API_URL=https://api.github.com/repos/lewagon/data-meta/contents/syllabus.yml
curl $(gh api $API_URL --jq .download_url) > myriadloader/syllabus.yml
python myriadloader/yaml_parser.py
