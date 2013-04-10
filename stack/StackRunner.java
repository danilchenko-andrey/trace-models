package stack;

import java.io.*;
import java.util.*;
import stack.Stack;

public class StackRunner {

	public static void main(String[] args) throws Exception {
		Reader in = new FileReader("stack-test");
		Stack stack = new Stack(); 
		int r;
		try{
			while ((r = in.read()) != -1) {
				char command = (char)r;
				switch (command) {
					case 'a': stack.add();break;
					case 'r': stack.remove();break;
					case 's': stack.size();break;
					default:
						
				}
			}
		} catch (Exception e) {
			System.exit(0);
		}
	}
}