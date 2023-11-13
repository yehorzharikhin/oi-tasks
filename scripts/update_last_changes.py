import sys

from .update_oi_statement import update_statement

sources = {}

needed_prefix = "statements/"
for file in sys.argv:
    if file[:len(needed_prefix)] == needed_prefix:
        data = file.split("/")
        olymp = data[1]
        year = data[2]
        print(olymp, year)
        sources[olymp + ' ' + year] = True

for source in sources:
    print('Updating', source)
    olymp, year = source.split(' ')
    print(olymp, year)
    update_statement(olymp, year)