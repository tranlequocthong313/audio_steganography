package audio_steganography;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
public class Extracting {
	public static void extract() throws IOException {
		Metadata f = new Metadata();
        File audioFile = new File("C:\\Users\\thanh\\Library\\Workspace\\AudioSteganography\\audio_steganography\\output.wav");
        File outputFile = new File(f.getPath());
        FileInputStream audioIn = new FileInputStream(audioFile);
        FileOutputStream out = new FileOutputStream(outputFile);
        byte[] audioBuffer = new byte[(int)audioFile.length()];
        int audioLength;
        int outputLength = (int)f.getLength();
        int wav_header = 44;
        int temp = 0;
        while ((audioLength = audioIn.read(audioBuffer)) > 0) {
            // Extract the data from the least significant bit of each byte
            for (int i = wav_header; i < audioLength && (i - wav_header) < outputLength; i++) {
            	byte data = 0;
            	byte d = (byte) (audioBuffer[i] & 0x01);
            	temp = temp + d;
            	if ((i - wav_header) % 8 == 0) {
            		data = (byte)temp;
            		temp = 0;
            		d = 0;
            	}
            	else continue;
                //byte data = (byte) (audioBuffer[i] & 0x01);
                out.write(data);
                //System.out.print(data);
            }   
        }
        audioIn.close();
        out.close();
        System.out.println("Succeed to extract!\n");
    }
}
