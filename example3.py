import re
import requests
import lxml.html as lhtml

URL = 'https://www.python.org/'


def get_elements(response, css):
    # получаем список элементов соответствующий css-селектору
    element = lhtml.document_fromstring(response.text).cssselect(css)
    if not element:
        return None

    # очищаем от пробелов и переноса строки
    return re.sub("^\s+|\n|\r|\s+$", '', element[0].text_content())


if __name__ == '__main__':

    try:
        response = requests.get(URL, timeout=3)
    except TimeoutError:
        print('Timeout error')
    except Exception:
        print('Connection error')
    else:

        # получаем ссылки на страницы с описанием события
        css = '.event-widget div.shrubbery ul.menu li a'
        css_list = lhtml.document_fromstring(response.text).cssselect(css)
        href_list = [element.get('href') for element in css_list]

        for href in href_list:
            try:
                response = requests.get(URL + href, timeout=3)
            except Exception:
                continue

            event = get_elements(response, '.single-event-title')
            location = get_elements(response, '.single-event-location')

            event_date = get_elements(response, '.single-date')
            if event_date:
                event_start = get_elements(response, '.time-start')
                event_end = get_elements(response, '.time-end')
            else:
                event_start = get_elements(response, '.date-start')
                event_end = get_elements(response, '.date-end')

            event_year = get_elements(response, '.year')

            print('%s %s %s %s %s' % (event, location, event_start, event_end, event_year))
