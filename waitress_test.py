from waitress import serve
import extractionservice
serve(extractionservice.app, host='10.90.213.248', port=5000)
