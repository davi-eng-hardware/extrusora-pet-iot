#include <Stepper.h>
#include <SoftwareSerial.h>

// --- Configuração do Motor de Passo ---
const int passosPorVolta = 2048; 
Stepper motorExtrusora(passosPorVolta, 8, 10, 9, 11);

// --- Configuração do Bluetooth ---
SoftwareSerial bluetooth(2, 3); 

// --- Pinos de Controle ---
const int pinoPotenciometro = A0; 
const int pinoLED = 7; 
bool modoManual = false; // Variável nova pra guardar a ordem do botão
// --- Parâmetros do Processo ---
int temperaturaAlvo = 210; // Temperatura simulada para liberar o motor (210°C)
unsigned long tempoUltimoEnvio = 0; // Variável para controlar o envio via Bluetooth

void setup() {
  Serial.begin(9600);       // Monitor Serial (PC)
  bluetooth.begin(9600);    // Comunicação Bluetooth (Celular)
  
  pinMode(pinoLED, OUTPUT);
  
  // Velocidade baixa = Torque ALTO para puxar a fita
  motorExtrusora.setSpeed(10); 
  
  bluetooth.println("=== NIOBIO LABS: Sistema Iniciado ===");
  Serial.println("Sistema Iniciado. Aguardando Aquecimento...");
}

void loop() {
  // --- 1. ESCUTANDO O COMANDO DO LINUX ---
  if (bluetooth.available()) {
    char comando = bluetooth.read();
    if (comando == '1') {
      modoManual = true;  
    } else if (comando == '0') {
      modoManual = false; 
    }
  }

  // --- 2. LEITURA DO SENSOR ---
  int leituraBruta = analogRead(pinoPotenciometro);
  int temperaturaSimulada = map(leituraBruta, 0, 1023, 0, 250); 
  
  if (millis() - tempoUltimoEnvio > 1000) {
    bluetooth.print("Temp: ");
    bluetooth.print(temperaturaSimulada);
    bluetooth.print(" C | Alvo: ");
    bluetooth.println(temperaturaAlvo);
    tempoUltimoEnvio = millis();
  }

  // --- 3. O INTERLOCK ATUALIZADO ---
  if (temperaturaSimulada >= temperaturaAlvo || modoManual) {
    digitalWrite(pinoLED, HIGH);
    motorExtrusora.step(100); 
  } else {
    digitalWrite(pinoLED, HIGH);
    delay(100);
    digitalWrite(pinoLED, LOW);
    delay(100);
  }
}