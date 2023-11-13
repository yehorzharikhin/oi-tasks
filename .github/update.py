import sys

sources = {}

print(sys.argv)


needed_prefix = "statements/"
for file in sys.argv:
    if file[:len(needed_prefix)] == needed_prefix:
        data = file.split("/")
        olymp = data[1].capitalize()
        year = data[2]
        print(olymp, year)
        sources[olymp + ' ' + year] = True

print(sources)