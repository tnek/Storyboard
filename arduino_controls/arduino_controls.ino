#define L_BUTT 13
#define R_BUTT 12

#define PING_TICKS 1000

class Button {
  public:
    Button(const unsigned pin) : pin(pin) {
      pinMode(pin, INPUT);
    }
    pressed() {
      bool prev_down = down;
      down = digitalRead(pin);
      if (down && !prev_down) {
        return true;
      }
      return false;
    }
  private:
    unsigned pin;
    bool down = false;
} ;

Button* l_butt = nullptr;
Button* r_butt = nullptr;
bool serial_connected = false;

void setup() {
  // put your setup code here, to run once:
  l_butt = new Button(L_BUTT);
  r_butt = new Button(R_BUTT);
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  if (Serial.available() > 0) { // Check if we are connected!
    String ping =  Serial.readStringUntil('\n');
    Serial.println("[INFO] Received " + ping);
    if (ping == "PING") {
      serial_connected = true;
      Serial.println("[PONG]");
    } else if (ping == "RST") {
      serial_connected = false;
      Serial.println("[ACK]");
    }
  } else if (!serial_connected) {
    Serial.println("[INFO] Waiting for serial...");
    delay(1000);
  }

  // We do not want to do anything until we are connected.
  if (!serial_connected) return;

  if (l_butt->pressed()) {
    Serial.println("[Button] LEFT");
  } else if (r_butt->pressed()) {
    Serial.println("[Button] RIGHT");
  }

  delay(1);
}
