package audio_steganography;

import java.io.IOException;
import java.util.Scanner;

public class Main {
	
	public static void main(String[] args) throws IOException, InterruptedException {
		
		// Those paths below need to change to your specific paths to make sure the code runs right
		
		// This is the carrier path, we will create a copy of this but that copy will contain the message
		String iCarrierPath = "C:\\Users\\thanh\\Library\\Workspace\\AudioSteganography\\audio_steganography\\input.wav";
		// This is the copy of the carrier path, which contains the message
		String oCarrierPath = "C:\\Users\\thanh\\Library\\Workspace\\AudioSteganography\\audio_steganography\\output.wav";
		
		// This is the message path that we will embed to the copy of the carrier
		//String messagePath = "C:\\Users\\thanh\\Library\\Workspace\\AudioSteganography\\audio_steganography\\message_image1.jpg";
		//String messagePath = "C:\\Users\\thanh\\Library\\Workspace\\AudioSteganography\\audio_steganography\\message_image2.jpg";
		//String messagePath = "C:\\Users\\thanh\\Library\\Workspace\\AudioSteganography\\audio_steganography\\message_text.txt";
		String messagePath = "C:\\Users\\thanh\\Library\\Workspace\\AudioSteganography\\audio_steganography\\message_video.mp4";
		
		try (Scanner sc = new Scanner(System.in)) {
			
			// The user's choice in the menu
			int i = 0;
			
			// Loop menu
			do {
				
				System.out.println("1. Embed\n2. Extract\n0.Exit\nYou choose: ");
				i = sc.nextInt(); // Read the user's choice
				if (i == 1) Embedding.embed(iCarrierPath,messagePath, oCarrierPath); // Embedding method
				else if (i == 2) Extracting.extract(); // Extracting method
				else i = 0; // Exit
				
			} while (i != 0); // do_while
			
		} // try (Scanner)
		
		System.out.println("Exit!\n");
		
	} // main(String)
	
} // class Main
