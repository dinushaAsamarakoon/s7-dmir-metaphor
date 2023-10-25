from dataset import search, tokenize_text, stem_sinhala_text
from datetime import datetime


def is_valid_year(year):
    try:
        datetime.strptime(year, '%Y')
        return True
    except ValueError:
        return False


def get_all(year):
    if is_valid_year(year):
        query = {
            "range": {
                "year": {
                    "gte": year
                }
            }
        }
    else:
        query = {
            'match_all': {}
        }
    return search(query)


def search_by_poem_name_and_year(search_term, year):
    if is_valid_year(year):
        query = {
            'bool': {
                'must': [
                    {'match': {'poem_name': search_term}},
                    {
                        'range': {
                            'year': {
                                'gte': year
                            }
                        }
                    }
                ]
            }
        }
    else:
        query = {'match': {'poem_name': search_term}},

    return search(query)


def search_by_metaphor_type(search_term):
    query = {
        'term': {
            'type': search_term
        }
    }
    return search(query)


def search_by_author_and_year(search_term, year):
    if is_valid_year(year):
        query = {
            'bool': {
                'must': [
                    {'match': {'author': search_term}},
                    {
                        'range': {
                            'year': {
                                'gte': year
                            }
                        }
                    }
                ]
            }
        }
    else:
        query = {
            'match': {
                'author': search_term
            }
        }
    return search(query)


def search_by_published_year(search_term):
    query = {
        'match': {
            'year': search_term
        }
    }
    return search(query)


def search_metaphors(search_term):
    query = {
        'match': {
            'lime': search_term
        }
    }
    return search(query)


def search_metaphors_with_stemming(search_term):
    stemmed_search_term = stem_sinhala_text(tokenize_text(search_term)[1])
    query = {
        'bool': {
            'should': [
                {'match': {'lime': search_term}},
                {'match': {'stemmed_lime': stemmed_search_term}}
            ],
            'minimum_should_match': 1
        }
    }
    return search(query)


def search_by_source(search_term):
    query = {
        'match': {
            'source': search_term
        }
    }
    return search(query)


def search_by_target(search_term):
    query = {
        'match': {
            'target': search_term
        }
    }
    return search(query)


def search_by_meaning(search_term):
    query = {
        'match': {
            'meaning': search_term
        }
    }
    return search(query)


def multi_search(search_term: str, year: str, mode: int):
    if mode == 0:
        res = get_all(year)
    elif mode == 1:
        res = search_by_poem_name_and_year(search_term, year)
    elif mode == 2:
        res = search_by_metaphor_type(search_term)
    elif mode == 3:
        res = search_by_author_and_year(search_term, year)
    elif mode == 4:
        res = search_metaphors(search_term)
    elif mode == 5:
        res = search_metaphors_with_stemming(search_term)
    elif mode == 6:
        res = search_by_source(search_term)
    elif mode == 7:
        res = search_by_target(search_term)
    elif mode == 8:
        res = search_by_meaning(search_term)
    else:
        raise RuntimeError('Invalid search mode')

    return res
