import requests
from bs4 import BeautifulSoup
import csv

class Bolsa:
    def __init__(self, url, headers):
        self.url = url
        self.headers = headers

    def get_elementos(self):
        response = requests.get(url=self.url, headers=self.headers)
        # print(resp.status_code)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')
        tabla = soup.find('table', class_='Wikitable Ordenable')
        filas = tabla.find_all('tr')[1:]
        return filas

    def crea_csv_y_calcula(self, filas):
        with open('dTabla.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['P.', 'Economía', 'Bolsa', 'Capital', 'Volúmen'])

            total_capital = 0
            total_volumen = 0

            for fila in filas:
                celdas = fila.find_all('td')
                id_p = celdas[0].text.strip() # P.
                economia = celdas[1].text.strip() # Economía
                bolsa = celdas[2].text.strip() # Bolsa
                capital = celdas[3].text.strip() # Capitalización
                volumen = celdas[4].text.strip() # Volúmen de intercambios

                try:
                    capital = float(capital)
                    volumen = float(volumen)
                except ValueError as ve:
                    continue

                writer.writerow([id_p, economia, bolsa, f'{capital:,.2f}', f'{volumen:,.2f}'])

                total_capital += capital
                total_volumen += volumen

        print(f'Total Capital: {total_capital:,.2f}')
        print(f'Total Volumen: {total_volumen:,.2f}')


if __name__ == '__main__':
    url = 'https://es.wikipedia.org/wiki/Bolsa_de_valores'
    h  = {'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Mobile Safari/537.36'}
    bolsa = Bolsa(url, h)
    filas = bolsa.get_elementos()
    bolsa.crea_csv_y_calcula(filas)
