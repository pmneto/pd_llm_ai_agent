from datetime import datetime
import locale

# Garante formatação em português se estiver no Linux/macOS
try:
    locale.setlocale(locale.LC_TIME, 'pt_BR.utf8')
except:
    pass  # No Windows ou se não funcionar, usa padrão

def get_today():
    '''This function returns which day is today'''
    agora = datetime.now()
    return agora.strftime("%A, %d de %B de %Y")  # ex: quarta-feira, 26 de junho de 2025
