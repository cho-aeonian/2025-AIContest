#include <Servo.h>

Servo MG996;
#define mg996 8

char currentCommand = 'x'; // 직전 명령
char lastCommand = 'x';
int value = 0;

void setup() {
  Serial.begin(9600);
  MG996.attach(mg996);
  Serial.println("아두이노 시작됨");
}

void loop() {
  value = analogRead(A3);

  // 센서값 전송 (구분자 포함)
  Serial.print("W:"); 
  Serial.println(value);

  // 명령 수신
  if (Serial.available() > 0) {
    currentCommand = Serial.read();
  }

  // 명령이 바뀐 경우에만 처리
  if (currentCommand != lastCommand) {
    if (currentCommand == '1' && value >= 310) {
      MG996.write(0);
      Serial.println("모터 0도 (출하돈)");
    }
    else if (currentCommand == '0' && value <= 310) {
      MG996.write(80);
      Serial.println("모터 80도 (임신돈)");
    }
    lastCommand = currentCommand;
  }

  delay(1000); // 1초 간격
}
