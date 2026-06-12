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

def main():
    driver = configurar_driver()
    
    # Acessa as URLs
    driver.get("https://botapostamax.netlify.app/")
    driver.execute_script("window.open('https://botapostaganha.netlify.app/');")
    
    intervalo_refresh = 1200 # 20 minutos em segundos
    ultima_atualizacao = time.time()
    
    try:
        while True:
            # Alternância extremamente rápida entre abas
            for handle in driver.window_handles:
                driver.switch_to.window(handle)
                # Pausa mínima para o navegador processar a troca
                time.sleep(0.2) 
            
            # Refresh a cada 20 minutos
            if (time.time() - ultima_atualizacao) > intervalo_refresh:
                for handle in driver.window_handles:
                    driver.switch_to.window(handle)
                    driver.refresh()
                ultima_atualizacao = time.time()
                
    except Exception:
        pass
    finally:
        driver.quit()

if __name__ == "__main__":
    main()