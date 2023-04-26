import languages as lang


def trans(id, current_language):
    string = lang.languages[current_language][id]

    return string