export API_URL=https://api.github.com/repos/lewagon/data-meta/contents/syllabus.yml
curl $(gh api $API_URL --jq .download_url) > $PARSER_PATH/syllabus.yml
python $PARSER_PATH/yaml_parser.py
