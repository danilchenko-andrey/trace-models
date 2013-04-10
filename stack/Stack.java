package stack;

public class Stack {
	private int size;

	public Stack() {
		size = 0;
	}

	public void add() {
		size++;
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
			size--;
		} else {
			error();
		}
	}

	public void error() {
		System.exit(1);
	}

	public void zero() {}
	public void one() {}
	public void many() {}
}