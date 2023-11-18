package audio_steganography;
import java.io.IOException;
import java.util.Scanner;
public class Main {
	public static void main(String[] args) throws IOException, InterruptedException {
		try (Scanner sc = new Scanner(System.in)) {
			int i = 0;
			do {
				System.out.println("1. Embed\n2. Extract\n0.Exit\nYou choose: ");
				i = sc.nextInt();
				if (i == 1) Embedding.embed();
				//if (i == 1) Embedding.hideDataInAudio();
				else if (i == 2) Extracting.extract();
				else i = 0;
			} while (i != 0);
		}
		System.out.println("Exit!\n");
	}
}
