import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Força o ambiente do script a utilizar o fuso horário de São Paulo
os.environ['TZ'] = 'America/Sao_Paulo'

def configurar_driver():
    """Configura o Chrome com fuso horário local e modo headless."""
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    
    # Tenta forçar o fuso horário no navegador via argumento
    chrome_options.add_argument("--timezone=America/Sao_Paulo")
    
    chrome_options.binary_location = "/usr/bin/chromium"
    
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def executar_ciclo():
    """Executa o navegador por 3 horas e depois fecha tudo para liberar memória."""
    driver = configurar_driver()
    
    try:
        # Acessa as URLs iniciais
        driver.get("https://botapostamax.netlify.app/")
        driver.execute_script("window.open('https://botapostaganha.netlify.app/');")
        
        intervalo_refresh = 1200  # 20 minutos em segundos
        intervalo_reiniciar = 10800  # 3 horas em segundos
        
        inicio_ciclo = time.time()
        ultima_atualizacao = time.time()
        
        while True:
            agora = time.time()
            
            # Condição para reiniciar o script 100% (3 horas)
            if (agora - inicio_ciclo) > intervalo_reiniciar:
                print("Reiniciando o navegador para limpar RAM e CPU...")
                break # Sai do loop interno para cair no 'finally' e reabrir
                
            # Alternância extremamente rápida entre abas
            for handle in driver.window_handles:
                driver.switch_to.window(handle)
                time.sleep(0.2) # Pausa mínima para processamento
            
            # Refresh a cada 20 minutos
            if (agora - ultima_atualizacao) > intervalo_refresh:
                for handle in driver.window_handles:
                    driver.switch_to.window(handle)
                    driver.refresh()
                ultima_atualizacao = time.time()
                
    except Exception as e:
        print(f"Erro detectado: {e}")
    finally:
        # Garante o fechamento total do processo do Chromium
        driver.quit()

def main():
    while True:
        executar_ciclo()
        # Pequena pausa de segurança de 5 segundos antes de reabrir tudo de novo
        time.sleep(5)

if __name__ == "__main__":
    main()
