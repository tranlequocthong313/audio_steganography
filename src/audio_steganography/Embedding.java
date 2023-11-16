package audio_steganography;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
public class Embedding {
	public static void embed() throws IOException {
        File audioFile = new File("C:\\Users\\thanh\\Library\\Workspace\\AudioSteganography\\audio_steganography\\input.wav");
        File fileToEmbed = new File("C:\\Users\\thanh\\Library\\Workspace\\AudioSteganography\\audio_steganography\\message.jpg");
        File outputFile = new File("C:\\Users\\thanh\\Library\\Workspace\\AudioSteganography\\audio_steganography\\output.wav");
        FileInputStream audioIn = new FileInputStream(audioFile);
        FileInputStream fileIn = new FileInputStream(fileToEmbed);
        FileOutputStream out = new FileOutputStream(outputFile);
        Metadata f = new Metadata("C:\\Users\\thanh\\Library\\Workspace\\AudioSteganography\\audio_steganography\\message.jpg");

        byte[] audioBuffer = new byte[(int)audioFile.length()];
        byte[] fileBuffer = new byte[(int)fileToEmbed.length()];
        int audioLength;
        int fileLength;
        int wav_header = 44;
        while ((audioLength = audioIn.read(audioBuffer)) > 0 && (fileLength = fileIn.read(fileBuffer)) > 0) {
            for (int i = 0; i < fileLength; i++) {
            	// lay 6 bit cua audio + tung bit mot cua embed file
            	audioBuffer[i + wav_header] = (byte) ((audioBuffer[i + wav_header] & 0xFE) | (fileBuffer[i] & 0x01));
            }
            out.write(audioBuffer, 0, audioLength);
            out.flush();
        }
        audioIn.close();
        fileIn.close();
        out.close();
        System.out.println("Succeed to embed!\n");
    }
}
