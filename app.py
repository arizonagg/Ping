from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup, NavigableString

app = Flask(__name__)

@app.route('/pingapi', methods=['GET'])
def harga_emas():
    try:
        url = 'https://digital.pegadaian.co.id'
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        harga_elements = soup.find_all(class_='detail-harga__left')
        harga_list = []

        for elem in harga_elements:
            h5 = elem.find('h5')
            if h5:
                # Ambil hanya teks langsung dari h5, tanpa teks dalam span
                text_only = ''.join(t for t in h5.contents if isinstance(t, NavigableString)).strip()
                harga_list.append(text_only)

        return jsonify({
            'harga_emas': harga_list,
            'sumber': url
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
