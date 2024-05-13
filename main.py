from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/company/<path:company_url>')
def get_company_data(company_url):
    url = f"https://finchat.io/company/NYSE-{company_url}"
           #https://finchat.io/company/NYSE-PLTR/
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes

        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table')

        if table:
            # Trova le righe e colonne della tabella
            rows = table.find_all('tr')
            data = []
            for row in rows:
                cols = row.find_all('td')
                cols = [col.text.strip() for col in cols]
                data.append(cols)
            
            return jsonify({'table_data': data})
        else:
            return jsonify({'error': 'Nessuna tabella trovata'})

    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run()
