#include <WiFi.h>
#include <WebServer.h>
#include <OneWire.h>
#include <DallasTemperature.h>
#include <AccelStepper.h>
#include <EEPROM.h>

#define STEP_CALIENTE 15
#define DIR_CALIENTE 2
#define STEP_FRIA 18
#define DIR_FRIA 5

const float vueltasPorApertura = 2.5;
const int pasosPorVuelta = 200;
const int microsteps = 16;
int PASOS_MAXIMOS = 0;

AccelStepper motorCaliente(AccelStepper::DRIVER, STEP_CALIENTE, DIR_CALIENTE);
AccelStepper motorFria(AccelStepper::DRIVER, STEP_FRIA, DIR_FRIA);

#define ONE_WIRE_BUS 4
OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensores(&oneWire);

DeviceAddress sensorCaliente = { 0x28, 0xCF, 0x89, 0x52, 0x00, 0x00, 0x00, 0x42 };
DeviceAddress sensorFria     = { 0x28, 0x56, 0x10, 0x57, 0x04, 0xE1, 0x3C, 0x92 };
DeviceAddress sensorSalida   = { 0x28, 0x58, 0x59, 0x54, 0x00, 0x00, 0x00, 0x21 };

const char* ssid = "MATVPC 5014";
const char* password = "Marco12345";
WebServer server(80);

#define EEPROM_SIZE 3
#define ADDR_CALIENTE 0
#define ADDR_FRIA 1
#define ADDR_MODO 2

int aperturaCaliente = 0;
int aperturaFria = 0;
int aperturaAnteriorCaliente = -1;
int aperturaAnteriorFria = -1;

enum Modo { CALIBRACION, SIMULACION };
Modo modoActual = SIMULACION;
unsigned long tiempoFinalBanio = 0;

// PID Variables
float setpoint = 0;
float tempSalida = 0;
float error = 0, lastError = 0, integral = 0, derivative = 0;
float Kp = 2.0, Ki = 0.05, Kd = 1.0;
unsigned long lastTime = 0;

void guardarEEPROM(int direccion, uint8_t valor) {
  if (EEPROM.read(direccion) != valor) {
    EEPROM.write(direccion, valor);
    EEPROM.commit();
  }
}

void setup() {
  Serial.begin(115200);
  sensores.begin();

  EEPROM.begin(EEPROM_SIZE);
  PASOS_MAXIMOS = vueltasPorApertura * pasosPorVuelta * microsteps;
  Serial.printf("⚙️ PASOS_MAXIMOS calculado: %d pasos\n", PASOS_MAXIMOS);

  aperturaCaliente = EEPROM.read(ADDR_CALIENTE);
  aperturaFria     = EEPROM.read(ADDR_FRIA);
  modoActual = (Modo) EEPROM.read(ADDR_MODO);

  int posCal = map(aperturaCaliente, 0, 100, 0, PASOS_MAXIMOS);
  int posFr  = map(aperturaFria,     0, 100, 0, PASOS_MAXIMOS);

  motorCaliente.setCurrentPosition(posCal);
  motorFria.setCurrentPosition(posFr);

  aperturaAnteriorCaliente = aperturaCaliente;
  aperturaAnteriorFria     = aperturaFria;

  motorCaliente.setMaxSpeed(500);
  motorCaliente.setAcceleration(300);
  motorFria.setMaxSpeed(500);
  motorFria.setAcceleration(300);

  WiFi.begin(ssid, password);
  Serial.print("Conectando a WiFi...");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\n✅ WiFi conectado");
  Serial.print("🟢 IP local asignada: ");
  Serial.println(WiFi.localIP());

  server.on("/setpoint", HTTP_GET, []() {
    if (server.hasArg("caliente") && server.hasArg("fria")) {
      aperturaCaliente = server.arg("caliente").toInt();
      aperturaFria = server.arg("fria").toInt();
      Serial.printf("🔧 Apertura recibida → Caliente: %d%% | Fría: %d%%\n", aperturaCaliente, aperturaFria);

      guardarEEPROM(ADDR_CALIENTE, aperturaCaliente);
      guardarEEPROM(ADDR_FRIA, aperturaFria);

      server.send(200, "text/plain", "OK");
    } else {
      server.send(400, "text/plain", "Faltan parámetros 'caliente' y/o 'fria'");
    }
  });

  server.on("/temperaturas", HTTP_GET, []() {
    sensores.requestTemperatures();
    float t1 = sensores.getTempC(sensorCaliente);
    float t2 = sensores.getTempC(sensorFria);
    tempSalida = sensores.getTempC(sensorSalida);

    Serial.printf("🌡️ Temp Caliente: %.2f°C | Fría: %.2f°C | Salida: %.2f°C\n", t1, t2, tempSalida);

    String json = "{\"caliente\":" + String(t1, 2) + ",\"fria\":" + String(t2, 2) + ",\"salida\":" + String(tempSalida, 2) + "}";
    server.send(200, "application/json", json);
  });

  server.on("/aperturas", HTTP_GET, []() {
    String json = "{\"caliente\":" + String(aperturaCaliente) + ",\"fria\":" + String(aperturaFria) + "}";
    server.send(200, "application/json", json);
  });

  server.on("/set_modo", HTTP_GET, []() {
    if (server.hasArg("modo")) {
      String modo = server.arg("modo");
      if (modo == "calibracion") modoActual = CALIBRACION;
      else if (modo == "simulacion") modoActual = SIMULACION;
      guardarEEPROM(ADDR_MODO, (uint8_t)modoActual);
      server.send(200, "text/plain", "Modo actualizado");
    } else {
      server.send(400, "text/plain", "Falta parámetro 'modo'");
    }
  });

  server.on("/inicio_banio", HTTP_GET, []() {
    if (server.hasArg("duracion") && server.hasArg("setpoint")) {
      int duracion = server.arg("duracion").toInt();
      setpoint = server.arg("setpoint").toFloat();
      tiempoFinalBanio = millis() + duracion * 1000UL;
      server.send(200, "text/plain", "Temporizador y setpoint establecidos");
    } else {
      server.send(400, "text/plain", "Faltan parámetros 'duracion' y/o 'setpoint'");
    }
  });

  server.begin();
  Serial.println("🌐 Servidor HTTP iniciado.");
}

void loop() {
  server.handleClient();

  if (!sensores.validAddress(sensorCaliente) || !sensores.validAddress(sensorFria) || !sensores.validAddress(sensorSalida)) {
    Serial.println("⚠️ Error: Al menos una dirección de sensor no es válida.");
    delay(1000);
    return;
  }

  if (modoActual == SIMULACION && tiempoFinalBanio > 0) {
    unsigned long now = millis();
    float dt = (now - lastTime) / 1000.0;
    lastTime = now;

    error = setpoint - tempSalida;
    integral += error * dt;
    derivative = (error - lastError) / dt;
    lastError = error;

    float control = Kp * error + Ki * integral + Kd * derivative;

    aperturaCaliente += control;
    aperturaFria -= control;

    aperturaCaliente = constrain(aperturaCaliente, 0, 100);
    aperturaFria = constrain(aperturaFria, 0, 100);

    int destinoCal = map(aperturaCaliente, 0, 100, 0, PASOS_MAXIMOS);
    int destinoFr  = map(aperturaFria, 0, 100, 0, PASOS_MAXIMOS);

    motorCaliente.moveTo(destinoCal);
    motorFria.moveTo(destinoFr);

    if (millis() >= tiempoFinalBanio) {
      motorCaliente.moveTo(0);
      motorFria.moveTo(0);
      tiempoFinalBanio = 0;
      Serial.println("⏱️ Baño terminado. Motores regresando a home.");
    }
  }

  motorCaliente.run();
  motorFria.run();
}
