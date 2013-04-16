package stack;

public class Stack {
	private int size;

	public Stack() {
		size = 0;
	}

	public void add() {
		if (size == 0) {
			s_1();
		} else {
			s_inc();
		}
	}

	public String size() {
		if (size == 0) {
			zero();
			return "zero";
		}
		if (size == 1) {
			one();
			return "one";
		}
		many();
		return "many";
	}

	public void remove() {
		if (size > 0) {
			if (size > 1) {
				s_dec();
			} else {
				s_0();
			}
		} else {
			error();
		}
	}

	public void error() {
		System.exit(1);
	}

	public void s_inc() {
		size++;
	}
	public void s_dec() {
		size--;
	}
	public void s_1() {
		size = 1;
	}
	public void s_0() {
		size = 0;
	}
	public void zero() {}
	public void one() {}
	public void many() {}
}