public class AlarmAutomata {
	private int state;
	private int h;
	private int m;
	private int ah;
	private int am;

	public AlarmAutomata() {
		state=1;
		h = 0;
		m = 0;
		ah = 0;
		am = 0;
	}

	public void step(int event) {
		switch (state) {
			case 1: // alarm is off
				switch(event) {
					case 1: z1();break; // H
					case 2: z2(); break; // M
					case 3: z5(); break; // T
					case 4: state = 2; break; // A
				}
				break;
			case 2: // setting alarm
				switch(event) {
					case 1: z3();break; // H
					case 2: z4(); break; // M
					case 3: z5(); break; // T
					case 4: state = 3; break; // A
				}
				break;
			case 3: // alarm is off
				switch(event) {
					case 1: z1();break; // H
					case 2: z2(); break; // M
					case 3: // T
						if ((60 * ah + am) == (60 * h + m)) {
							z6(); z5();
						} else if ((60 * ah + am + 1) % (60 * 23 + 59) == (60 * h + m)) {
							z7(); z5();
						} else { // not x1 and not x2
							z5();
						}
						break; 
					case 4: z7(); state = 2; break; // A
				}
				break;
			default:
		}
	}

	public void z1() {
		h = (h + 1) % 24;
		System.out.println("h=" + h + " m=" + m);
		System.out.println("ah=" + ah + " am=" + am);
	}
	public void z2() {
		m = (m + 1) % 60;
		System.out.println("h=" + h + " m=" + m);
		System.out.println("ah=" + ah + " am=" + am);
	}
	public void z3() {
		ah = (ah + 1) % 24;
		System.out.println("h=" + h + " m=" + m);
		System.out.println("ah=" + ah + " am=" + am);
	}
	public void z4() {
		am = (am + 1) % 60;
		System.out.println("h=" + h + " m=" + m);
		System.out.println("ah=" + ah + " am=" + am);
	}
	public void z5() {
		m = (m + 1) % 60;
		if (m == 0) h = (h + 1) % 24;
		System.out.println("h=" + h + " m=" + m);
		System.out.println("ah=" + ah + " am=" + am);
	}
	public void z6() {
		System.out.println("Включить звонок");
	}
	public void z7() {
		System.out.println("Выключить звонок");
	}
}