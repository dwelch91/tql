from io import StringIO

from tql.__main__ import build_args_parser
from tql.filter import print_filter_list_table
from tql.replace import print_replacements_table

with open('./README.md.tmpl', 'r') as f:
    readme = f.read()

buf = StringIO()
print_filter_list_table(fmt='md', stream=buf)
filter_table = buf.getvalue()
filter_table = filter_table.replace('<', r'\<').replace('>', r'\>')
buf.close()

buf = StringIO()
print_replacements_table(fmt='md', stream=buf)
replace_table = buf.getvalue()
buf.close()

parser = build_args_parser()
parser.prog = 'tql'
usage = parser.format_help()

readme = readme.format(filter_table=filter_table, replace_table=replace_table, usage=usage)

with open('./README.md', 'w') as f:
    f.write(readme)