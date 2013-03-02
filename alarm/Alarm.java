package alarm;

import java.io.*;
import java.util.*;
import alarm.AlarmAutomata;

public class Alarm {

	public static void main(String[] args) throws Exception {
		Reader in = new FileReader("alarm-test");
		AlarmAutomata automata = new AlarmAutomata();
		int r;
		try{
			while ((r = in.read()) != -1) {
				char command = (char)r;
				switch (command) {
					case 'h': automata.step(1);break;
					case 'm': automata.step(2);break;
					case 't': automata.step(3);break;
					case 'a': automata.step(4);break;
					case 'q': System.exit(0);break;
					default:
						
				}
			}
		} catch (Exception e) {
			System.exit(0);
		}
	}
}