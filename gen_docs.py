from io import StringIO
from textwrap import wrap

from tql.__main__ import build_args_parser
from tql.filter import print_filter_list_table
from tql.replace import print_replacements_table

with open('./README.md.tmpl', 'r') as f:
    readme = f.read()

buf = StringIO()
print_filter_list_table(fmt='md', stream=buf)
filter_table = buf.getvalue()
buf.close()

buf = StringIO()
print_replacements_table(fmt='md', stream=buf)
replace_table = buf.getvalue()
buf.close()

parser = build_args_parser()
parser.prog = 'tql'
usage_out = []
indent = 0
for line in parser.format_help().replace(',', ', ').splitlines():
    wrapped_lines = wrap(line, 80)
    if not wrapped_lines:
        continue
    if len(wrapped_lines) == 1:
        indent = len(line) - len(line.lstrip())
        usage_out.append(line)
        continue

    usage_out.append(wrapped_lines[0])
    for wrap_line in wrapped_lines[1:]:
        usage_out.append(' '*indent + wrap_line)

readme = readme.format(filter_table=filter_table, replace_table=replace_table, usage='\n'.join(usage_out))

with open('./README.md', 'w') as f:
    f.write(readme)