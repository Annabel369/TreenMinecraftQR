#include <SPI.h>
#include <SD.h>
#include <TJpg_Decoder.h>
#include <TFT_eSPI.h> // Certifique-se de ter esta biblioteca configurada para o seu display

// Instancia o display TFT (ajuste os pinos no User_Setup.h da biblioteca TFT_eSPI se necessário)
TFT_eSPI tft = TFT_eSPI();

// Definições do projeto
#define TOTAL_FRAMES 425
#define PASTA_FRAMES "/frame"

unsigned long ultimoFrameTempo = 0;
const int intervaloFrame = 33; // ~30 FPS

unsigned long tempoPausaInicio = 0;
bool estaPausado = false;
unsigned long duracaoPausaAtual = 0;

int frameAtual = 1;

// Função de callback exigida pelo TJpg_Decoder
bool tft_output(int16_t x, int16_t y, uint16_t w, uint16_t h, uint16_t* bitmap) {
  if (y >= tft.height()) return 0;
  
  // Agora o 'tft' é reconhecido no escopo
  tft.pushImage(x, y, w, h, bitmap);
  return 1;
}

void setup() {
  Serial.begin(115200);

  // Inicializa o display TFT
  tft.begin();
  tft.setRotation(0); // Ajuste a rotação conforme seu hardware (0 a 3)
  tft.fillScreen(TFT_BLACK);

  // Inicializa o cartão SD e verifica se a pasta existe
  if (!SD.begin()) {
    Serial.println("Erro Crítico: Falha ao inicializar o Cartão SD!");
    tft.setCursor(10, 10);
    tft.setTextColor(TFT_RED);
    tft.println("Erro: Cartao SD!");
    return;
  }
  
  // Verifica se a pasta de frames existe no cartão SD
  if (!SD.exists(PASTA_FRAMES)) {
    Serial.printf("Erro: A pasta '%s' não foi encontrada no cartão SD!\n", PASTA_FRAMES);
  } else {
    Serial.printf("Pasta '%s' encontrada com sucesso no SD.\n", PASTA_FRAMES);
  }

  // Configura o decodificador JPEG
  TJpgDec.setJpgScale(1);
  TJpgDec.setCallback(tft_output);
}

void loop() {
  unsigned long tempoAtual = millis();

  // Se estiver em pausa nos frames específicos (ex: 33, 109, 192, 417)
  if (estaPausado) {
    // Se quiser que as folhas caiam enquanto o QR code está estático, chame sua função aqui:
    // animateSakuraLeaves(); 

    if (tempoAtual - tempoPausaInicio >= duracaoPausaAtual) {
      estaPausado = false; // Retoma a animação normal
    }
    return;
  }

  // Controla o intervalo de 30 FPS
  if (tempoAtual - ultimoFrameTempo >= intervaloFrame) {
    ultimoFrameTempo = tempoAtual;

    char caminhoArquivo[50];
    sprintf(caminhoArquivo, "%s/frame_%04d.jpg", PASTA_FRAMES, frameAtual);

    // Verifica se o arquivo individual existe no cartão antes de decodificar
    if (SD.exists(caminhoArquivo)) {
      TJpgDec.drawSdJpg(0, 0, caminhoArquivo);
    } else {
      Serial.printf("Aviso: Arquivo %s não encontrado no SD!\n", caminhoArquivo);
    }

    // Define quais frames devem pausar (ex: 33, 109, 192, 417) e por quanto tempo (ex: 5 segundos)
    if (frameAtual == 33 || frameAtual == 109 || frameAtual == 192 || frameAtual == 417) {
      estaPausado = true;
      tempoPausaInicio = tempoAtual;
      duracaoPausaAtual = 5000; // 5 segundos de pausa (mude para 30000 se preferir 30 segundos)
      Serial.printf("Pausa ativada no frame_%04d.jpg\n", frameAtual);
    }

    frameAtual++;
    if (frameAtual > TOTAL_FRAMES) {
      frameAtual = 1; // Reinicia o ciclo da animação
    }
  }
}