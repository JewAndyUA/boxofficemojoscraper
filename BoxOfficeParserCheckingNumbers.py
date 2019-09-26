def Check(worldwide, domestic, overseas, budget):
    if worldwide == 'n/a' or domestic == 'N/A':
        worldwide = '$0'
    if domestic == 'n/a' or domestic == 'N/A':
        domestic = '$0'
    if overseas == 'n/a' or overseas == 'N/A':
        overseas = '$0'
    if budget == 'n/a' or domestic == 'N/A':
        budget = '$0'

    return worldwide[1:], domestic[1:], overseas[1:], budget[1:]

