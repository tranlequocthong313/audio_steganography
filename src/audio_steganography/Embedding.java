package audio_steganography;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.nio.file.Files;
public class Embedding {
	public static void embed() throws IOException {
		String audioPath = "C:\\Users\\thanh\\Library\\Workspace\\AudioSteganography\\audio_steganography\\input.wav";
		//String embedPath = "C:\\Users\\thanh\\Library\\Workspace\\AudioSteganography\\audio_steganography\\message_image1.jpg";
		//String embedPath = "C:\\Users\\thanh\\Library\\Workspace\\AudioSteganography\\audio_steganography\\message_image2.jpg";
		//String embedPath = "C:\\Users\\thanh\\Library\\Workspace\\AudioSteganography\\audio_steganography\\message_text.txt";
		String embedPath = "C:\\Users\\thanh\\Library\\Workspace\\AudioSteganography\\audio_steganography\\message_video.mp4";
		String outputPath = "C:\\Users\\thanh\\Library\\Workspace\\AudioSteganography\\audio_steganography\\output.wav";
		
        File audioFile = new File(audioPath);
        File fileToEmbed = new File(embedPath);
        Metadata f = new Metadata(embedPath);
        
        if (audioFile.length() / f.getLength() < 9) {
        	System.out.println("Failed to embed! The file is too big!");
        	return;
        }
        
        File outputFile = new File(outputPath);
        
        FileInputStream audioIn = new FileInputStream(audioFile);
        FileInputStream fileIn = new FileInputStream(fileToEmbed);
        FileOutputStream out = new FileOutputStream(outputFile);

        byte[] audioBuffer = new byte[(int)audioFile.length()];
        byte[] fileBuffer = new byte[(int)fileToEmbed.length()];
        
        int audioLength;
        int fileLength;
        
        int wav_header = 44;
        
        while ((audioLength = audioIn.read(audioBuffer)) > 0 && (fileLength = fileIn.read(fileBuffer)) > 0) {
        	//int messageIndex = 0;
        	int j = 0;
            for (int i = 0; i < fileLength || j < fileLength; i = i + 8) {
            	
            	// lay 7 bit cua audio + tung bit mot cua embed file
            	//audioBuffer[i + wav_header] = (byte) ((audioBuffer[i + wav_header] & 0xFE) | (fileBuffer[i] & 0x01));
            	byte temp = (byte)fileBuffer[j];
            	audioBuffer[i + wav_header] = (byte) ((audioBuffer[i + wav_header] & 0xFE) | (((temp & 0x80) >> 7) & 0x01));
            	temp = (byte)fileBuffer[j];
            	audioBuffer[i + wav_header + 1] = (byte) ((audioBuffer[i + wav_header + 1] & 0xFE) | ((temp & 0x40) >> 6));
            	temp = (byte)fileBuffer[j];
            	audioBuffer[i + wav_header + 2] = (byte) ((audioBuffer[i + wav_header + 2] & 0xFE) | ((temp & 0x20) >> 5));
            	temp = (byte)fileBuffer[j];
            	audioBuffer[i + wav_header + 3] = (byte) ((audioBuffer[i + wav_header + 3] & 0xFE) | ((temp & 0x10) >> 4));
            	temp = (byte)fileBuffer[j];
            	audioBuffer[i + wav_header + 4] = (byte) ((audioBuffer[i + wav_header + 4] & 0xFE) | ((temp & 0x08) >> 3));
            	temp = (byte)fileBuffer[j];
            	audioBuffer[i + wav_header + 5] = (byte) ((audioBuffer[i + wav_header + 5] & 0xFE) | ((temp & 0x04) >> 2));
            	temp = (byte)fileBuffer[j];
            	audioBuffer[i + wav_header + 6] = (byte) ((audioBuffer[i + wav_header + 6] & 0xFE) | ((temp & 0x02) >> 1));
            	temp = (byte)fileBuffer[j];
            	audioBuffer[i + wav_header + 7] = (byte) ((audioBuffer[i + wav_header + 7] & 0xFE) | (temp & 0x01));
            	
            	j++;
            }
            
            /*for (int i = wav_header; i < audioLength && messageIndex < fileLength; i++) {
                for (int j = 0; j < 8; j++) {
                    int bit = (fileBuffer[messageIndex] >> j) & 1;
                    audioBuffer[i] = (byte) ((audioBuffer[i] & 0xFE) | bit);
                    messageIndex++;
                    if (messageIndex >= fileLength) {
                        break;
                    }
                }
            }*/
            
            out.write(audioBuffer, 0, audioLength);
            out.flush();
        }
        audioIn.close();
        fileIn.close();
        out.close();
        
        System.out.println("Succeed to embed!\n");
    }
	
	public static void hideDataInAudio() throws IOException {
		String audioFilePath = "C:\\Users\\thanh\\Library\\Workspace\\AudioSteganography\\audio_steganography\\input.wav";
		String embedPath = "C:\\Users\\thanh\\Library\\Workspace\\AudioSteganography\\audio_steganography\\message_image2.jpg";
		File audioFile = new File(audioFilePath);
	    File embedFile = new File(embedPath);
	    Metadata f = new Metadata(embedPath);
	    if (audioFile.length() / f.getLength() < 9) {
        	System.out.println("Failed to embed! The file is too big!");
        	return;
        }
	    byte[] audioBytes = Files.readAllBytes(audioFile.toPath());
	    byte[] messageBytes = Files.readAllBytes(embedFile.toPath());
	    int messageLength = messageBytes.length;
	    int audioLength = audioBytes.length;
	    int messageIndex = 0;
	    int wav_header = 44;
	    for (int i = wav_header; i < audioLength && messageIndex < messageLength; i++) {
	        for (int j = 0; j < 8; j++) {
	            int bit = (messageBytes[messageIndex] >> j) & 1;
	            audioBytes[i] = (byte) ((audioBytes[i] & 0xFE) | bit);
	            messageIndex++;
	            if (messageIndex >= messageLength) {
	                break;
	            }
	        }
	    }
	    Files.write(audioFile.toPath(), audioBytes);
	}

}
