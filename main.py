from search import multi_search
from ui import get_window

def take_inputs():
    mode = int(input('Enter search mode: '))
    search_term = ""
    if mode != 0:
        search_term = input('Enter search query: ')
    since_when = ""
    if mode == 0 or mode == 1 or mode == 3:
        since_when = input("Enter search query year in 'yyyy' format press enter if not needed: ")
    return mode, search_term, since_when


def transform_results(results):
    total_matches = results['total']['value']
    documents = [i['_source'] for i in results['hits']]

    table_rows = []
    for doc in documents:
        row = [
            doc['poem_name'],
            doc['type'],
            doc['author'],
            doc['year'],
            doc['lime'],
            doc['metaphor_available'],
            doc['count'],
            doc['source'],
            doc['target'],
            doc['meaning'],
        ]
        table_rows.append(tuple(row))

    return total_matches, table_rows


def main():
    modes_text = open('search_options.txt', 'r').read()
    while True:
        print(modes_text)
        mode, search_term, year = take_inputs()
        if mode < 0:
            break

        results = multi_search(search_term, year, mode)

        total_matches, table_rows = transform_results(results)
        print('Total Matches -', total_matches)
        results_table = get_window(table_rows)
        results_table.mainloop()


main()
