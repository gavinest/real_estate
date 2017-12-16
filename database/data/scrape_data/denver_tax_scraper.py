import pandas as pd
import requests
from bs4 import BeautifulSoup
from collections import OrderedDict
import json
import ast

class denverTax(object):
    def __init__(self, pin):
        super(denverTax, self).__init__()
        self.base_url = 'https://www.denvergov.org/property/realproperty/'
        self.pin = pin

        #call scrappers
        self._summary_info()
        self._assessment_info()
        self._chain_of_title()
        self._taxes()
        self._comps()
        # self._save_data()

    def _summary_info(self):
        endpoint = 'summary/'
        r = requests.get(self.base_url + endpoint + self.pin)
        soup = BeautifulSoup(r.text, 'html.parser')
        try:
            property_table = soup.select('div#property_summary')[0]
        except IndexError:
            print '\nError on pin {}'.format(self.pin)
            self.prop_general = {'pin': self.pin}
            self.prop_summary = {'pin': self.pin}
        else:
            self.prop_summary = {'pin': self.pin}
            for row in property_table.find_all('tr'):
                cells = row.find_all('td')
                k1, v1, k2, v2 = cells
                self.prop_summary[k1.text.encode('utf-8').strip()] = v1.text.encode('utf-8').strip()
                self.prop_summary[k2.text.encode('utf-8').strip()] = v2.text.encode('utf-8').strip()

            general = soup.select('table#property-info-bar')[0]
            titles = [title.text.encode('utf-8') for title in general.find_all('th') if title.text]
            titles.pop(0)
            titles = OrderedDict(zip(titles, range(len(titles))))

            owner_cell_labels = ['owner1', 'owner2', 'address', 'city/state/zip']
            owner_cell = [' '.join(_.text.strip().split()) for _ in general.find_all('td')[0].find_all('div')]
            prop_general = dict(zip(owner_cell_labels, owner_cell))
            csz = prop_general.pop('city/state/zip')
            city, _, state, zipcode = csz.split(' ')
            # zipcode = csz.split(' ')[0]
            # city, state = csz.split(' , ')[:2]
            prop_general['zip'] = zipcode
            prop_general['city'] = city
            prop_general['state'] = state

            cells = [' '.join(cell.text.encode('utf-8').strip().split()) for cell in general.find_all('td')]
            cells.pop(0)
            cells.pop(1)
            prop_general.update(dict(zip(titles.keys(), cells)))
            self.prop_general = prop_general
            self.prop_general['pin'] = self.pin

    def _assessment_info(self):
        endpoint = 'assessment/'
        r = requests.get(self.base_url + endpoint + self.pin)
        soup = BeautifulSoup(r.text, 'html.parser')
        try:
            assessment = soup.select('div#assessment_data')[0]
        except IndexError:
            print '\nError on pin {}'.format(self.pin)
            self.prop_assessment = {'pin': self.pin}
        else:
            titles = set([title.text for title in assessment.find_all('th') if title.text])

            self.prop_assessment = {'pin': self.pin}
            for row in assessment.find_all('tr'):
                if row.find_all('td'):
                    cells =  [_.text.encode('utf-8') for _ in row.find_all('td')]
                    key, values = cells[0], cells[1:]
                    self.prop_assessment[key] = dict(zip(titles, values))

    def _chain_of_title(self):
        endpoint = 'chainoftitle/'
        r = requests.get(self.base_url + endpoint + self.pin)
        soup = BeautifulSoup(r.text, 'html.parser')
        try:
            chain = soup.select('div.panel.panel-primary')[0]
        except IndexError:
            print '\nError on pin {}'.format(self.pin)
            self.prop_title = {'pin': self.pin}
        else:
            titles = [title.text for title in chain.find('tr').find_all('th') if title.text]
            self.prop_title = {
                'pin': self.pin,
                'title': [],
                }
            for row in chain.find_all('tr'):
                if row.find_all('td'):
                    cells =  [_.text.encode('utf-8') for _ in row.find_all('td')]
                    self.prop_title['title'].append(dict(zip(titles, cells)))

    def _taxes(self):
        endpoint = 'taxes/'
        r = requests.get(self.base_url + endpoint + self.pin)
        soup = BeautifulSoup(r.text, 'html.parser')
        try:
            tax_table = soup.select('table#TaxesTable')[0]
        except IndexError:
            print '\nError on pin {}'.format(self.pin)
            self.prop_tax = {'pin': self.pin}
        else:
            titles = [title.text for title in tax_table.find_all('th') if title.text]
            self.prop_tax = {'pin': self.pin}
            for row in tax_table.find_all('tr'):
                if row.find_all('td'):
                    cells =  [_.text.encode('utf-8') for _ in row.find_all('td')]
                    key, values = cells[0], cells[1:]
                    self.prop_tax[key] = dict(zip(titles, values))

    def _comps(self):
        endpoint = 'comparables/'
        r = requests.get(self.base_url + endpoint + self.pin)
        soup = BeautifulSoup(r.text, 'html.parser')
        try:
            comps_table = soup.select('table.table.table-striped')[0]
        except IndexError:
            print '\nError on pin {}'.format(self.pin)
            self.prop_comps = {'pin': self.pin}
        else:
            comps_row = comps_table.findAll('tr')[2]
            comps_schedule_nums = [_.text.encode('utf-8') for _ in comps_row.findChildren()[1:]]
            self.prop_comps = {'comps': comps_schedule_nums}
            self.prop_comps['pin'] = self.pin

    def _check_new_file(file_name, columns):
        if not os.path.isfile(file_name):
            with open(filename, 'w') as f:
                f.write(','.join(columns) + '\n')

    def _save_data(self):
        with open('prop_general.txt', 'a') as f:
            entry = json.dumps(ast.literal_eval(str(self.prop_general)))
            f.write(entry + '\n')
        with open('prop_assessment.txt', 'a') as f:
            entry = json.dumps(ast.literal_eval(str(self.prop_assessment)))
            f.write(entry + '\n')
        with open('prop_tax.txt', 'a') as f:
            entry = json.dumps(ast.literal_eval(str(self.prop_tax)))
            f.write(entry + '\n')
        with open('prop_summary.txt', 'a') as f:
            entry = json.dumps(ast.literal_eval(str(self.prop_summary)))
            f.write(entry + '\n')
        with open('prop_title.txt', 'a') as f:
            entry = json.dumps(ast.literal_eval(str(self.prop_title)))
            f.write(entry + '\n')
        with open('prop_comps.txt', 'a') as f:
            entry = json.dumps(ast.literal_eval(str(self.prop_comps)))
            f.write(entry + '\n')
        print '\nFinished scraped pindata to file. Pin {}.'.format(self.pin)


if __name__ == '__main__':
    # pin = '161355168'
    # pin = '164177451'
    pin = '160434078'
    d = denverTax(pin)
