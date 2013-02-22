public class Alarm {

	public static void main(String[] args) {
		AlarmAutomata automata = new AlarmAutomata();
		char command = 't';
		try{
			while (true) {
				command = (char)System.in.read();
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