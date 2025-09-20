#include <Wire.h>
#include <RTClib.h>
#include <SD.h>
#include <SPI.h>

File logFile;
char filename[16];

int pinSD; // plaasts hier de CS pin waarop de SD module is aangesloten

unsigned long startMillis;

void setup() {
	Serial.begin(); // voer de baudrate include
	pinMode(pinSD, OUTPUT);
	
	if (SD.begin(pinSD)){
		Serial.println("SD card is ready for use.")
	} else {
		Serial.println("SD card is not connected!")
		return;
	}
	
	for (int i = 1; i < 1000; i++) {
		sprintf(filename, "LOG%03d.CSV", i);
		if (!SD.exists(filename)) {
			logFile = SD.open(filename, FILE_WRITE);
			break;
		}
	}
	
	if (!logFile) {
		Serial.println("Failed creating file!");
		//while(1);
	}
	
	logFile.println("TIMESTAMP,TIME_SINCE_START_MEASUREMENT,WINDSPEED,RPM");
	logFile.flush();
	
	startMillis = millis();
	
	Serial.print("Logging to: ");
	Serial.println(filename);
}

void loop() {
	static unsigned long lastlog = 0;
	unsigned long currentMillis = millis();
	
	if (currentMillis - lastlog >= 1000) {
		lastlog = currentMillis
		
		DateTime now = rtc.now();
		char timestamp[20];
		sprintf(timestamp, "%04d%02d%02d%02d%02d%02d", now.year(), now.month(), now.day(), now.hour(), now.minute(), now.second());
		
		unsigned long elapsed = (currentMillis - startMillis) / 1000;
		
		//Log data
		logFile.print(timestamp);
		logFile.print(",");
		logFile.print(elapsed);
		logFile.print(",");
		logFile.print(windspeed, BASE); // Zie documentation voor BASE nummers, maar chatgpt zegt de nauwkeurigheid achter te komma
		logFile.print(",");
		logFile.print(rpm, BASE);
		logFile.flush();
		
	}
}