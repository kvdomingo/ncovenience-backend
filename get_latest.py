import os
from time import time
from django.conf import settings
from phcovid.phcovid import get_cases


def main():
    t0 = time()
    df = get_cases()
    t1 = time()
    print(f'Done in {(t1 - t0)/60} minutes')
    with open(os.path.join(settings.BASE_DIR, 'web/static/web/data/latest.json'), 'w') as f:
        df.to_json(f, indent=4, orient='index')


if __name__ == '__main__':
    main()
